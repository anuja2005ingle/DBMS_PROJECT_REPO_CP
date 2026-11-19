import codecs

new_content = '''import React, { useState, useEffect } from "react";
import { Icon, Text, Button, Chip } from "../components/ui";
import { fetchDomains, fetchTags, fetchTechnologies } from "../api";

export default function Explore({ type, onNavigate }: { type: "domains" | "technologies" | "tags", onNavigate: (page: string) => void }) {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  useEffect(() => {
    setLoading(true);
    setError("");
    const fetcher = type === "domains" ? fetchDomains : type === "technologies" ? fetchTechnologies : fetchTags;
    fetcher()
      .then(setData)
      .catch((err) => setError(err.message || "Failed to load " + type))
      .finally(() => setLoading(false));
  }, [type]);

  return (
    <main className="page-shell">
      <div className="page-head discover-head">
        <div>
          <div className="breadcrumbs">Home <Icon name="chevron" size="sm"/> Explore {type}</div>
          <Text as="title">Explore {type.charAt(0).toUpperCase() + type.slice(1)}</Text>
        </div>
      </div>
      <div className="content-card">
        {loading ? (
          <Text>Loading {type}...</Text>
        ) : error ? (
          <div className="error-state"><Text as="subtitle">Service Unavailable</Text><Text>{error}</Text></div>
        ) : data.length === 0 ? (
          <Text>No {type} found.</Text>
        ) : (
          <div className="chip-row" style={{ flexWrap: 'wrap', gap: '12px' }}>
            {data.map((item, i) => (
              <Chip key={i} tone={type === 'domains' ? 'blue' : type === 'technologies' ? 'teal' : 'purple'}>
                {item.DomainName || item.TechName || item.TagName || item.name}
              </Chip>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
'''

with codecs.open('frontend/src/pages/Explore.tsx', 'w', 'utf-8') as f:
    f.write(new_content)
