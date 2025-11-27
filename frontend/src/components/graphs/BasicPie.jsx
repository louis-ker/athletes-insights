// import { PieChart } from '@mui/x-charts/PieChart';

// export default function BasicPie({ className }) {
//   return (
//     <div className={`chatbot-container ${className || ''}`}>
//       <PieChart
//         series={[
//           {
//             data: [
//               { id: 0, value: 10, label: 'series A' },
//               { id: 1, value: 15, label: 'series B' },
//               { id: 2, value: 20, label: 'series C' },
//             ],
//           },
//         ]}
//         width={200}
//         height={200}
//       />
//     </div>
//   );
// }

import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';

export default function BasicPie({ className }) {
  const containerRef = React.useRef(null);
  const [size, setSize] = React.useState(200); // taille par défaut

  React.useEffect(() => {
    if (!containerRef.current || typeof ResizeObserver === 'undefined') return;

    const observer = new ResizeObserver(([entry]) => {
      if (!entry) return;
      const { width, height } = entry.contentRect;
      if (width > 0 && height > 0) {
        const minSide = Math.min(width, height);
        setSize(Math.max(minSide, 120)); // on garde une taille mini pour rester lisible
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
        height: '100%',          // 🟢 prend toute la place du container (50vh / 100vh)
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <PieChart
        series={[
          {
            data: [
              { id: 0, value: 10, label: 'series A' },
              { id: 1, value: 15, label: 'series B' },
              { id: 2, value: 20, label: 'series C' },
            ],
          },
        ]}
        width={size}
        height={size}
      />
    </div>
  );
}
