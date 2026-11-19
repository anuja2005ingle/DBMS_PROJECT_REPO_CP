import codecs

with codecs.open('frontend/src/pages/Discover.tsx', 'r', 'utf-8') as f:
    content = f.read()

# Update loadProjects payload
payload_old = '''const data = await fetchProjects({
        keyword: searchParams.get("keyword") || undefined,
        academic_year: searchParams.get("academic_year") || undefined,
        domain_id: searchParams.get("domain_id") ? parseInt(searchParams.get("domain_id")!) : undefined,
      });'''

payload_new = '''const data = await fetchProjects({
        keyword: searchParams.get("keyword") || undefined,
        academic_year: searchParams.get("academic_year") || undefined,
        domain_id: searchParams.get("domain_id") ? parseInt(searchParams.get("domain_id")!) : undefined,
        project_type_id: searchParams.get("project_type_id") ? parseInt(searchParams.get("project_type_id")!) : undefined,
        department_id: searchParams.get("department_id") ? parseInt(searchParams.get("department_id")!) : undefined,
        tech_id: searchParams.get("tech_id") ? parseInt(searchParams.get("tech_id")!) : undefined,
        tag_id: searchParams.get("tag_id") ? parseInt(searchParams.get("tag_id")!) : undefined,
      });'''
      
content = content.replace(payload_old, payload_new)

# Update applyFilters to accept new params
apply_old = '''  const applyFilters = (filters: any) => {
    setFiltersOpen(false);
    const newParams = new URLSearchParams(searchParams);
    if (filters.academic_year) newParams.set("academic_year", filters.academic_year);
    else newParams.delete("academic_year");
    
    if (filters.domain_id) newParams.set("domain_id", filters.domain_id);
    else newParams.delete("domain_id");
    
    setSearchParams(newParams);
  };'''

apply_new = '''  const applyFilters = (filters: any) => {
    setFiltersOpen(false);
    const newParams = new URLSearchParams(searchParams);
    const keys = ["academic_year", "domain_id", "project_type_id", "department_id", "tech_id", "tag_id"];
    keys.forEach(k => {
      if (filters[k]) newParams.set(k, filters[k]);
      else newParams.delete(k);
    });
    setSearchParams(newParams);
  };'''

content = content.replace(apply_old, apply_new)

# Add clear filters function handling
clear_old = '''  const clearSearch = () => {
    setDraft("");
    const newParams = new URLSearchParams(searchParams);
    newParams.delete("keyword");
    setSearchParams(newParams);
  };'''

clear_new = '''  const clearSearch = () => {
    setDraft("");
    setSearchParams(new URLSearchParams());
  };'''

content = content.replace(clear_old, clear_new)

# Update active chips
chips_old = '''          <div className="active-filters">
            <span>Active filters:</span>
            {academicYear && <Chip tone="blue" removable>{academicYear}</Chip>}
            {domainId && <Chip tone="blue" removable>Domain ID: {domainId}</Chip>}
            {query && <Chip tone="purple" removable>Search: {query}</Chip>}
          </div>'''

chips_new = '''          <div className="active-filters">
            <span>Active filters:</span>
            {searchParams.get("academic_year") && <Chip tone="blue" removable>Year: {searchParams.get("academic_year")}</Chip>}
            {searchParams.get("domain_id") && <Chip tone="blue" removable>Domain: {searchParams.get("domain_id")}</Chip>}
            {searchParams.get("project_type_id") && <Chip tone="blue" removable>Type: {searchParams.get("project_type_id")}</Chip>}
            {searchParams.get("department_id") && <Chip tone="blue" removable>Dept: {searchParams.get("department_id")}</Chip>}
            {searchParams.get("tech_id") && <Chip tone="blue" removable>Tech: {searchParams.get("tech_id")}</Chip>}
            {searchParams.get("tag_id") && <Chip tone="blue" removable>Tag: {searchParams.get("tag_id")}</Chip>}
            {query && <Chip tone="purple" removable>Search: {query}</Chip>}
          </div>'''

content = content.replace(chips_old, chips_new)

with codecs.open('frontend/src/pages/Discover.tsx', 'w', 'utf-8') as f:
    f.write(content)
