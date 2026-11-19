import urllib.request
import urllib.error
import json
import pymysql

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Ingle@2005',
    'database': 'college_projects'
}

def post_json(url, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    try:
        res = urllib.request.urlopen(req)
        return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body.decode('utf-8')

def get_json(url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers, method='GET')
    res = urllib.request.urlopen(req)
    return res.status, json.loads(res.read())

print("=== STARTING FULL END-TO-END VERIFICATION ===")

created_project_ids = []

# Test 1 & 2 & 3: Submit project with new student details, verify in MySQL
print("\n--- Test 2 & 3: Submit project with new student details ---")
payload_1 = {
    "Title": "Autonomous Quadcopter Navigation",
    "Description": "Precision GPS-denied navigation for aerial drones using sensor fusion.",
    "AcademicYear": "2024-25",
    "ProjectTypeID": 1,
    "StatusID": 1,
    "DepartmentID": 1,
    "StudentDetails": [
        {
            "FullName": "Rohan Sharma",
            "RollNumber": "2024CS099",
            "Email": "rohan.sharma@college.edu",
            "DepartmentID": 1
        }
    ],
    "Mentors": ["Dr. Alan Turing"], # Existing mentor by name
    "Domains": [1], # IoT & Automation
    "Tags": ["theft", "aerial-drone"], # 1 existing tag ('theft'), 1 new tag ('aerial-drone')
    "Technologies": ["Python", "ROS2"] # 1 existing tech ('Python'), 1 new tech ('ROS2')
}

status, res = post_json("http://127.0.0.1:8000/projects/", payload_1)
print(f"Submission status: {status}, Response: {res}")
assert status == 201, f"Expected 201, got {status}"
p1_id = res["ProjectID"]
created_project_ids.append(p1_id)

db = pymysql.connect(**DB_CONFIG)
db.commit()
with db.cursor(pymysql.cursors.DictCursor) as c:
    # Verify Project row
    c.execute("SELECT * FROM Project WHERE ProjectID = %s", (p1_id,))
    p_row = c.fetchone()
    print("Project in MySQL:", p_row)
    assert p_row is not None
    assert p_row["StatusID"] == 1 # Proposed

    # Verify Student row
    c.execute("SELECT * FROM Student WHERE RollNumber = '2024CS099'")
    s_row = c.fetchone()
    print("New Student in MySQL:", s_row)
    assert s_row is not None
    assert s_row["FirstName"] == "Rohan"
    assert s_row["LastName"] == "Sharma"
    assert s_row["Email"] == "rohan.sharma@college.edu"

    # Verify ProjectStudent row
    c.execute("SELECT * FROM ProjectStudent WHERE ProjectID = %s", (p1_id,))
    ps_rows = c.fetchall()
    print("ProjectStudent in MySQL:", ps_rows)
    assert len(ps_rows) == 1
    assert ps_rows[0]["StudentID"] == s_row["StudentID"]

    # Verify ProjectMentor row (Dr. Alan Turing has FacultyID 1)
    c.execute("SELECT * FROM ProjectMentor WHERE ProjectID = %s", (p1_id,))
    pm_rows = c.fetchall()
    print("ProjectMentor in MySQL:", pm_rows)
    assert len(pm_rows) == 1
    assert pm_rows[0]["FacultyID"] == 1

    # Verify Tag ('aerial-drone' created, 'theft' reused)
    c.execute("SELECT * FROM Tag WHERE TagName = 'aerial-drone'")
    tag_row = c.fetchone()
    print("New Tag 'aerial-drone' in MySQL:", tag_row)
    assert tag_row is not None

    c.execute("SELECT t.TagName FROM ProjectTag pt JOIN Tag t ON pt.TagID = t.TagID WHERE pt.ProjectID = %s", (p1_id,))
    pt_rows = c.fetchall()
    print("ProjectTags in MySQL:", pt_rows)
    pt_names = [r["TagName"] for r in pt_rows]
    assert "theft" in pt_names
    assert "aerial-drone" in pt_names

    # Verify Technology ('ROS2' created, 'Python' reused)
    c.execute("SELECT * FROM Technology WHERE TechName = 'ROS2'")
    tech_row = c.fetchone()
    print("New Tech 'ROS2' in MySQL:", tech_row)
    assert tech_row is not None

    c.execute("SELECT tc.TechName FROM ProjectTechnology pt JOIN Technology tc ON pt.TechID = tc.TechID WHERE pt.ProjectID = %s", (p1_id,))
    ptech_rows = c.fetchall()
    print("ProjectTechnologies in MySQL:", ptech_rows)
    ptech_names = [r["TechName"] for r in ptech_rows]
    assert "Python" in ptech_names
    assert "ROS2" in ptech_names

print("--> Test 2 & 3 PASSED!")

# Test 4: Submit a project using an existing student and verify NO duplicate student record is created
print("\n--- Test 4: Submit project using existing student (Rohan Sharma) ---")
payload_2 = {
    "Title": "Smart Agriculture Quadcopter",
    "Description": "Drone surveying crop health using multispectral cameras.",
    "AcademicYear": "2024-25",
    "ProjectTypeID": 2,
    "StatusID": 1,
    "DepartmentID": 1,
    "StudentDetails": [
        {
            "FullName": "Rohan Sharma",
            "RollNumber": "2024CS099",
            "Email": "rohan.sharma@college.edu",
            "DepartmentID": 1
        }
    ],
    "Mentors": [1], # Dr. Alan Turing by ID
    "Domains": [5], # Agriculture Technology
    "Tags": ["aerial-drone"],
    "Technologies": ["Python"]
}

status, res = post_json("http://127.0.0.1:8000/projects/", payload_2)
print(f"Submission status: {status}, Response: {res}")
assert status == 201
p2_id = res["ProjectID"]
created_project_ids.append(p2_id)

db.commit()
with db.cursor(pymysql.cursors.DictCursor) as c:
    c.execute("SELECT COUNT(*) as cnt FROM Student WHERE RollNumber = '2024CS099'")
    cnt = c.fetchone()["cnt"]
    print("Student count for 2024CS099:", cnt)
    assert cnt == 1, "Duplicate student was created!"

    c.execute("SELECT * FROM ProjectStudent WHERE ProjectID = %s", (p2_id,))
    ps_rows = c.fetchall()
    print("ProjectStudent for p2:", ps_rows)
    assert len(ps_rows) == 1
    assert ps_rows[0]["StudentID"] == s_row["StudentID"]

print("--> Test 4 PASSED!")

# Test 5 & 6 & 7: Multiple team members and unknown faculty mentor nomination
print("\n--- Test 5, 6, 7: Multiple team members & unknown mentor nomination ---")
payload_3 = {
    "Title": "Deep Learning Medical Imaging",
    "Description": "Automated tumor classification from MRI brain scans.",
    "AcademicYear": "2024-25",
    "ProjectTypeID": 3,
    "StatusID": 1,
    "DepartmentID": 2,
    "StudentDetails": [
        {
            "FullName": "Aarav Patel",
            "RollNumber": "2024AI088",
            "Email": "aarav.patel@college.edu",
            "DepartmentID": 2
        },
        {
            "FullName": "Sneha Kulkarni",
            "RollNumber": "2024AI089",
            "Email": "sneha.kulkarni@college.edu",
            "DepartmentID": 2
        }
    ],
    "Mentors": ["Dr. Grace Hopper", "Dr. Homi Bhabha"], # Grace Hopper is registered (FacultyID 2), Homi Bhabha is unknown
    "Domains": [4], # Healthcare Technology
    "Tags": ["patient tracking", "medical-ai"],
    "Technologies": ["FastAPI", "PyTorch"]
}

status, res = post_json("http://127.0.0.1:8000/projects/", payload_3)
print(f"Submission status: {status}, Response: {res}")
assert status == 201
p3_id = res["ProjectID"]
created_project_ids.append(p3_id)

db.commit()
with db.cursor(pymysql.cursors.DictCursor) as c:
    # Verify multiple team members linked
    c.execute("SELECT s.FirstName, s.LastName, s.RollNumber FROM ProjectStudent ps JOIN Student s ON ps.StudentID = s.StudentID WHERE ps.ProjectID = %s", (p3_id,))
    team = c.fetchall()
    print("Team members in MySQL for p3:", team)
    assert len(team) == 2
    team_rolls = [t["RollNumber"] for t in team]
    assert "2024AI088" in team_rolls
    assert "2024AI089" in team_rolls

    # Verify Faculty relationship: Grace Hopper (FacultyID 2)
    c.execute("SELECT * FROM ProjectMentor WHERE ProjectID = %s", (p3_id,))
    pm_rows = c.fetchall()
    print("ProjectMentor for p3:", pm_rows)
    assert len(pm_rows) == 1
    assert pm_rows[0]["FacultyID"] == 2

    # Verify unknown mentor nomination: Dr. Homi Bhabha
    c.execute("SELECT * FROM ProjectMentorNomination WHERE ProjectID = %s", (p3_id,))
    pmn_rows = c.fetchall()
    print("ProjectMentorNomination for p3:", pmn_rows)
    assert len(pmn_rows) == 1
    assert pmn_rows[0]["NominatedName"] == "Dr. Homi Bhabha"
    assert pmn_rows[0]["Status"] == "Pending"

print("--> Test 5, 6, 7 PASSED!")

# Test 8, 9, 10, 11: Case-insensitivity deduplication for Tags and Technologies
print("\n--- Test 8, 9, 10, 11: Tag & Technology Case-Insensitive Deduplication ---")
payload_4 = {
    "Title": "Cyber Threat Early Warning System",
    "Description": "Network packet inspection using signature matching.",
    "AcademicYear": "2024-25",
    "ProjectTypeID": 1,
    "StatusID": 1,
    "DepartmentID": 1,
    "StudentDetails": [
        {
            "FullName": "Rohan Sharma",
            "RollNumber": "2024CS099",
            "Email": "rohan.sharma@college.edu",
            "DepartmentID": 1
        }
    ],
    "Mentors": ["Dr. Claude Shannon"],
    "Domains": [2], # Cybersecurity
    "Tags": ["AERIAL-DRONE", "Medical-AI", "cyber-defense"], # 'aerial-drone' and 'medical-ai' exist in lowercase
    "Technologies": ["ros2", "pytorch", "Snort"] # 'ROS2' and 'PyTorch' exist with different case
}

status, res = post_json("http://127.0.0.1:8000/projects/", payload_4)
print(f"Submission status: {status}, Response: {res}")
assert status == 201
p4_id = res["ProjectID"]
created_project_ids.append(p4_id)

db.commit()
with db.cursor(pymysql.cursors.DictCursor) as c:
    # Check that no duplicate aerial-drone tag exists
    c.execute("SELECT TagID, TagName FROM Tag WHERE LOWER(TagName) = 'aerial-drone'")
    tags = c.fetchall()
    print("Tags matching 'aerial-drone':", tags)
    assert len(tags) == 1, "Duplicate tag created for different casing!"

    # Check that no duplicate ros2 tech exists
    c.execute("SELECT TechID, TechName FROM Technology WHERE LOWER(TechName) = 'ros2'")
    techs = c.fetchall()
    print("Techs matching 'ros2':", techs)
    assert len(techs) == 1, "Duplicate tech created for different casing!"

print("--> Test 8, 9, 10, 11 PASSED!")

# Test 12: Transaction rollback on invalid relationship
print("\n--- Test 12: Intentionally invalid relationship -> Transaction rollback ---")
payload_invalid = {
    "Title": "Transaction Rollback Test Project",
    "Description": "This project should fail and roll back completely.",
    "AcademicYear": "2024-25",
    "ProjectTypeID": 1,
    "StatusID": 1,
    "DepartmentID": 1,
    "StudentDetails": [
        {
            "FullName": "Rollback Test Student",
            "RollNumber": "2024FAIL999",
            "Email": "rollback.fail@college.edu",
            "DepartmentID": 1
        }
    ],
    "Domains": [999999], # Non-existent domain!
    "Tags": ["rollback-tag-should-not-exist"],
    "Technologies": ["rollback-tech-should-not-exist"]
}

status, res = post_json("http://127.0.0.1:8000/projects/", payload_invalid)
print(f"Invalid submission status: {status}, Response: {res}")
assert status == 400

db.commit()
with db.cursor(pymysql.cursors.DictCursor) as c:
    c.execute("SELECT COUNT(*) as cnt FROM Project WHERE Title = 'Transaction Rollback Test Project'")
    p_cnt = c.fetchone()["cnt"]
    print("Project row count:", p_cnt)
    assert p_cnt == 0, "Project was not rolled back!"

    c.execute("SELECT COUNT(*) as cnt FROM Student WHERE RollNumber = '2024FAIL999'")
    s_cnt = c.fetchone()["cnt"]
    print("Student row count:", s_cnt)
    assert s_cnt == 0, "Student insert was not rolled back!"

    c.execute("SELECT COUNT(*) as cnt FROM Tag WHERE TagName = 'rollback-tag-should-not-exist'")
    t_cnt = c.fetchone()["cnt"]
    print("Tag row count:", t_cnt)
    assert t_cnt == 0, "Tag insert was not rolled back!"

    c.execute("SELECT COUNT(*) as cnt FROM Technology WHERE TechName = 'rollback-tech-should-not-exist'")
    tc_cnt = c.fetchone()["cnt"]
    print("Tech row count:", tc_cnt)
    assert tc_cnt == 0, "Tech insert was not rolled back!"

print("--> Test 12 PASSED (Transaction completely rolled back)!")

# Test 13: Project Details view verification (checking team members and mentors display)
print("\n--- Test 13: Project Details view with team members and mentors ---")
status, details = get_json(f"http://127.0.0.1:8000/projects/{p3_id}")
print("Project 3 Details from API:", json.dumps(details, indent=2))
assert status == 200
assert "Aarav Patel" in details["TeamMembers"]
assert "Sneha Kulkarni" in details["TeamMembers"]
assert "Dr. Grace Hopper" in details["Mentors"]
assert "Dr. Homi Bhabha (Pending)" in details["Mentors"]
assert "medical-ai" in details["Tags"]
assert "PyTorch" in details["Technologies"]

print("--> Test 13 PASSED!")

# Cleanup test records
print("\n--- Cleaning up temporary test projects ---")
with db.cursor() as c:
    for pid in created_project_ids:
        c.execute("DELETE FROM ProjectStatusAudit WHERE ProjectID = %s", (pid,))
        c.execute("DELETE FROM Project WHERE ProjectID = %s", (pid,))
    # Clean up test students
    c.execute("DELETE FROM Student WHERE RollNumber IN ('2024CS099', '2024AI088', '2024AI089')")
    # Clean up test tags and techs created in tests
    c.execute("DELETE FROM Tag WHERE TagName IN ('aerial-drone', 'medical-ai', 'cyber-defense')")
    c.execute("DELETE FROM Technology WHERE TechName IN ('ROS2', 'PyTorch', 'Snort')")
db.commit()
print("Cleaned up test projects:", created_project_ids)

print("\n=== ALL WORKFLOW TESTS PASSED SUCCESSFULLY ===")
