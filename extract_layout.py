import re
import codecs

with codecs.open('frontend/src/App_backup.tsx', 'r', 'utf-16') as f:
    content = f.read()

funcs = ['Navbar', 'Footer']
blocks = []

for func in funcs:
    pattern = r'function ' + func + r'\s*\(.*?\)\s*\{'
    match = re.search(pattern, content, re.DOTALL)
    if not match: continue
    
    start_idx = match.end()
    brace_count = 1
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:]):
        if char == '{': brace_count += 1
        elif char == '}': brace_count -= 1
        if brace_count == 0:
            end_idx = start_idx + i + 1
            break
            
    blocks.append('export default ' + content[match.start():end_idx])

with codecs.open('frontend/src/components/Navbar.tsx', 'w', 'utf-8') as f:
    f.write('import React from "react";\nimport { Link } from "react-router-dom";\nimport { Icon, Text, Logo, Button } from "./ui";\nimport { Role } from "../App";\n\n' + blocks[0].replace('onNavigate("home")', 'onNavigate("/")'))

with codecs.open('frontend/src/components/Footer.tsx', 'w', 'utf-8') as f:
    f.write('import React from "react";\nimport { Link } from "react-router-dom";\nimport { Logo, Text } from "./ui";\n\n' + blocks[1].replace('onNavigate("home")', 'onNavigate("/")'))

print('Layout extracted.')
