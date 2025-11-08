// import Box from '@mui/material/Box';
// import { BarChart } from '@mui/x-charts/BarChart';
// import { createTheme, ThemeProvider } from '@mui/material/styles';

// const uData = [4000, 3000, 2000, 2780, 1890, 2390, 3490];
// const pData = [2400, 1398, 9800, 3908, 4800, 3800, 4300];
// const amtData = [2400, 2210, 2290, 2000, 2181, 2500, 2100];

// const xLabels = [
//   'Page A',
//   'Page B',
//   'Page C',
//   'Page D',
//   'Page E',
//   'Page F',
//   'Page G',
// ];

// export default function MixedBarChart() {
//   return (
//       <Box sx={{ width: '100%', height: 400 }}>
//         <BarChart
//           series={[
//             { data: pData, label: 'pv', stack: 'stack1', color: '#3f50b5' },
//             { data: amtData, label: 'amt', color: '#f44336' },
//             { data: uData, label: 'uv', stack: 'stack1', color: '#757ce8' },
//           ]}
//           xAxis={[{ data: xLabels }]}
//           yAxis={[{ width: 50 }]}
//           sx={{
//             '& .MuiChartsAxis-root text': { fill: '#ffffffff' },
//             '& .MuiChartsLegend-root': { color: '#ffffffff' },
//           }}
//         />
//       </Box>
//   );
// }

// MixedBarChart.jsx
import Box from '@mui/material/Box';
import { BarChart } from '@mui/x-charts/BarChart';
import { useTheme } from '@mui/material/styles';

const uData = [4000, 3000, 2000, 2780, 1890, 2390, 3490];
const pData = [2400, 1398, 9800, 3908, 4800, 3800, 4300];
const amtData = [2400, 2210, 2290, 2000, 2181, 2500, 2100];

const xLabels = [
  'Page A',
  'Page B',
  'Page C',
  'Page D',
  'Page E',
  'Page F',
  'Page G',
];

export default function MixedBarChart({ className }) {
  const theme = useTheme();

  return (
    <div className={`chatbot-container ${className || ''}`}>
      <Box sx={{ width: '100%', height: 400 }}>
        <BarChart
          series={[
            // Les couleurs viennent du thème (cohérent clair/sombre)
            { data: pData, label: 'pv', stack: 'stack1', color: theme.palette.primary.main },
            { data: amtData, label: 'amt', color: theme.palette.error.main },
            { data: uData, label: 'uv', stack: 'stack1', color: theme.palette.secondary.main },
          ]}
          xAxis={[{ data: xLabels }]}
          yAxis={[{ width: 50 }]}
          // Styles d’axes/légende pilotés par le thème
          sx={(t) => ({
            '& .MuiChartsAxis-root text': { fill: t.palette.text.primary },
            '& .MuiChartsLegend-root': { color: t.palette.text.primary },
          })}
        />
      </Box>
    </div>
  );
}

