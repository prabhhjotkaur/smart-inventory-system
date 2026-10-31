"""
main.py - Flask Server for Smart Inventory & Dead Stock Management System
Automatically opens http://127.0.0.1:5000 in your web browser.
"""

import sys
import time
import threading
import webbrowser
from collections import deque
from flask import Flask, render_template, request, jsonify

import data_manager
import algorithms

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load items from CSV & initialize FIFO Restock Queue
items = data_manager.load_items()
order_queue = deque()
order_counter = 101


@app.route("/")
def index():
    return render_template("index.html")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route("/api/summary")
def get_summary():
    """Computes basic inventory KPIs and dead stock list."""
    threshold = int(request.args.get("threshold", 60))

    total_value = sum(x["stock"] * x["cost"] for x in items)
    total_units = sum(x["stock"] for x in items)
    low_stock_count = sum(1 for x in items if x["stock"] <= x["min_stock"])

    dead_stock_items = []
    dead_capital = 0

    for x in items:
        days_idle = algorithms.days_since(x["last_sale_date"])
        if days_idle >= threshold and x["stock"] > 0:
            tied_up = x["stock"] * x["cost"]
            dead_capital += tied_up
            dead_stock_items.append({
                "id": x["id"],
                "name": x["name"],
                "category": x["category"],
                "stock": x["stock"],
                "cost": x["cost"],
                "days_idle": days_idle,
                "tied_up": round(tied_up, 2),
                "discount": 40 if days_idle >= 90 else 20
            })

    # Sort dead stock by tied-up capital descending
    dead_stock_items.sort(key=lambda item: item["tied_up"], reverse=True)

    return jsonify({
        "total_items": len(items),
        "total_units": total_units,
        "total_value": round(total_value, 2),
        "low_stock_count": low_stock_count,
        "dead_stock_count": len(dead_stock_items),
        "dead_capital": round(dead_capital, 2),
        "dead_items": dead_stock_items,
        "dead_stock": dead_stock_items  # Supported for compatibility
    })


@app.route("/api/items")
def get_items():
    """Returns items with optional DAA search or sort."""
    query = request.args.get("q", "").strip()
    search_algo = request.args.get("search_algo", "linear")
    sort_key = request.args.get("sort_key", "")
    sort_algo = request.args.get("sort_algo", "merge")
    reverse = request.args.get("reverse", "false").lower() == "true"

    result_items = list(items)
    last_meta = None

    # Search
    if query:
        if search_algo == "binary":
            sorted_by_id, _ = algorithms.merge_sort(result_items, key="id")
            found, meta = algorithms.binary_search(sorted_by_id, query)
            result_items = [found] if found else []
            last_meta = meta
        else:
            result_items, meta = algorithms.linear_search(result_items, query)
            last_meta = meta

    # Sort
    if sort_key and sort_key in ["price", "cost", "stock", "units_sold"]:
        if sort_algo == "bubble":
            result_items, meta = algorithms.bubble_sort(result_items, key=sort_key, reverse=reverse)
            last_meta = meta
        elif sort_algo == "quick":
            result_items, meta = algorithms.quick_sort(result_items, key=sort_key, reverse=reverse)
            last_meta = meta
        else:
            result_items, meta = algorithms.merge_sort(result_items, key=sort_key, reverse=reverse)
            last_meta = meta

    for x in result_items:
        x["days_idle"] = algorithms.days_since(x["last_sale_date"])
        x["value"] = round(x["stock"] * x["cost"], 2)

    return jsonify({
        "items": result_items,
        "meta": last_meta
    })


@app.route("/api/items", methods=["POST"])
def add_item():
    """Adds a new item to inventory."""
    data = request.json or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"success": False, "message": "Name is required"}), 400

    new_id = f"P{len(items) + 101}"
    new_item = {
        "id": new_id,
        "name": name,
        "category": data.get("category", "Stationery"),
        "cost": float(data.get("cost", 10)),
        "price": float(data.get("price", 20)),
        "stock": int(data.get("stock", 20)),
        "min_stock": int(data.get("min_stock", 10)),
        "units_sold": 0,
        "last_sale_date": time.strftime("%Y-%m-%d")
    }
    items.append(new_item)
    data_manager.save_items(items)
    return jsonify({"success": True, "item": new_item})


@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Deletes an item from inventory."""
    global items
    items = [x for x in items if x["id"] != item_id]
    data_manager.save_items(items)
    return jsonify({"success": True})


@app.route("/api/knapsack")
def run_knapsack():
    """Runs 0/1 Knapsack Dynamic Programming budget optimizer."""
    budget = float(request.args.get("budget", 2000))
    result, meta = algorithms.knapsack_restock(items, budget)
    return jsonify({
        "result": result,
        "meta": meta
    })


@app.route("/api/queue", methods=["GET"])
def get_queue():
    """Returns FIFO restock order queue."""
    return jsonify({"queue": list(order_queue)})


@app.route("/api/queue/add", methods=["POST"])
def add_to_queue():
    """Enqueues a restock order (FIFO Queue)."""
    global order_counter
    data = request.json or {}
    item_id = data.get("id")
    name = data.get("name")
    qty = int(data.get("qty", 10))
    cost = float(data.get("cost", 10))

    order = {
        "order_id": f"ORD-{order_counter}",
        "id": item_id,
        "name": name,
        "qty": qty,
        "cost": cost,
        "total": round(qty * cost, 2)
    }
    order_counter += 1
    order_queue.append(order)

    meta = {
        "algorithm": "FIFO Queue (Enqueue)",
        "time_complexity": "O(1)",
        "time_ms": 0.05,
        "details": f"Added {order['order_id']} to restock queue."
    }
    return jsonify({"success": True, "order": order, "meta": meta})


@app.route("/api/queue/process", methods=["POST"])
def process_queue():
    """Dequeues and fulfills the next order (FIFO Queue)."""
    if not order_queue:
        return jsonify({"success": False, "message": "Queue is empty. Add items to queue first."})

    order = order_queue.popleft()
    for x in items:
        if x["id"] == order["id"]:
            x["stock"] += order["qty"]
            break
    data_manager.save_items(items)

    meta = {
        "algorithm": "FIFO Queue (Dequeue)",
        "time_complexity": "O(1)",
        "time_ms": 0.05,
        "details": f"Processed {order['order_id']}: Added +{order['qty']} units to {order['name']}."
    }
    return jsonify({"success": True, "order": order, "meta": meta})


@app.route("/api/reset", methods=["POST"])
def reset_all():
    global items
    items = data_manager.reset_items()
    order_queue.clear()
    return jsonify({"success": True, "message": "Reset to 113 items."})


def auto_open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except Exception:
        pass


if __name__ == "__main__":
    threading.Thread(target=auto_open_browser, daemon=True).start()
    print("=" * 60)
    print(" Smart Inventory & Dead Stock Management System")
    print(" Running at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
