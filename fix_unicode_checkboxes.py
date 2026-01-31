# -*- coding: utf-8 -*-
"""Script to fix corrupted UTF-8 checkbox characters in product_checks_gui.py"""

# Read the file as binary
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'rb') as f:
    data = f.read()

print("Starting byte-level replacements...")

# These are the exact corrupted byte sequences we found
# ✓ (checkmark) appears as: â\x9c" = \xc3\xa2\xc5\x93\xe2\x9c\x93
# ✗ (X mark) appears as: â\x9c— = \xc3\xa2\xc5\x93\xe2\x9c\x97  
# ☐ (unchecked) appears as: â\x98\x90 = \xc3\xa2\xcb\x9c\xc2\x90
# ☑ (checked) appears as: â\x98' = \xc3\xa2\xcb\x9c\xc2\x91

replacements = [
    # Checkmark (✓) -> OK
    (b"text='\xc3\xa2\xc5\x93\xe2\x9c\x93'", b"text='OK'"),
    (b"config(text='\xc3\xa2\xc5\x93\xe2\x9c\x93'", b"config(text='OK'"),
    
    # X mark (✗) -> X
    (b"config(text='\xc3\xa2\xc5\x93\xe2\x9c\x97'", b"config(text='X'"),
    
    # Unchecked box (☐) -> [ ]
    (b"text='\xc3\xa2\xcb\x9c\xc2\x90'", b"text='[ ]'"),
    
    # Checked box (☑) -> [X]
    (b"text='\xc3\xa2\xcb\x9c\xc2\x91'", b"text='[X]'"),
    (b"new_symbol = '\xc3\xa2\xcb\x9c\xc2\x91'", b"new_symbol = '[X]'"),
    (b"else '\xc3\xa2\xcb\x9c\xc2\x90'", b"else '[ ]'"),
    
    # Document indicator
    (b"'\xc3\xa2\xc5\x93\xe2\x9c\x93' if task.Doc", b"'X' if task.Doc"),
    
    # Heading
    (b"heading('#0', text='\xc3\xa2\xc5\x93\xe2\x9c\x93')", b"heading('#0', text='Check')"),
]

for old_bytes, new_bytes in replacements:
    count = data.count(old_bytes)
    if count > 0:
        print(f"Replacing {old_bytes} -> {new_bytes} ({count} occurrences)")
        data = data.replace(old_bytes, new_bytes)
    else:
        print(f"Not found: {old_bytes}")

# Write the file back
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'wb') as f:
    f.write(data)

print("\nFile updated successfully!")
print("All corrupted byte sequences replaced with ASCII equivalents")
