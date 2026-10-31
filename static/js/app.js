/**
 * app.js - Frontend controller for Smart Inventory & Dead Stock Management System
 */

let currentThreshold = 60;

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
    loadItems();
    runKnapsack();
    loadQueue();
});

// Non-blocking Toast Notification
function showToast(message, isError = false) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast ${isError ? "error" : "success"} show`;
    setTimeout(() => {
        toast.className = "toast";
    }, 3500);
}

// Update the algorithm info banner
function updateAlgoBanner(meta) {
    if (!meta) return;
    const tag = document.getElementById("algoTag");
    const time = document.getElementById("algoTime");
    const comp = document.getElementById("algoComplexity");
    const detail = document.getElementById("algoDetail");

    if (tag) tag.textContent = `Algorithm: ${meta.algorithm || "Direct"}`;
    if (time) time.textContent = `${meta.time_ms !== undefined ? meta.time_ms : 0.05} ms`;
    if (comp) comp.textContent = meta.time_complexity || "O(1)";
    if (detail) detail.textContent = meta.details || "Query executed.";
}

// Tab navigation
function showTab(tabName) {
    document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));

    const target = document.getElementById(`tab-${tabName}`);
    if (target) target.classList.add("active");

    const btn = Array.from(document.querySelectorAll(".nav-btn")).find(b =>
        b.getAttribute("onclick") && b.getAttribute("onclick").includes(tabName)
    );
    if (btn) btn.classList.add("active");

    if (tabName === "dashboard") loadDashboard();
    if (tabName === "inventory") loadItems();
    if (tabName === "restock") {
        runKnapsack();
        loadQueue();
    }
}

// ============================================================================
// 1. DASHBOARD & DEAD STOCK (PAGE 1)
// ============================================================================

async function loadDashboard() {
    try {
        const res = await fetch(`/api/summary?threshold=${currentThreshold}`);
        const data = await res.json();

        // 1. Update KPI numbers (NO "SKUs" text!)
        const kpiItems = document.getElementById("kpiItems");
        if (kpiItems) kpiItems.textContent = data.total_items;

        const kpiUnits = document.getElementById("kpiUnits");
        if (kpiUnits) kpiUnits.textContent = `${data.total_units.toLocaleString()} Units`;

        const kpiValue = document.getElementById("kpiValue");
        if (kpiValue) kpiValue.textContent = `₹${data.total_value.toLocaleString("en-IN", {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        const kpiDead = document.getElementById("kpiDeadCapital");
        if (kpiDead) kpiDead.textContent = `₹${data.dead_capital.toLocaleString("en-IN", {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        // 2. Populate Dead Stock Table
        const tbody = document.getElementById("deadTableBody");
        if (tbody) {
            tbody.innerHTML = "";
            const deadList = data.dead_items || data.dead_stock || [];

            if (deadList.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 24px; color: #64748b;">No items idle for more than ${currentThreshold} days.</td></tr>`;
            } else {
                deadList.forEach(x => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td><b>${x.id}</b></td>
                        <td><b>${x.name}</b></td>
                        <td>${x.category}</td>
                        <td>${x.stock} units</td>
                        <td>₹${x.cost.toFixed(2)}</td>
                        <td><b class="text-red">${x.days_idle} days</b></td>
                        <td><b class="text-red">₹${x.tied_up.toLocaleString("en-IN", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</b></td>
                        <td><span class="badge badge-amber">Apply ${x.discount}% Discount</span></td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        updateAlgoBanner({
            algorithm: "Dead Stock Filter",
            time_complexity: "O(n)",
            time_ms: 0.12,
            details: `Scanned all ${data.total_items} items to identify ${data.dead_stock_count} dead stock items.`
        });
    } catch (err) {
        console.error("Dashboard load error:", err);
    }
}

function setThreshold(days) {
    currentThreshold = days;
    document.querySelectorAll(".pill-btn").forEach(btn => {
        btn.classList.toggle("active", btn.textContent.includes(`${days} Days`));
    });
    loadDashboard();
}

// ============================================================================
// 2. ALL ITEMS (SEARCH & SORT)
// ============================================================================

async function loadItems() {
    searchItems();
}

async function searchItems() {
    const q = document.getElementById("searchInput") ? document.getElementById("searchInput").value : "";
    const searchAlgo = document.getElementById("searchAlgo") ? document.getElementById("searchAlgo").value : "linear";
    const sortKey = document.getElementById("sortKey") ? document.getElementById("sortKey").value : "";
    const sortAlgo = document.getElementById("sortAlgo") ? document.getElementById("sortAlgo").value : "merge";
    const sortOrder = document.getElementById("sortOrder") ? document.getElementById("sortOrder").value : "asc";
    const reverse = (sortOrder === "desc");

    try {
        const res = await fetch(`/api/items?q=${encodeURIComponent(q)}&search_algo=${searchAlgo}&sort_key=${sortKey}&sort_algo=${sortAlgo}&reverse=${reverse}`);
        const data = await res.json();

        const tbody = document.getElementById("itemsTableBody");
        if (!tbody) return;
        tbody.innerHTML = "";

        if (!data.items || data.items.length === 0) {
            tbody.innerHTML = `<tr><td colspan="12" style="text-align:center; padding: 24px; color:#64748b;">No matching items found.</td></tr>`;
            return;
        }

        data.items.forEach(x => {
            let statusBadge = `<span class="badge badge-green">In Stock</span>`;
            if (x.stock === 0) {
                statusBadge = `<span class="badge badge-red">Out of Stock</span>`;
            } else if (x.stock <= x.min_stock) {
                statusBadge = `<span class="badge badge-amber">Low Stock</span>`;
            }

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><b>${x.id}</b></td>
                <td><b>${x.name}</b></td>
                <td>${x.category}</td>
                <td>₹${x.cost.toFixed(2)}</td>
                <td><b>₹${x.price.toFixed(2)}</b></td>
                <td>${x.stock}</td>
                <td>${x.min_stock}</td>
                <td>${x.units_sold}</td>
                <td>₹${x.value.toLocaleString()}</td>
                <td>${x.days_idle} d</td>
                <td>${statusBadge}</td>
                <td><button class="btn-del" onclick="deleteItem('${x.id}', '${x.name}')">Delete</button></td>
            `;
            tbody.appendChild(tr);
        });

        updateAlgoBanner(data.meta);
    } catch (err) {
        console.error("Search error:", err);
    }
}

function sortItems() {
    searchItems();
}

// Add Item Modal
function openAddModal() {
    const modal = document.getElementById("addModal");
    if (modal) modal.classList.add("open");
}

function closeAddModal() {
    const modal = document.getElementById("addModal");
    if (modal) modal.classList.remove("open");
}

async function saveNewItem() {
    const name = document.getElementById("new_name").value.trim();
    if (!name) {
        showToast("Please enter item name.", true);
        return;
    }

    const payload = {
        name: name,
        category: document.getElementById("new_category").value,
        cost: parseFloat(document.getElementById("new_cost").value) || 10,
        price: parseFloat(document.getElementById("new_price").value) || 20,
        stock: parseInt(document.getElementById("new_stock").value) || 20,
        min_stock: parseInt(document.getElementById("new_min_stock").value) || 10
    };

    try {
        const res = await fetch("/api/items", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            closeAddModal();
            showToast(`Added '${name}' successfully!`);
            loadItems();
            loadDashboard();
        } else {
            showToast(data.message || "Failed to add item.", true);
        }
    } catch (err) {
        showToast("Failed to connect to server.", true);
    }
}

async function deleteItem(id, name) {
    if (!confirm(`Are you sure you want to delete '${name}' (${id})?`)) return;
    try {
        const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
        const data = await res.json();
        if (data.success) {
            showToast(`Deleted '${name}'.`);
            loadItems();
            loadDashboard();
        }
    } catch (err) {
        showToast("Failed to delete item.", true);
    }
}

// ============================================================================
// 3. RESTOCK (KNAPSACK & FIFO ORDER QUEUE)
// ============================================================================

async function runKnapsack() {
    const input = document.getElementById("budgetInput");
    const budget = parseFloat(input ? input.value : 2000) || 2000;

    try {
        const res = await fetch(`/api/knapsack?budget=${budget}`);
        const data = await res.json();
        const r = data.result;

        const summaryBox = document.getElementById("budgetSummary");
        if (summaryBox) {
            summaryBox.innerHTML = `
                <span>Total Spent: <b>₹${r.total_spent.toLocaleString()}</b></span>
                <span>Remaining Budget: <b>₹${r.remaining_budget.toLocaleString()}</b></span>
                <span>Expected Profit: <b class="text-green">+₹${r.expected_profit.toLocaleString()}</b></span>
            `;
        }

        const tbody = document.getElementById("knapsackTableBody");
        if (!tbody) return;
        tbody.innerHTML = "";

        if (!r.selected_items || r.selected_items.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 24px; color:#64748b;">No items need restocking or budget too low.</td></tr>`;
            return;
        }

        r.selected_items.forEach(x => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><b>${x.id}</b></td>
                <td><b>${x.name}</b></td>
                <td><b class="text-blue">+${x.qty} units</b></td>
                <td>₹${x.cost}</td>
                <td><b class="text-green">+₹${x.profit}</b></td>
                <td>
                    <button class="btn-blue btn-sm" onclick="addToQueue('${x.id}', '${x.name.replace(/'/g, "\\'")}', ${x.qty}, ${x.cost / x.qty})">
                        + Add to Queue
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        updateAlgoBanner(data.meta);
    } catch (err) {
        console.error("Knapsack error:", err);
    }
}

async function loadQueue() {
    try {
        const res = await fetch("/api/queue");
        const data = await res.json();

        const tbody = document.getElementById("queueTableBody");
        if (!tbody) return;
        tbody.innerHTML = "";

        if (!data.queue || data.queue.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 24px; color:#64748b;">Queue is empty.</td></tr>`;
            return;
        }

        data.queue.forEach(o => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><b>${o.order_id}</b></td>
                <td><b>${o.name}</b></td>
                <td>+${o.qty} units</td>
                <td><b>₹${o.total.toFixed(2)}</b></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Queue load error:", err);
    }
}

async function addToQueue(id, name, qty, cost) {
    try {
        const res = await fetch("/api/queue/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id, name, qty, cost })
        });
        const data = await res.json();
        if (data.success) {
            showToast(`Added ${data.order.order_id} (${name}) to restock queue.`);
            loadQueue();
            updateAlgoBanner(data.meta);
        }
    } catch (err) {
        showToast("Failed to queue order.", true);
    }
}

async function processQueue() {
    try {
        const res = await fetch("/api/queue/process", { method: "POST" });
        const data = await res.json();

        if (data.success) {
            showToast(`✅ ${data.meta.details}`);
            await loadQueue();
            loadItems();
            loadDashboard();
            updateAlgoBanner(data.meta);
        } else {
            showToast(data.message || "Queue is empty. Add items first.", true);
        }
    } catch (err) {
        console.error("Queue process error:", err);
        showToast("Failed to process queue.", true);
    }
}

async function resetData() {
    if (!confirm("Reset to default 113 items?")) return;
    try {
        const res = await fetch("/api/reset", { method: "POST" });
        const data = await res.json();
        showToast(data.message || "Reset successful!");
        loadDashboard();
        loadItems();
        runKnapsack();
        loadQueue();
    } catch (err) {
        showToast("Failed to reset.", true);
    }
}
