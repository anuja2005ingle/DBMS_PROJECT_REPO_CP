import requests

BASE = "http://127.0.0.1:8000"

users = [
    {"Email": "admin@college.edu", "Password": "admin", "RoleID": 3},
    {"Email": "dr.rao@college.edu", "Password": "faculty", "RoleID": 2, "FacultyID": 1},
    {"Email": "anuja@student.edu", "Password": "student", "RoleID": 1, "StudentID": 1}
]

for u in users:
    try:
        r = requests.post(f"{BASE}/auth/register", json=u)
        print(f"Registered {u['Email']}: {r.status_code} {r.text}")
    except Exception as e:
        print(e)
