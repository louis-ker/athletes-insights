// import React from 'react';
// import { LiveProvider, LivePreview, LiveError } from 'react-live';
// import {
//   LineChart, BarChart, PieChart,
//   ChartsXAxis, ChartsYAxis, ChartsLegend, ChartsGrid
// } from '@mui/x-charts';

// export default function DynamicGraphRenderer({ jsx, data }) {
//   if (!jsx) return null;

//   // 1) garde-fous basiques
//   let code = String(jsx).slice(0, 20000);
//   const forbidden = [/import\s+/i, /fetch\s*\(/i, /new\s+Function\s*\(/i, /eval\s*\(/i];
//   if (forbidden.some((re) => re.test(code))) {
//     return <div style={{color:'crimson'}}>Code refusé (imports/fetch interdits).</div>;
//   }

//   // 2) si "export default function GeneratedChart" => on le rend appelable
//   //    on supprime "export default" pour l'éval, puis on appelle render(<GeneratedChart data={data} />)
//   //    (Le prompt backend impose ce nom, donc on l’assume ici)
//   code = code
//     .replace(/export\s+default\s+function\s+([A-Za-z0-9_]+)/, 'function $1')
//     .replace(/export\s+default\s*=\s*/, '') // cas "export default = () => {}"
//     .trim();

//   const scope = {
//     React,
//     LineChart, BarChart, PieChart,
//     ChartsXAxis, ChartsYAxis, ChartsLegend, ChartsGrid,
//     data,
//   };

//   const wrapped = `${code}\n\nrender(<GeneratedChart data={data} />);`;

//   return (
//     <LiveProvider code={wrapped} scope={scope} noInline>
//       <LivePreview />
//       <LiveError />
//     </LiveProvider>
//   );
// }

// src/components/DynamicGraphRenderer.jsx
import React from 'react';
import { LiveProvider, LivePreview, LiveError } from 'react-live';
import {
  // Charts
  LineChart, BarChart, PieChart, AreaChart, ScatterChart, ComposedChart, RadialBarChart, RadarChart,
  // Primitives
  Line, Bar, Pie, Area, Scatter, RadialBar, Radar, Cell,
  // Axes & helpers
  XAxis, YAxis, ZAxis, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  Tooltip, Legend, CartesianGrid, ReferenceLine, ReferenceArea, Brush, Label, LabelList,
  ResponsiveContainer,
} from 'recharts';

export default function DynamicGraphRenderer({ jsx, data }) {
  if (!jsx) return null;

  // 1) garde-fous basiques
  let code = String(jsx).slice(0, 20000);
  const forbidden = [/import\s+/i, /fetch\s*\(/i, /new\s+Function\s*\(/i, /eval\s*\(/i, /require\s*\(/i];
  if (forbidden.some((re) => re.test(code))) {
    return <div style={{ color: 'crimson' }}>Code refusé (imports/fetch/require interdits).</div>;
  }

  // 2) rendre appelable "export default function GeneratedChart(...)"
  code = code
    .replace(/export\s+default\s+function\s+([A-Za-z0-9_]+)/, 'function $1')
    .replace(/export\s+default\s*=\s*/, '')
    .trim();

  // Hooks disponibles sans import explicite
  const { useState, useMemo, useEffect } = React;

  // 3) injecter toutes les primitives Recharts dans le scope
  const scope = {
    React,
    // Hooks
    useState, useMemo, useEffect,
    // Recharts charts
    LineChart, BarChart, PieChart, AreaChart, ScatterChart, ComposedChart, RadialBarChart, RadarChart,
    // Recharts primitives
    Line, Bar, Pie, Area, Scatter, RadialBar, Radar, Cell,
    // Axes/helpers
    XAxis, YAxis, ZAxis, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    Tooltip, Legend, CartesianGrid, ReferenceLine, ReferenceArea, Brush, Label, LabelList,
    ResponsiveContainer,
    // Data injectée
    data,
  };

  const wrapped = `${code}\n\nrender(<GeneratedChart data={data} />);`;

  return (
    <LiveProvider code={wrapped} scope={scope} noInline>
      <LivePreview />
      <LiveError />
    </LiveProvider>
  );
}
