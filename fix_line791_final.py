# Final comprehensive fix for line 791
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'rb') as f:
    data = f.read()

print("Analyzing line 791...")

# Find the line with new_symbol
lines = data.split(b'\r\n')
for i, line in enumerate(lines):
    if b'new_symbol =' in line and b'check_item' in line:
        print(f"Line {i+1}: {line}")
        print(f"Hex: {line.hex()}")
        
        # Replace ANY character between quotes before 'if check_item'
        # Pattern: new_symbol = '...' if check_item['checked'] else '[ ]'
        if b"if check_item['checked'] else '[ ]'" in line:
            # Replace the entire assignment
            lines[i] = b"                        new_symbol = '[X]' if check_item['checked'] else '[ ]'"
            print(f"Fixed line {i+1}")

# Rejoin and save
data = b'\r\n'.join(lines)

with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'wb') as f:
    f.write(data)

print("\nFile updated! Line 791 should now be correct.")
print("Please CLOSE and RESTART the application to see the changes.")
