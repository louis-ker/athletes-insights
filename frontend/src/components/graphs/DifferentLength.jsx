import * as React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';

export default function DifferentLength({ className }) {
  const containerRef = React.useRef(null);
  const [chartHeight, setChartHeight] = React.useState(200); // valeur par défaut

  React.useEffect(() => {
    if (!containerRef.current || typeof ResizeObserver === 'undefined') return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const h = entries[0].contentRect.height;
        if (h > 0) {
          setChartHeight(h);
        }
      }
    });

    observer.observe(containerRef.current);

    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={containerRef}
      className={`chatbot-container ${className || ''}`}
      style={{
        width: '100%',
        height: '100%',   // prend toute la place du container (50vh / 100vh)
      }}
    >
      <LineChart
        xAxis={[{ data: [1, 2, 3, 5, 8, 10, 12, 15, 16] }]}
        series={[
          {
            data: [2, 5.5, 2, 8.5, 1.5, 5],
            valueFormatter: (value) => (value == null ? 'NaN' : value.toString()),
          },
          {
            data: [null, null, null, null, 5.5, 2, 8.5, 1.5, 5],
          },
          {
            data: [7, 8, 5, 4, null, null, 2, 5.5, 1],
            valueFormatter: (value) => (value == null ? '?' : value.toString()),
          },
        ]}
        // on utilise la hauteur réelle du container
        height={Math.max(chartHeight, 120)}  // min 120 pour éviter graph minuscule
        margin={{ bottom: 10 }}
      />
    </div>
  );
}
