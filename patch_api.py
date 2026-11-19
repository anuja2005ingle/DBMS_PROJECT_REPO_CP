import codecs
with codecs.open('frontend/src/api/index.ts', 'r', 'utf-8') as f:
    content = f.read()

api_old = '''export async function fetchProjects(params: {
  keyword?: string;
  academic_year?: string;
  project_type_id?: number;
  department_id?: number;
  domain_id?: number;
} = {}) {
  const urlParams = new URLSearchParams();
  if (params.keyword) urlParams.append('keyword', params.keyword);
  if (params.academic_year) urlParams.append('academic_year', params.academic_year);
  if (params.project_type_id) urlParams.append('project_type_id', params.project_type_id.toString());
  if (params.department_id) urlParams.append('department_id', params.department_id.toString());
  if (params.domain_id) urlParams.append('domain_id', params.domain_id.toString());'''

api_new = '''export async function fetchProjects(params: {
  keyword?: string;
  academic_year?: string;
  project_type_id?: number;
  department_id?: number;
  domain_id?: number;
  tech_id?: number;
  tag_id?: number;
} = {}) {
  const urlParams = new URLSearchParams();
  if (params.keyword) urlParams.append('keyword', params.keyword);
  if (params.academic_year) urlParams.append('academic_year', params.academic_year);
  if (params.project_type_id) urlParams.append('project_type_id', params.project_type_id.toString());
  if (params.department_id) urlParams.append('department_id', params.department_id.toString());
  if (params.domain_id) urlParams.append('domain_id', params.domain_id.toString());
  if (params.tech_id) urlParams.append('tech_id', params.tech_id.toString());
  if (params.tag_id) urlParams.append('tag_id', params.tag_id.toString());'''

content = content.replace(api_old, api_new)

with codecs.open('frontend/src/api/index.ts', 'w', 'utf-8') as f:
    f.write(content)
