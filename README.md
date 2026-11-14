# Basic KPDCL Electricity Billing System

A simple Python command-line project for creating electricity bills and viewing saved bill history.

## Run it

Open PowerShell in this folder and run:

    py billing_system.py

Choose 1 to create a bill, 2 to view history, or 3 to exit. Bills are saved in bill_history.json.

## Bill calculation

The example uses progressive domestic energy rates:

- First 200 units: ₹2.45 per unit
- Next 200 units: ₹4.20 per unit
- Above 400 units: ₹4.60 per unit
- Fixed charge: ₹10 per kW (load is rounded up to a whole kW)

The program asks for tax, subsidy credit, and previous arrears. The due date is set to 15 days after the bill date.

These are example rates for the KPDCL domestic tariff period effective from September 2026 through March 2027. Change the constants near the top of billing_system.py when the tariff changes. Enter the applicable tax and subsidy for each bill.
