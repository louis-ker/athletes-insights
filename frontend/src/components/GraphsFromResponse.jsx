import React from 'react';
import DynamicGraphRenderer from './DynamicGraphRenderer';
import athletes from './../../../backend/rag-article-generator/data/tables/athletes_500m_full_noNull_ordered.json';

export default function GraphsFromResponse({ responseData }) {
  const graphs = responseData?.graphs || {};
  const entries = Object.entries(graphs);

  if (!entries.length) {
    return <em></em>;
    }

  // on limite à 50 lignes comme demandé côté prompt
  const data = Array.isArray(athletes) ? athletes.slice(0, 50) : [];

  return (
    <div>
      {entries.map(([partKey, meta]) => {
        const title =
          responseData?.[partKey]?.title ||
          `Graphique (${partKey})`;
        return (
          <section key={partKey} style={{ marginTop: 24 }}>
            <h3 style={{ margin: '0 0 12px' }}>{title}</h3>
            <DynamicGraphRenderer jsx={meta.jsx} data={data} />
          </section>
        );
      })}
    </div>
  );
}
