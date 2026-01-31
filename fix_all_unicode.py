# -*- coding: utf-8 -*-
"""Complete fix for ALL remaining corrupted UTF-8 characters"""

# Read the file as binary
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'rb') as f:
    data = f.read()

print("Applying COMPLETE fix for all remaining characters...")

# ALL corrupted byte sequences - comprehensive list
all_replacements = [
    # Label code status lines 542, 545
    (b".config(text='\xc3\xa2\xc5\x93\xe2\x9c\x93'", b".config(text='OK'"),
    (b".config(text='\xc3\xa2\xc5\x93\xe2\x9c\x97'", b".config(text='X'"),
    
    # Heading line 679
    (b".heading('#0', text='\xc3\xa2\xc5\x93\xe2\x9c\x93')", b".heading('#0', text='Check')"),
    
    # Document indicator lines 748, 769
    (b"'\xc3\xa2\xc5\x93\xe2\x9c\x93' if task.Doc else ''", b"'X' if task.Doc else ''"),
    
    # Toggle symbol line 791
    (b"new_symbol = '\xc3\xa2\xcb\x9c\xc2\x91' if check_item", b"new_symbol = '[X]' if check_item"),
]

total_replacements = 0
for old_bytes, new_bytes in all_replacements:
    count = data.count(old_bytes)
    if count > 0:
        print(f"  Replacing {count} occurrence(s)")
        data = data.replace(old_bytes, new_bytes)
        total_replacements += count

# Write the file back
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'wb') as f:
    f.write(data)

print(f"\nCompleted! Total replacements: {total_replacements}")
print("All Unicode characters should now be fixed.")
print("\nPlease restart the application to see the changes.")
