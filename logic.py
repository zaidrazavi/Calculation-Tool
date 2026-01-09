import random
from collections import deque

# =========================================================
# DATA: BHK × ITEMS × (MIN, MAX)  [RUPEES]
# =========================================================

BHK_RANGES = {
    "1BHK": {
        "Modular Kitchen": (250000, 300000),
        "Wardrobe & Storage": (180000, 230000),
        "Furniture": (150000, 200000),
        "Electrical & Lighting": (70000, 100000),
        "Painting & Wall Finish": (60000, 90000),
        "False Ceiling & POP": (70000, 100000),
        "Bathroom & Plumbing": (70000, 100000),
        "Appliances": (150000, 200000),
        "Curtains / Blinds": (40000, 60000),
        "Deep Cleaning & Installation": (23000, 50000),
    },
    "2BHK": {
        "Modular Kitchen": (300000, 350000),
        "Wardrobe & Storage": (250000, 300000),
        "Furniture": (200000, 260000),
        "Electrical & Lighting": (90000, 120000),
        "Painting & Wall Finish": (80000, 110000),
        "False Ceiling & POP": (90000, 120000),
        "Bathroom & Plumbing": (90000, 120000),
        "Appliances": (200000, 260000),
        "Curtains / Blinds": (60000, 80000),
        "Deep Cleaning & Installation": (23000, 60000),
    },
    "3BHK": {
        "Modular Kitchen": (350000, 400000),
        "Wardrobe & Storage": (300000, 360000),
        "Furniture": (260000, 330000),
        "Electrical & Lighting": (110000, 150000),
        "Painting & Wall Finish": (100000, 140000),
        "False Ceiling & POP": (110000, 150000),
        "Bathroom & Plumbing": (110000, 150000),
        "Appliances": (260000, 330000),
        "Curtains / Blinds": (80000, 100000),
        "Deep Cleaning & Installation": (23000, 70000),
    }
}

# =========================================================
# STRICT OUTPUT ORDER (EXCEL STYLE)
# =========================================================

ITEM_ORDER = [
    "Modular Kitchen",
    "Wardrobe & Storage",
    "Furniture",
    "Electrical & Lighting",
    "Painting & Wall Finish",
    "False Ceiling & POP",
    "Bathroom & Plumbing",
    "Appliances",
    "Curtains / Blinds",
    "Deep Cleaning & Installation",
]

# =========================================================
# MEMORY: LAST 5 CALCULATIONS
# =========================================================

history = deque(maxlen=5)

# =========================================================
# CORE LOGIC
# =========================================================

def allocate_budget_flexible(bhk: str, budget: int) -> dict:
    items = list(BHK_RANGES[bhk].items())
    items.sort(key=lambda x: x[1][0])  # sort by minimum cost

    selected = []
    remaining = budget

    # STEP 1: Select feasible items with minimum allocation
    for item, (low, high) in items:
        if remaining >= low:
            selected.append((item, low, high))
            remaining -= low

    if not selected:
        raise ValueError("Budget too low for any interior work")

    # STEP 2: Work in thousands (design logic)
    total_thousands = budget // 1000
    remainder = budget % 1000

    mins = [(item, low // 1000, high // 1000) for item, low, high in selected]

    allocation_k = {}
    remaining_k = total_thousands

    # Assign minimum first
    for item, low_k, _ in mins:
        allocation_k[item] = low_k
        remaining_k -= low_k

    # Distribute remaining randomly (except last item)
    for item, low_k, high_k in mins[:-1]:
        max_extra = min(high_k - low_k, remaining_k)
        extra = random.randint(0, max_extra)
        allocation_k[item] += extra
        remaining_k -= extra

    # Last item absorbs all remaining
    last_item = mins[-1][0]
    allocation_k[last_item] += remaining_k

    # Convert back to rupees
    allocation = {item: allocation_k[item] * 1000 for item in allocation_k}

    # Add remainder (₹ not divisible by 1000) to last item
    allocation[last_item] += remainder

    # STEP 3: FORCE STRICT OUTPUT ORDER
    ordered_allocation = {}
    for item in ITEM_ORDER:
        if item in allocation:
            ordered_allocation[item] = allocation[item]

    return ordered_allocation

def calculate(budget: int, bhk: str) -> dict:
    allocation = allocate_budget_flexible(bhk, budget)

    record = {
        "BHK": bhk,
        "Budget": budget,
        "Breakdown": allocation
    }

    history.appendleft(record)
    return record
