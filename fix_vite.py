import codecs

with codecs.open('frontend/vite.config.ts', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace("import siteConfiguration from './.figma/make/site.json'", "import siteConfiguration from './.figma/make/site.json' with { type: 'json' }")
content = content.replace("__dirname", "import.meta.dirname")
content = content.replace("port: parseInt(process.env.PORT || '8443')", "port: parseInt(process.env.PORT || '5173')")

with codecs.open('frontend/vite.config.ts', 'w', 'utf-8') as f:
    f.write(content)
