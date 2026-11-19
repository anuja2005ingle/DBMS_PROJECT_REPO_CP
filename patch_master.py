import codecs
with codecs.open('backend/app/routers/master_data.py', 'a', 'utf-8') as f:
    f.write('''
@router.get("/students", response_model=List[MasterEntity])
def get_students(db: pymysql.connections.Connection = Depends(get_db_connection)):
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT StudentID as id, CONCAT(FirstName, ' ', LastName) as name FROM Student ORDER BY name")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve students")

@router.get("/faculty", response_model=List[MasterEntity])
def get_faculty(db: pymysql.connections.Connection = Depends(get_db_connection)):
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT FacultyID as id, CONCAT(FirstName, ' ', LastName) as name FROM Faculty ORDER BY name")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve faculty")
''')
