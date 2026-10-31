"""
data_manager.py - CSV persistence & 113 everyday store items
"""

import os
import csv
from datetime import date, timedelta
from typing import List, Dict, Any

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.csv")


def get_default_items() -> List[Dict[str, Any]]:
    today = date.today()

    def d(days_ago):
        return (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    base_templates = [
        ("Ball Pen (Blue)", "Stationery", 5.0, 10.0, 20),
        ("Ball Pen (Black)", "Stationery", 5.0, 10.0, 20),
        ("Gel Pen (Blue)", "Stationery", 10.0, 20.0, 15),
        ("Gel Pen (Red)", "Stationery", 10.0, 20.0, 10),
        ("HB Pencil Pack", "Stationery", 25.0, 45.0, 15),
        ("Plastic Scale 15cm", "Stationery", 6.0, 12.0, 15),
        ("Steel Ruler 30cm", "Stationery", 22.0, 40.0, 10),
        ("White Eraser (Pack of 5)", "Stationery", 12.0, 25.0, 15),
        ("Pencil Sharpener", "Stationery", 4.0, 8.0, 20),
        ("Geometry Box", "Stationery", 65.0, 110.0, 8),
        ("Spiral Notebook 200 Pgs", "Stationery", 45.0, 75.0, 15),
        ("A4 Copier Paper Ream", "Stationery", 180.0, 260.0, 10),
        ("Sticky Notes Yellow", "Stationery", 20.0, 35.0, 15),
        ("Fevicol Glue 100g", "Stationery", 25.0, 40.0, 12),
        ("Clear Tape 1 inch", "Stationery", 15.0, 25.0, 15),
        ("Paper Cutter Knife", "Stationery", 18.0, 30.0, 10),
        ("Permanent Marker Black", "Stationery", 15.0, 25.0, 15),
        ("Whiteboard Marker Blue", "Stationery", 18.0, 30.0, 12),
        ("Stapler Small", "Stationery", 40.0, 65.0, 8),
        ("Stapler Pins Box", "Stationery", 12.0, 20.0, 20),
        ("Paper Clips Box", "Stationery", 15.0, 25.0, 15),
        ("Document Folder Plastic", "Stationery", 18.0, 35.0, 15),
        ("Highlighter Yellow", "Stationery", 16.0, 30.0, 12),
        ("Correction Pen Whitener", "Stationery", 22.0, 35.0, 10),

        # Electrical
        ("LED Bulb 9W (Cool White)", "Electrical", 65.0, 110.0, 15),
        ("LED Bulb 12W", "Electrical", 85.0, 140.0, 12),
        ("LED Bulb 15W", "Electrical", 110.0, 175.0, 10),
        ("CFL Bulb 18W (Old Stock)", "Electrical", 70.0, 110.0, 8),
        ("Incandescent Bulb 60W Yellow", "Electrical", 12.0, 20.0, 15),
        ("Tube Light Batten 20W", "Electrical", 140.0, 220.0, 10),
        ("Night Lamp 0.5W", "Electrical", 25.0, 45.0, 12),
        ("3-Pin Power Plug Top 16A", "Electrical", 30.0, 55.0, 15),
        ("2-Pin Flat Plug", "Electrical", 10.0, 20.0, 20),
        ("Modular Switch 6A", "Electrical", 22.0, 40.0, 20),
        ("Modular Socket 6A", "Electrical", 35.0, 60.0, 15),
        ("Electric Insulation Tape", "Electrical", 10.0, 18.0, 25),
        ("Extension Cord 4-Way 2m", "Electrical", 180.0, 280.0, 8),
        ("Tester Screwdriver 500V", "Electrical", 25.0, 45.0, 10),
        ("Copper Wire Coil 1.5 sq mm", "Electrical", 550.0, 780.0, 5),
        ("Ceiling Fan Regulator", "Electrical", 95.0, 160.0, 8),
        ("Door Bell (Ding Dong)", "Electrical", 110.0, 190.0, 6),
        ("AA Alkaline Battery (4-Pk)", "Electrical", 60.0, 95.0, 15),
        ("AAA Pencil Battery (4-Pk)", "Electrical", 60.0, 95.0, 15),
        ("9V Radio Battery", "Electrical", 25.0, 45.0, 10),

        # Hardware & General
        ("Steel Padlock 40mm", "Hardware", 75.0, 120.0, 8),
        ("Brass Padlock 50mm", "Hardware", 140.0, 220.0, 6),
        ("Screwdriver Set 6-in-1", "Hardware", 85.0, 150.0, 6),
        ("Combination Pliers 8-inch", "Hardware", 110.0, 180.0, 5),
        ("Hand Hammer 500g", "Hardware", 95.0, 160.0, 5),
        ("Measuring Tape 3 Meter", "Hardware", 45.0, 80.0, 10),
        ("Measuring Tape 5 Meter", "Hardware", 70.0, 120.0, 8),
        ("Nails 2-inch Box 500g", "Hardware", 40.0, 65.0, 10),
        ("Wood Screws Assorted Box", "Hardware", 50.0, 85.0, 10),
        ("Wall Plugs Rawl Gitti (100)", "Hardware", 25.0, 45.0, 15),
        ("Hacksaw Frame with Blade", "Hardware", 80.0, 140.0, 5),
        ("Spare Hacksaw Blades (3)", "Hardware", 20.0, 35.0, 10),
        ("WD-40 Spray 64g", "Hardware", 110.0, 150.0, 6),
        ("M-Seal Epoxy Putty 50g", "Hardware", 15.0, 25.0, 20),
        ("Super Glue Fevikwik 3g", "Hardware", 4.0, 5.0, 40),
        ("Sandpaper Sheet Medium", "Hardware", 8.0, 15.0, 25),
        ("Paint Brush 2-inch", "Hardware", 25.0, 45.0, 12),
        ("Cotton Cleaning Cloth Duster", "General", 15.0, 30.0, 20),
        ("Microfiber Cloth", "General", 35.0, 65.0, 15),
        ("Plastic Spray Bottle 500ml", "General", 30.0, 55.0, 10),
        ("Stainless Steel Scissors 7-in", "General", 35.0, 65.0, 10),
        ("Torch Light Rechargeable", "General", 120.0, 195.0, 8),
        ("Calculator 8-Digit Pocket", "Stationery", 85.0, 140.0, 6),
        ("Desktop Desk Organizer", "Stationery", 95.0, 160.0, 5),
    ]

    items = []
    pid = 101

    for i, (name, cat, cost, price, min_stock) in enumerate(base_templates):
        if i % 7 == 0:
            # Dead Stock: idle > 90 days
            stock = min_stock * 2 + 10
            sold = 2
            days_ago = 95 + (i * 2)
        elif i % 5 == 0:
            # Low Stock: stock <= min_stock
            stock = max(1, min_stock // 3)
            sold = 85
            days_ago = 2 + (i % 4)
        elif i % 4 == 0:
            # Slow moving: 45-70 days
            stock = min_stock + 8
            sold = 15
            days_ago = 45 + (i % 25)
        else:
            # Fast moving: 1-8 days
            stock = min_stock * 2
            sold = 120 + (i * 3)
            days_ago = 1 + (i % 8)

        items.append({
            "id": f"P{pid}",
            "name": name,
            "category": cat,
            "cost": float(cost),
            "price": float(price),
            "stock": int(stock),
            "min_stock": int(min_stock),
            "units_sold": int(sold),
            "last_sale_date": d(days_ago)
        })
        pid += 1

    variations = [
        ("Register Notebook 100 Pgs", "Stationery", 25, 40, 15, 65, 2),
        ("Register Notebook 300 Pgs", "Stationery", 65, 105, 10, 15, 45),
        ("Graph Paper Pad 50 Sheets", "Stationery", 20, 35, 10, 8, 120),
        ("Ruled Exam Sheets (Bundle)", "Stationery", 70, 110, 10, 45, 5),
        ("Plastic Clip File A4", "Stationery", 12, 25, 15, 60, 4),
        ("Ring Binder File Big", "Stationery", 60, 95, 8, 4, 110),
        ("White Chalk Box 100pcs", "Stationery", 30, 50, 10, 5, 130),
        ("Dustless Colored Chalk Box", "Stationery", 40, 65, 8, 2, 140),
        ("Duster Sponge for Board", "Stationery", 20, 35, 10, 15, 18),
        ("Stamp Pad Ink Bottle 30ml", "Stationery", 22, 35, 8, 3, 115),
        ("Stamp Pad Blue Small", "Stationery", 25, 40, 10, 12, 22),
        ("Glue Stick 15g", "Stationery", 20, 35, 15, 40, 3),
        ("Drawing Sheet Cartridge (10)", "Stationery", 35, 60, 10, 18, 12),
        ("Sketch Pen Set 12 Colors", "Stationery", 30, 50, 12, 35, 4),
        ("Wax Crayons 16 Shades", "Stationery", 25, 45, 12, 22, 8),
        ("Oil Pastels 25 Shades Box", "Stationery", 65, 100, 8, 14, 15),
        ("Water Color Tube Set 12", "Stationery", 75, 120, 6, 8, 48),
        ("Painting Brush Round #4", "Stationery", 15, 25, 10, 12, 15),
        ("Painting Brush Flat #8", "Stationery", 25, 40, 8, 6, 95),
        ("Color Palette Plastic", "Stationery", 15, 25, 10, 4, 110),
        ("LED Bulb 7W Warm White", "Electrical", 55, 90, 12, 30, 3),
        ("LED Bulb 20W High Power", "Electrical", 160, 250, 6, 2, 85),
        ("LED Panel Light 6W Round", "Electrical", 140, 220, 8, 3, 105),
        ("LED Panel Light 12W Square", "Electrical", 210, 320, 6, 2, 130),
        ("Strip Light Warm 5 Meter", "Electrical", 160, 260, 5, 8, 65),
        ("Halogen Bulb 500W (Heavy)", "Electrical", 45, 80, 5, 12, 160),
        ("Ceiling Rose White", "Electrical", 15, 25, 15, 25, 6),
        ("Batten Holder Angled", "Electrical", 18, 30, 15, 30, 4),
        ("Pendant Lamp Holder Brass", "Electrical", 25, 45, 10, 4, 115),
        ("Bed Switch Single 6A", "Electrical", 15, 25, 15, 18, 10),
        ("Anchor PVC Gang Box 1-Way", "Electrical", 18, 30, 15, 25, 5),
        ("Anchor PVC Gang Box 4-Way", "Electrical", 40, 65, 10, 12, 8),
        ("Casing Capping 1-inch 2m", "Electrical", 28, 45, 15, 35, 3),
        ("Wire Grip Clips 8mm (100)", "Electrical", 22, 35, 15, 40, 2),
        ("Cable Ties 4-inch (Pack 100)", "Electrical", 25, 45, 15, 50, 1),
        ("Cable Ties 8-inch (Pack 100)", "Electrical", 45, 75, 10, 35, 4),
        ("Insulation Tape Red", "Electrical", 10, 18, 20, 25, 3),
        ("Insulation Tape Green", "Electrical", 10, 18, 20, 20, 6),
        ("Fuse Wire 5 Amp Reel", "Electrical", 12, 20, 10, 4, 140),
        ("Main Switch Rewireable 16A", "Electrical", 180, 290, 4, 2, 150),
        ("Soldering Iron 25W", "Hardware", 110, 175, 5, 6, 12),
        ("Soldering Lead Wire 50g", "Hardware", 45, 75, 8, 12, 8),
        ("Soldering Flux Paste 15g", "Hardware", 15, 25, 10, 15, 5),
        ("Steel Wire Brush Small", "Hardware", 25, 40, 8, 5, 95),
        ("Spirit Level 12-inch", "Hardware", 85, 140, 5, 3, 110),
    ]

    for name, cat, cost, price, min_stock, stock, days_ago in variations:
        items.append({
            "id": f"P{pid}",
            "name": name,
            "category": cat,
            "cost": float(cost),
            "price": float(price),
            "stock": int(stock),
            "min_stock": int(min_stock),
            "units_sold": 45 if days_ago < 30 else 5,
            "last_sale_date": d(days_ago)
        })
        pid += 1

    return items


def load_items() -> List[Dict[str, Any]]:
    if not os.path.exists(CSV_FILE):
        return reset_items()

    items = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append({
                    "id": str(row["id"]),
                    "name": str(row["name"]),
                    "category": str(row["category"]),
                    "cost": float(row["cost"]),
                    "price": float(row["price"]),
                    "stock": int(row["stock"]),
                    "min_stock": int(row["min_stock"]),
                    "units_sold": int(row.get("units_sold", 0)),
                    "last_sale_date": str(row.get("last_sale_date", date.today().strftime("%Y-%m-%d")))
                })
        return items if items else reset_items()
    except Exception:
        return reset_items()


def save_items(items: List[Dict[str, Any]]) -> None:
    fieldnames = ["id", "name", "category", "cost", "price", "stock", "min_stock", "units_sold", "last_sale_date"]
    try:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow({
                    "id": item["id"],
                    "name": item["name"],
                    "category": item["category"],
                    "cost": item["cost"],
                    "price": item["price"],
                    "stock": item["stock"],
                    "min_stock": item["min_stock"],
                    "units_sold": item.get("units_sold", 0),
                    "last_sale_date": item.get("last_sale_date", date.today().strftime("%Y-%m-%d"))
                })
    except Exception as e:
        print(f"Warning: Could not save inventory CSV: {e}")


def reset_items() -> List[Dict[str, Any]]:
    items = get_default_items()
    save_items(items)
    return items
