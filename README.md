# Smart Inventory & Dead Stock Management System

A clean, interactive Python inventory management application. It helps retail store managers track stock, identify stagnant capital (**Dead Stock**), optimize restocking under a fixed budget using **0/1 Knapsack Dynamic Programming**, and fulfill supplier replenishment orders with a **FIFO Queue**.

---

## 🚀 How to Run the Application

### Option 1: One-Click Run (Windows)
Simply double-click the **`run.bat`** file in this folder. It automatically installs requirements and opens `http://127.0.0.1:5000` in your web browser.

### Option 2: One-Click Run (macOS / Linux)
Open your terminal in this directory and execute:
```bash
bash run.sh
```

### Option 3: Standard Terminal Execution
```bash
pip install -r requirements.txt
python main.py
```
> The application will automatically launch in your default web browser at `http://127.0.0.1:5000`.

---

## 📁 Project Architecture & File Breakdown

| File / Folder | Role & Purpose |
| :--- | :--- |
| **`main.py`** | Flask web server. Sets up routing, handles REST API endpoints for inventory operations, and auto-opens the web browser. |
| **`algorithms.py`** | Manual implementations of Design & Analysis of Algorithms (DAA): Linear Search, Binary Search, Bubble Sort, Merge Sort, Quick Sort, and 0/1 Knapsack Dynamic Programming. |
| **`data_manager.py`** | Handles persistent CSV read/write operations with concurrency safety and contains the default catalog of 113 everyday store items. |
| **`inventory.csv`** | Persistent flat-file storage storing Item ID, Name, Category, Cost Price, Selling Price, Current Stock, Minimum Stock, Units Sold, and Last Sale Date. |
| **`templates/index.html`** | Clean, responsive single-page user interface with 3 main navigation views. |
| **`static/css/style.css`** | Clean SaaS styling with high-contrast KPI cards, tables, badges, and non-blocking toast notifications. |
| **`static/js/app.js`** | Client-side controller handling search/filter events, API synchronization, DOM rendering, and real-time algorithmic telemetry. |
| **`requirements.txt`** | Dependency manifest listing `flask>=2.2.0`. |
| **`run.bat`** | Automated launch batch script for Windows environments. |
| **`run.sh`** | Automated launch shell script for Unix/Linux/macOS environments. |
| **`.gitignore`** | Excludes temporary Python artifacts (`__pycache__`, `.env`, `.DS_Store`). |

---

## 🐍 Python Libraries Used & Justification

1. **`Flask`**: Provides a lightweight local HTTP server and REST API interface so the application can be cleanly accessed in any modern web browser without complex GUI dependencies.
2. **`csv`** *(Python Built-in)*: Used for simple, transparent, file-based persistence without requiring a separate SQL database server.
3. **`datetime`** *(Python Built-in)*: Used to calculate the exact number of idle days since the last sale date (`days_idle = (current_date - last_sale_date).days`).
4. **`time`** *(Python Built-in)*: Measures execution durations in milliseconds for every algorithmic query, powering the live telemetry inspector banner.
5. **`webbrowser` & `threading`** *(Python Built-in)*: Auto-launches the application in the system's default web browser when `main.py` is executed.

---

## 🧠 Design and Analysis of Algorithms (DAA) Implemented

| Algorithm | Paradigm | Time Complexity | Real-World Application in System |
| :--- | :--- | :--- | :--- |
| **Linear Search** | Brute Force | $O(n)$ | Searches product names or categories sequentially without requiring prior sorting. |
| **Binary Search** | Divide & Conquer | $O(\log n)$ | Quickly locates items by Item ID in $O(\log n)$ after verifying/sorting the array. |
| **Merge Sort** | Divide & Conquer | $O(n \log n)$ | Stable sorting by Stock Quantity, Unit Cost, Selling Price, or Units Sold. |
| **Quick Sort** | Divide & Conquer | $O(n \log n)$ | Fast in-place partitioning to sort the catalog by Item ID or Name. |
| **Bubble Sort** | Comparison Sort | $O(n^2)$ | Baseline educational sorting algorithm used for comparative analysis. |
| **0/1 Knapsack** | Dynamic Programming | $O(n \cdot W)$ | Solves the inventory budget restock dilemma by maximizing profit under a fixed budget constraint. |
| **FIFO Restock Queue** | First-In, First-Out | $O(1)$ | Manages supplier replenishment orders in the exact order they were issued. |

---

## 💡 System Features & Modules

### 1. Dashboard (Dead Stock Aging Scanner)
- Automatically filters items sitting idle without sales for more than **30, 60, or 90 days**.
- Calculates the total **Tied-up Capital** ($\text{Stock Quantity} \times \text{Cost Price}$) trapped in idle goods.
- Suggests actionable markdown clearance discounts (e.g. 20% or 40% off) to recover cash.

### 2. All Items (Catalog Management)
- Complete table view of all 113 everyday store items (Pens, Bulbs, Cables, Tapes, Sockets, Rulers).
- Search with instant algorithm telemetry (displaying algorithm name, time taken in ms, and time complexity).
- Sorting controls with choice of algorithm (Merge Sort, Quick Sort, Bubble Sort).
- Add new items and delete obsolete items.

### 3. Restock Optimizer (Knapsack DP & FIFO Queue)
- **Knapsack DP Solver**: Given a restocking budget (e.g., ₹2,000), it selects the combination of low-stock items that yields maximum profit.
- **FIFO Restock Queue**: Click "+ Add to Queue" on recommended items, then click "Process Next Order" to increment current inventory stock in real time.

---

## 📤 How to Publish This Project to GitHub

### Method A: Web Upload (No Git Installation Required - 1 Minute)
1. Go to [github.com](https://github.com) and log in to your account.
2. In the top-right corner, click **+** and select **New repository**.
3. Name your repository (e.g., `projectdaa-python` or `smart-inventory-system`).
4. Keep it **Public** and do **not** check "Add a README file" (since you already have one).
5. Click **Create repository**.
6. On the empty repository page, click the link **"uploading an existing file"**.
7. Drag and drop all the files from your `Desktop/projectdaa-python` folder into the browser window.
8. Click **Commit changes**. Your project is now published!

### Method B: Using Git Command Line
If Git is installed on your computer, open PowerShell or Command Prompt in this folder and run:
```bash
git init
git add .
git commit -m "Initial commit: Smart Inventory and Dead Stock Management System"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
git push -u origin main
```
