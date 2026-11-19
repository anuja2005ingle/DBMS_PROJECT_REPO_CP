import codecs
with codecs.open('frontend/src/pages/Admin.tsx', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace('size="sm"', '')

with codecs.open('frontend/src/pages/Admin.tsx', 'w', 'utf-8') as f:
    f.write(content)
