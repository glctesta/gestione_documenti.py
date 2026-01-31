# Fix line 791 - checkbox toggle symbol
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'rb') as f:
    data = f.read()

# The exact corrupted sequence on line 791
# new_symbol = '[corrupted]' if check_item['checked'] else '[ ]'
# We need to replace the corrupted part with [X]

# Replace the entire line pattern to be safe
old_line = b"new_symbol = '\xc3\xa2\xcb\x9c\xc2\x91' if check_item['checked'] else '[ ]'"
new_line = b"new_symbol = '[X]' if check_item['checked'] else '[ ]'"

if old_line in data:
    data = data.replace(old_line, new_line)
    print("Fixed line 791 - checkbox toggle")
else:
    # Try alternative pattern
    print("Trying alternative pattern...")
    # Just replace any remaining corrupted checkbox character
    data = data.replace(b"= '\xc3\xa2\xcb\x9c\xc2\x91' if", b"= '[X]' if")
    print("Applied alternative fix")

with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\product_checks_gui.py', 'wb') as f:
    f.write(data)

print("Done! Checkbox toggle should now work correctly.")
