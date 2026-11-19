import codecs
with codecs.open('frontend/src/components/ui.tsx', 'r', 'utf-8') as f:
    content = f.read()

new_card = '''export function ProjectCard({ project, onView }: { project: any; onView: () => void }) {
  return <div className="project-card">
    <div className="card-top"><div className="project-id">{project.ProjectID || project.id}</div><StatusBadge status={project.Status || project.status}/></div>
    <Text as="subtitle" className="project-title">{project.Title || project.title}</Text>
    {project.description && <Text className="muted card-description">{project.description}</Text>}
    <div className="meta-row"><span><Icon name="calendar" size="sm"/>{project.AcademicYear || project.year}</span><span><Icon name="folder" size="sm"/>{project.ProjectType || project.type}</span></div>
    {(project.domains || project.technologies) && <div className="taxonomy">
      {project.domains && <div><span className="taxonomy-label">Domains</span><span className="chip-row">{project.domains.map((item: string) => <Chip key={item} tone="blue">{item}</Chip>)}</span></div>}
      {project.technologies && <div><span className="taxonomy-label">Technologies</span><span className="chip-row">{project.technologies.slice(0, 3).map((item: string) => <Chip key={item} tone="teal">{item}</Chip>)}</span></div>}
    </div>}
    <div className="card-footer"><span className="match-note"><Icon name="check" size="sm"/> Structured match</span><Button kind="ghost" onClick={onView}>View details <Icon name="arrow" size="sm"/></Button></div>
  </div>;
}'''

import re
content = re.sub(r'export function ProjectCard.*?</Button></div>\n  </div>;\n\}', new_card, content, flags=re.DOTALL)
with codecs.open('frontend/src/components/ui.tsx', 'w', 'utf-8') as f:
    f.write(content)
