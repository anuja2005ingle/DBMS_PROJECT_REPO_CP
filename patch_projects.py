import codecs
with codecs.open('backend/app/routers/projects.py', 'r', 'utf-8') as f:
    content = f.read()

sig_old = '''def search_projects(
    keyword: Optional[str] = Query(None, description="The search term to look for"),
    academic_year: Optional[str] = Query(None),
    project_type_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    domain_id: Optional[int] = Query(None),
    db: pymysql.connections.Connection = Depends(get_db_connection)
):'''

sig_new = '''def search_projects(
    keyword: Optional[str] = Query(None, description="The search term to look for"),
    academic_year: Optional[str] = Query(None),
    project_type_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    domain_id: Optional[int] = Query(None),
    tech_id: Optional[int] = Query(None),
    tag_id: Optional[int] = Query(None),
    db: pymysql.connections.Connection = Depends(get_db_connection)
):'''

content = content.replace(sig_old, sig_new)

where_old = '''        if domain_id:
            where_clauses.append("""
                EXISTS (SELECT 1 FROM ProjectDomain pdom 
                        WHERE pdom.ProjectID = p.ProjectID 
                          AND pdom.DomainID = %s)
            """)
            params.append(domain_id)'''

where_new = where_old + '''
        if tech_id:
            where_clauses.append("""
                EXISTS (SELECT 1 FROM ProjectTechnology ptech 
                        WHERE ptech.ProjectID = p.ProjectID 
                          AND ptech.TechID = %s)
            """)
            params.append(tech_id)
        if tag_id:
            where_clauses.append("""
                EXISTS (SELECT 1 FROM ProjectTag ptag 
                        WHERE ptag.ProjectID = p.ProjectID 
                          AND ptag.TagID = %s)
            """)
            params.append(tag_id)'''

content = content.replace(where_old, where_new)

with codecs.open('backend/app/routers/projects.py', 'w', 'utf-8') as f:
    f.write(content)
