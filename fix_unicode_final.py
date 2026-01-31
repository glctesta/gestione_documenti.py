# -*- coding: utf-8 -*-
"""Final script to fix remaining corrupted UTF-8 checkbox characters"""

# Read the file as binary
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'rb') as f:
    data = f.read()

print("Applying final replacements...")

# Remaining corrupted byte sequences
final_replacements = [
    # Label code status - checkmark
    (b"self.label_code_status_label.config(text='\xc3\xa2\xc5\x93\xe2\x9c\x93'", 
     b"self.label_code_status_label.config(text='OK'"),
    
    # Label code status - X mark
    (b"self.label_code_status_label.config(text='\xc3\xa2\xc5\x93\xe2\x9c\x97'", 
     b"self.label_code_status_label.config(text='X'"),
    
    # Heading
    (b"self.checklist_tree.heading('#0', text='\xc3\xa2\xc5\x93\xe2\x9c\x93')", 
     b"self.checklist_tree.heading('#0', text='Check')"),
    
    # Document indicator in values
    (b"'\xc3\xa2\xc5\x93\xe2\x9c\x93' if task.Doc else ''", 
     b"'X' if task.Doc else ''"),
    
    # Toggle symbol - checked box
    (b"new_symbol = '\xc3\xa2\xcb\x9c\xc2\x91' if check_item['checked'] else '[ ]'", 
     b"new_symbol = '[X]' if check_item['checked'] else '[ ]'"),
]

for old_bytes, new_bytes in final_replacements:
    count = data.count(old_bytes)
    if count > 0:
        print(f"Replacing ({count} occurrences)")
        data = data.replace(old_bytes, new_bytes)
    else:
        print(f"Not found (may already be fixed)")

# Write the file back
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'wb') as f:
    f.write(data)

print("\nAll replacements completed!")
print("File should now display checkboxes correctly")
