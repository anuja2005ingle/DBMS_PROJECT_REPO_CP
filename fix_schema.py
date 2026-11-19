import codecs

with codecs.open('database/views.sql', 'r', 'utf-8') as f:
    views_sql = f.read()

dep_query = """    (
        SELECT GROUP_CONCAT(d.DepartmentName SEPARATOR ', ')
        FROM ProjectDepartment pd
        INNER JOIN Department d ON pd.DepartmentID = d.DepartmentID
        WHERE pd.ProjectID = p.ProjectID
    ) AS Department,"""

views_sql = views_sql.replace('    pt.TypeName,\n    ps.StatusName,', '    pt.TypeName,\n' + dep_query + '\n    ps.StatusName,')

with codecs.open('database/views.sql', 'w', 'utf-8') as f:
    f.write(views_sql)

with codecs.open('backend/app/models/schemas.py', 'r', 'utf-8') as f:
    schemas = f.read()

schemas = schemas.replace('    TypeName: str\n    StatusName: str', '    TypeName: str\n    Department: str | None = None\n    StatusName: str')

with codecs.open('backend/app/models/schemas.py', 'w', 'utf-8') as f:
    f.write(schemas)
