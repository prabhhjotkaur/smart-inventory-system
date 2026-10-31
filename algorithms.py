"""
algorithms.py - Simple, clean implementations of required DAA algorithms:
1. Linear Search - O(n)
2. Binary Search - O(log n)
3. Bubble Sort - O(n^2)
4. Merge Sort - O(n log n)
5. Quick Sort - O(n log n)
6. 0/1 Knapsack (Dynamic Programming) - O(n * W)
7. Restock Queue (FIFO) - O(1)
"""

import time
from datetime import datetime, date
from typing import List, Dict, Any, Tuple, Optional


def days_since(date_str: str) -> int:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return max(0, (date.today() - d).days)
    except Exception:
        return 0


# ============================================================================
# 1. SEARCHING ALGORITHMS
# ============================================================================

def linear_search(items: List[Dict[str, Any]], query: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Linear Search: Scans every item sequentially."""
    t0 = time.perf_counter()
    q = query.strip().lower()

    results = []
    for item in items:
        if q in item["name"].lower() or q in item["id"].lower() or q in item["category"].lower():
            results.append(item)

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    meta = {
        "algorithm": "Linear Search",
        "time_complexity": "O(n)",
        "time_ms": round(elapsed_ms, 3),
        "details": f"Checked all {len(items)} items sequentially."
    }
    return results, meta


def binary_search(sorted_items: List[Dict[str, Any]], target_id: str) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    """Binary Search: Halves the search space on pre-sorted items."""
    t0 = time.perf_counter()
    target = target_id.strip().upper()

    low = 0
    high = len(sorted_items) - 1
    found = None
    steps = 0

    while low <= high:
        steps += 1
        mid = (low + high) // 2
        mid_id = sorted_items[mid]["id"].upper()

        if mid_id == target:
            found = sorted_items[mid]
            break
        elif mid_id < target:
            low = mid + 1
        else:
            high = mid - 1

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    meta = {
        "algorithm": "Binary Search",
        "time_complexity": "O(log n)",
        "time_ms": round(elapsed_ms, 3),
        "details": f"Found in {steps} steps out of {len(sorted_items)} items."
    }
    return found, meta


# ============================================================================
# 2. SORTING ALGORITHMS
# ============================================================================

def bubble_sort(items: List[Dict[str, Any]], key: str = "price", reverse: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Bubble Sort: Compares adjacent elements and swaps them."""
    t0 = time.perf_counter()
    arr = list(items)
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            val_a = arr[j][key]
            val_b = arr[j + 1][key]
            if (val_a < val_b) if reverse else (val_a > val_b):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    meta = {
        "algorithm": "Bubble Sort",
        "time_complexity": "O(n²)",
        "time_ms": round(elapsed_ms, 3),
        "details": f"Sorted {len(arr)} items by {key}."
    }
    return arr, meta


def merge_sort(items: List[Dict[str, Any]], key: str = "price", reverse: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Merge Sort: Divide and Conquer sorting."""
    t0 = time.perf_counter()
    arr = list(items)

    def _merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            val_l = left[i][key]
            val_r = right[j][key]
            if (val_l >= val_r) if reverse else (val_l <= val_r):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_arr = _merge_sort(arr)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    meta = {
        "algorithm": "Merge Sort",
        "time_complexity": "O(n log n)",
        "time_ms": round(elapsed_ms, 3),
        "details": f"Sorted {len(sorted_arr)} items by {key}."
    }
    return sorted_arr, meta


def quick_sort(items: List[Dict[str, Any]], key: str = "price", reverse: bool = False) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Quick Sort: Partitioning around a pivot."""
    t0 = time.perf_counter()
    arr = list(items)

    def _qsort(a, low, high):
        if low < high:
            pivot = a[high][key]
            i = low - 1
            for j in range(low, high):
                curr = a[j][key]
                if (curr >= pivot) if reverse else (curr <= pivot):
                    i += 1
                    a[i], a[j] = a[j], a[i]
            a[i + 1], a[high] = a[high], a[i + 1]
            pi = i + 1

            _qsort(a, low, pi - 1)
            _qsort(a, pi + 1, high)

    if arr:
        _qsort(arr, 0, len(arr) - 1)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    meta = {
        "algorithm": "Quick Sort",
        "time_complexity": "O(n log n)",
        "time_ms": round(elapsed_ms, 3),
        "details": f"Sorted {len(arr)} items by {key}."
    }
    return arr, meta


# ============================================================================
# 3. 0/1 KNAPSACK FOR RESTOCK BUDGET OPTIMIZATION
# ============================================================================

def knapsack_restock(items: List[Dict[str, Any]], budget: float) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    0/1 Knapsack Problem using Dynamic Programming.
    Maximizes profit of restocked items without exceeding budget.
    """
    t0 = time.perf_counter()

    # Find candidate items needing restocking (stock <= min_stock)
    candidates = []
    for item in items:
        if item["stock"] <= item["min_stock"]:
            qty_needed = max(10, (item["min_stock"] * 2) - item["stock"])
            cost = int(round(qty_needed * item["cost"]))
            profit = int(round(qty_needed * (item["price"] - item["cost"])))
            if cost > 0:
                candidates.append({
                    "id": item["id"],
                    "name": item["name"],
                    "category": item["category"],
                    "qty": qty_needed,
                    "cost": cost,
                    "profit": profit
                })

    n = len(candidates)
    W = max(1, int(budget))

    scale = 1
    if W > 2000:
        scale = 10
        W = W // 10

    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = max(1, candidates[i - 1]["cost"] // scale)
        v_i = candidates[i - 1]["profit"]
        for w in range(W + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    curr_w = W
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            selected.append(candidates[i - 1])
            curr_w -= max(1, candidates[i - 1]["cost"] // scale)

    selected.reverse()
    total_cost = sum(x["cost"] for x in selected)
    total_profit = sum(x["profit"] for x in selected)

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    meta = {
        "algorithm": "0/1 Knapsack (Dynamic Programming)",
        "time_complexity": "O(n · W)",
        "time_ms": round(elapsed_ms, 3),
        "details": f"Optimized {len(selected)} items within budget of ₹{budget:,.0f}."
    }

    result = {
        "budget": budget,
        "total_spent": total_cost,
        "remaining_budget": max(0, budget - total_cost),
        "expected_profit": total_profit,
        "selected_items": selected
    }
    return result, meta
