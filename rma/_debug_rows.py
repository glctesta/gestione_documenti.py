"""Debug: mostra i valori delle righe problematiche."""
import pandas as pd
import os, sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

fp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "Elenco schede EVOCA_ELECTROLUX 01012021_11032026.xls")

df = pd.read_excel(fp, engine="xlrd")

# Check rows 6 and 8 (0-indexed) — the problematic ones
for ridx in [6, 8]:
    print(f"\n--- Row {ridx} ---")
    cols_to_check = {
        "G (serial)": 6, "H (cust_part)": 7, "I (prod_code)": 8,
        "J (prod_week)": 9, "L (fault_desc)": 11, "R (fault_code)": 17,
        "S (fault_cause)": 18, "T (part_desc)": 19, "U (warranty)": 20,
        "AA (cust_id)": 26, "AB (cust_name)": 27, "AC (part_code)": 28,
        "AH (reference)": 33, "AI (fault_type)": 34, "AJ (fault_detail)": 35,
        "AK (fault_notes)": 36, "AL (fault_type_code)": 37,
        "AM (fault_detail_code)": 38, "AN (assembly)": 39,
    }
    for label, cidx in cols_to_check.items():
        val = df.iloc[ridx, cidx]
        print(f"  {label}: {repr(val)} (type={type(val).__name__})")

# Also check how many rows have NaN in CustomerId
na_count = df.iloc[:, 26].isna().sum()
print(f"\nCustomerId (AA) NaN count: {na_count}/{len(df)}")
