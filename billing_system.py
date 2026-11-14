import json
import math
from datetime import date, datetime, timedelta
from pathlib import Path

HISTORY_FILE = Path("bill_history.json")
#  cd "C:\Users\mutta\OneDrive\Documents\New project"
# py billing_system.py
# Simple domestic metered tariff example (rupees per unit).
SLABS = [(200, 2.45), (400, 4.20), (None, 4.60)]
FIXED_CHARGE_PER_KW = 10.00
DUE_DAYS = 15


def read_number(prompt, minimum=0, default=None):
    while True:
        value = input(prompt).strip()
        if value == "" and default is not None:
            return default
        try:
            number = float(value)
            if number < minimum:
                print(f"Enter a number at least {minimum}.")
                continue
            return number
        except ValueError:
            print("Please enter a valid number.")


def energy_charge(units):
    charge = 0
    previous_limit = 0
    remaining = units

    for limit, rate in SLABS:
        if limit is None:
            slab_units = remaining
        else:
            slab_units = min(remaining, limit - previous_limit)

        charge += slab_units * rate
        remaining -= slab_units
        if limit is not None:
            previous_limit = limit
        if remaining <= 0:
            break

    return round(charge, 2)


def calculate_bill(units, load_kw, tax_percent, subsidy, arrears):
    energy = energy_charge(units)
    fixed = math.ceil(load_kw) * FIXED_CHARGE_PER_KW
    tax = round((energy + fixed) * tax_percent / 100, 2)
    total = round(max(0, energy + fixed + tax - subsidy + arrears), 2)

    return {
        "energy_charge": energy,
        "fixed_charge": fixed,
        "tax": tax,
        "subsidy": subsidy,
        "arrears": arrears,
        "total": total,
    }


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data.get("bills", [])
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Could not read bill_history.json. Starting with an empty history.")
        return []


def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")


def create_bill(history):
    print("\nNew electricity bill")
    consumer_id = input("Consumer ID: ").strip()
    name = input("Consumer name: ").strip()
    month = input("Billing month (YYYY-MM, for example 2026-11): ").strip()

    if not consumer_id or not name or not month:
        print("Consumer ID, name, and billing month are required.")
        return
    try:
        parsed_month = datetime.strptime(month, "%Y-%m")
        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError
    except ValueError:
        print("Billing month must use YYYY-MM, for example 2026-11.")
        return

    previous = read_number("Previous meter reading (whole units): ")
    current = read_number("Current meter reading (whole units): ")
    if current < previous:
        print("Current reading cannot be lower than previous reading.")
        return
    if not previous.is_integer() or not current.is_integer():
        print("Meter readings must be whole numbers.")
        return

    load_kw = read_number("Connected load (kW): ", minimum=0.01)
    tax = read_number("Tax rate (%) [0]: ", default=0)
    subsidy = read_number("Subsidy credit (₹) [0]: ", default=0)
    arrears = read_number("Previous arrears (₹) [0]: ", default=0)

    units = int(current - previous)
    charges = calculate_bill(units, load_kw, tax, subsidy, arrears)
    today = date.today()
    due_date = today + timedelta(days=DUE_DAYS)

    bill = {
        "consumer_id": consumer_id,
        "name": name,
        "month": month,
        "units": units,
        "bill_date": today.isoformat(),
        "due_date": due_date.isoformat(),
        **charges,
    }

    print("\n------ KPDCL Electricity Bill ------")
    print(f"Consumer: {name} ({consumer_id})")
    print(f"Billing month: {month}")
    print(f"Units used: {units}")
    print(f"Energy charge: ₹{charges['energy_charge']:.2f}")
    print(f"Fixed charge: ₹{charges['fixed_charge']:.2f}")
    print(f"Tax: ₹{charges['tax']:.2f}")
    print(f"Subsidy: -₹{charges['subsidy']:.2f}")
    print(f"Previous arrears: ₹{charges['arrears']:.2f}")
    print(f"TOTAL PAYABLE: ₹{charges['total']:.2f}")
    print(f"Due date: {due_date.strftime('%d %b %Y')}")
    print("------------------------------------")

    history.append(bill)
    save_history(history)
    print("Bill saved to bill_history.json.")


def show_history(history):
    if not history:
        print("\nNo bill history yet.")
        return

    print("\nBill history")
    for bill in history:
        month = bill.get("month", bill.get("billing_month", "unknown"))
        consumer_id = bill.get("consumer_id", "unknown")
        name = bill.get("name", bill.get("consumer_name", "unknown"))
        units = bill.get("units", bill.get("consumption_kwh", 0))
        total = bill.get("total", bill.get("total_payable", 0))
        due_date = bill.get("due_date", bill.get("due_on", "unknown"))
        print(
            f"{month} | {consumer_id} | {name} | "
            f"{units} units | ₹{float(total):.2f} | due {due_date}"
        )

def main():
    history = load_history()

    while True:
        print("\nKPDCL Electricity Billing")
        print("1. Create bill")
        print("2. View bill history")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_bill(history)
        elif choice == "2":
            show_history(history)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()



