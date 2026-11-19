import codecs

admin_content = '''import React, { useState, useEffect } from "react";
import { Icon, Text, Button, StatusBadge } from "../components/ui";
import { fetchProjects } from "../api";

export default function Admin({ onNavigate, page }: { onNavigate: (p: string) => void, page: string }) {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    fetchProjects()
      .then(setProjects)
      .catch((err) => setError(err.message || "Failed to load projects"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="page-shell">
      <div className="page-head">
        <div>
          <Text as="title">Admin Dashboard</Text>
          <Text className="muted">Manage projects and master data.</Text>
        </div>
        <Button onClick={() => onNavigate("project-form")} icon="plus">Add Project</Button>
      </div>

      <div className="content-card">
        <Text as="subtitle">Project Management</Text>
        {loading ? (
          <Text>Loading projects...</Text>
        ) : error ? (
           <div className="error-state"><Text as="subtitle">Service Unavailable</Text><Text>{error}</Text></div>
        ) : (
          <table className="admin-table" style={{ width: '100%', textAlign: 'left', marginTop: '16px' }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p) => (
                <tr key={p.ProjectID}>
                  <td>{p.ProjectID}</td>
                  <td>{p.Title}</td>
                  <td><StatusBadge status={p.StatusName || p.Status} /></td>
                  <td>
                    <Button kind="ghost" size="sm" onClick={() => onNavigate(`details-${p.ProjectID}`)}>View</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </main>
  );
}
'''

form_content = '''import React, { useState, useEffect } from "react";
import { Icon, Text, Button, Input } from "../components/ui";
import { fetchProjectTypes, fetchProjectStatuses, fetchDepartments, createProject } from "../api";

export default function ProjectForm({ onNavigate }: { onNavigate: (p: string) => void }) {
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [types, setTypes] = useState<any[]>([]);
  const [statuses, setStatuses] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);

  const [form, setForm] = useState({
    Title: "",
    Description: "",
    AcademicYear: "2024",
    ProjectTypeID: 1,
    StatusID: 1,
    StudentID: 1,
    DepartmentID: 1
  });

  useEffect(() => {
    Promise.all([
      fetchProjectTypes(),
      fetchProjectStatuses(),
      fetchDepartments()
    ])
    .then(([t, s, d]) => {
      setTypes(t);
      setStatuses(s);
      setDepartments(d);
      setLoading(false);
    })
    .catch((err) => {
      setError(err.message || "Failed to load form data");
      setLoading(false);
    });
  }, []);

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      setError("");
      const res = await createProject(form);
      onNavigate(`details-${res.ProjectID}`);
    } catch (err: any) {
      setError(err.message || "Failed to create project");
      setSubmitting(false);
    }
  };

  if (loading) return <main className="page-shell"><Text>Loading form...</Text></main>;

  return (
    <main className="page-shell">
      <div className="page-head">
        <div>
          <Text as="title">Add Project</Text>
        </div>
      </div>
      
      <div className="content-card" style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '600px' }}>
        {error && <div className="error-state"><Text>{error}</Text></div>}
        
        <Input value={form.Title} onChange={(v) => setForm({...form, Title: v})} placeholder="Project Title" label="Title" />
        
        <textarea 
          value={form.Description} 
          onChange={(e) => setForm({...form, Description: e.target.value})} 
          placeholder="Project Description" 
          style={{ width: '100%', minHeight: '100px', padding: '8px' }}
        />
        
        <Input value={form.AcademicYear} onChange={(v) => setForm({...form, AcademicYear: v})} placeholder="Academic Year (e.g. 2024)" label="Academic Year" />
        
        <div>
          <Text as="label">Project Type</Text>
          <select onChange={(e) => setForm({...form, ProjectTypeID: parseInt(e.target.value)})} style={{ width: '100%', padding: '8px' }}>
            {types.map(t => <option key={t.ProjectTypeID} value={t.ProjectTypeID}>{t.TypeName}</option>)}
          </select>
        </div>

        <div>
          <Text as="label">Department</Text>
          <select onChange={(e) => setForm({...form, DepartmentID: parseInt(e.target.value)})} style={{ width: '100%', padding: '8px' }}>
            {departments.map(d => <option key={d.DepartmentID} value={d.DepartmentID}>{d.DepartmentName}</option>)}
          </select>
        </div>
        
        <div>
          <Text as="label">Status</Text>
          <select onChange={(e) => setForm({...form, StatusID: parseInt(e.target.value)})} style={{ width: '100%', padding: '8px' }}>
            {statuses.map(s => <option key={s.StatusID} value={s.StatusID}>{s.StatusName}</option>)}
          </select>
        </div>
        
        <Button onClick={handleSubmit}>{submitting ? "Saving..." : "Create Project"}</Button>
      </div>
    </main>
  );
}
'''

with codecs.open('frontend/src/pages/Admin.tsx', 'w', 'utf-8') as f:
    f.write(admin_content)

with codecs.open('frontend/src/pages/ProjectForm.tsx', 'w', 'utf-8') as f:
    f.write(form_content)
