import re
import codecs

with codecs.open('frontend/src/App_backup.tsx', 'r', 'utf-16') as f:
    content = f.read()

# Make sure we don't grab everything until the very end. We use a more careful matcher.
# Let's extract the types first
types_match = re.search(r'type Page =.*?;', content, re.DOTALL)
role_match = re.search(r'type Role =.*?;', content, re.DOTALL)
icon_match = re.search(r'type IconName =.*?;', content, re.DOTALL)

types = (types_match.group(0) if types_match else '') + '\n' + (role_match.group(0) if role_match else '') + '\n' + (icon_match.group(0) if icon_match else '') + '\n'

ui_funcs = ['Icon', 'Text', 'Button', 'Input', 'Chip', 'StatusBadge', 'Logo', 'SearchBox', 'EmptyState', 'ProjectCard']
ui_blocks = []

for func in ui_funcs:
    # Match the function block by counting braces
    pattern = r'function ' + func + r'\s*\(.*?\)\s*\{'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        continue
    
    start_idx = match.end()
    brace_count = 1
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:]):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        if brace_count == 0:
            end_idx = start_idx + i + 1
            break
            
    ui_blocks.append('export ' + content[match.start():end_idx])

with codecs.open('frontend/src/components/ui.tsx', 'w', 'utf-8') as f:
    f.write('import React, { createElement, KeyboardEvent, ReactNode } from "react";\n\n' + types + '\n\n' + '\n\n'.join(ui_blocks))
print('Success')
