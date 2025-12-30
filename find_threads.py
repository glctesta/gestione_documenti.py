
import re

with open('main.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if 'threading.Thread' in line:
            print(f"{i}: {line.strip()}")
