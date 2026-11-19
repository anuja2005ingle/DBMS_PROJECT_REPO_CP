import codecs
with codecs.open('frontend/src/api/index.ts', 'r', 'utf-8') as f:
    content = f.read()

old = '''export async function fetchStudents() {
  return getJson<any[]>(apiRoutes.base + '/students');
}
export async function fetchFaculty() {
  return getJson<any[]>(apiRoutes.base + '/faculty');
}'''
new = '''export async function fetchStudents() {
  const base = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
  return getJson<any[]>(base + '/students');
}
export async function fetchFaculty() {
  const base = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
  return getJson<any[]>(base + '/faculty');
}'''
content = content.replace(old, new)
with codecs.open('frontend/src/api/index.ts', 'w', 'utf-8') as f:
    f.write(content)
