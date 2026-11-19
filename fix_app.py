import codecs

with codecs.open('frontend/src/App.tsx', 'r', 'utf-8') as f:
    content = f.read()

old_code = 'case "discover": path = "/discover"; break;'
new_code = '''case "discover":
        path = "/discover";
        if (params) {
          const qs = new URLSearchParams(params).toString();
          if (qs) path += "?" + qs;
        }
        break;'''

content = content.replace(old_code, new_code)

with codecs.open('frontend/src/App.tsx', 'w', 'utf-8') as f:
    f.write(content)
