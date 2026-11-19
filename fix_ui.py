import codecs
with codecs.open('frontend/src/components/ui.tsx', 'r', 'utf-8') as f:
    content = f.read()

index = content.find('export function EmptyState')
clean_content = content[:index]

empty_state = '''export function EmptyState({ onClear, message }: { onClear: () => void; message?: string }) {
  return <div className="state-card"><span className="state-icon"><Icon name="search" size="lg"/></span><Text as="subtitle">{message || "No projects found"}</Text><Text className="muted">Try a different keyword or remove some filters to broaden your search.</Text><Button kind="secondary" onClick={onClear}>Clear search & filters</Button></div>;
}'''

project_card = '''export function ProjectCard({ project, onView }: { project: any; onView: () => void }) {
  return <div className="project-card">
    <div className="card-top"><div className="project-id">{project.ProjectID || project.id}</div><StatusBadge status={project.StatusName || project.Status || project.status || "Unknown"}/></div>
    <Text as="subtitle" className="project-title">{project.Title || project.title}</Text>
    {project.description && <Text className="muted card-description">{project.description}</Text>}
    <div className="meta-row"><span><Icon name="calendar" size="sm"/>{project.AcademicYear || project.year}</span><span><Icon name="folder" size="sm"/>{project.ProjectType || project.type || project.TypeName}</span></div>
    {(project.domains || project.technologies) && <div className="taxonomy">
      {project.domains && <div><span className="taxonomy-label">Domains</span><span className="chip-row">{project.domains.map((item: string) => <Chip key={item} tone="blue">{item}</Chip>)}</span></div>}
      {project.technologies && <div><span className="taxonomy-label">Technologies</span><span className="chip-row">{project.technologies.slice(0, 3).map((item: string) => <Chip key={item} tone="teal">{item}</Chip>)}</span></div>}
    </div>}
    <div className="card-footer"><span className="match-note"><Icon name="check" size="sm"/> Structured match</span><Button kind="ghost" onClick={onView}>View details <Icon name="arrow" size="sm"/></Button></div>
  </div>;
}'''

with codecs.open('frontend/src/components/ui.tsx', 'w', 'utf-8') as f:
    f.write(clean_content + '\n' + empty_state + '\n\n' + project_card + '\n')
