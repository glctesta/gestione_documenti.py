"""One-shot script to inspect the RMA Excel file columns - output to file."""
import pandas as pd

fp = r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\rma\Elenco schede EVOCA_ELECTROLUX 01012021_11032026.xls"
out = r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\rma\_columns.txt"

df = pd.read_excel(fp, engine="xlrd", nrows=3)

lines = []
for i, col in enumerate(df.columns):
    letter = ""
    n = i
    while True:
        letter = chr(65 + n % 26) + letter
        n = n // 26 - 1
        if n < 0:
            break
    sample = str(df.iloc[0, i]) if pd.notna(df.iloc[0, i]) else "(empty)"
    if len(sample) > 80:
        sample = sample[:80] + "..."
    lines.append(f"{letter:>3} (col {i:>2}): {col:<45} | {sample}")

lines.append(f"\nTotal columns: {len(df.columns)}")
df_full = pd.read_excel(fp, engine="xlrd", usecols=[0])
lines.append(f"Total rows: {len(df_full)}")

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Written to {out}")
