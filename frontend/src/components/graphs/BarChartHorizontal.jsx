// import * as React from 'react';
// import { useTheme, styled } from '@mui/material/styles';
// import Typography from '@mui/material/Typography';
// import { BarChart } from '@mui/x-charts/BarChart';
// import { useAnimate, useAnimateBar, useDrawingArea } from '@mui/x-charts/hooks';
// import { interpolateObject } from '@mui/x-charts-vendor/d3-interpolate';
// import Box from '@mui/material/Box';

// const athleteStats = [
//   { athlete: 'Yang Yang (A)', wins: 6, runnerUps: 1, thirds: 1 },
//   { athlete: 'Sylvie Daigle', wins: 5, runnerUps: 3, thirds: 0 },
//   { athlete: 'Choi Min-jeong', wins: 4, runnerUps: 1, thirds: 1 },
//   { athlete: 'Nathalie Lambert', wins: 3, runnerUps: 2, thirds: 0 },
//   { athlete: 'Chun Lee-kyung', wins: 3, runnerUps: 1, thirds: 0 },
//   { athlete: 'Jin Sun-yu', wins: 3, runnerUps: 1, thirds: 0 },
//   { athlete: 'Wang Meng', wins: 3, runnerUps: 2, thirds: 1 },
//   { athlete: 'Miyoshi Kato', wins: 2, runnerUps: 2, thirds: 1 },
//   { athlete: 'Eiko Shishii', wins: 2, runnerUps: 1, thirds: 1 },
//   { athlete: 'Bonnie Blair', wins: 2, runnerUps: 1, thirds: 0 },
//   { athlete: 'Choi Eun-kyung', wins: 2, runnerUps: 1, thirds: 0 },
//   { athlete: 'Suzanne Schulting', wins: 2, runnerUps: 0, thirds: 0 },
//   { athlete: 'Maryse Perreault', wins: 1, runnerUps: 3, thirds: 2 },
//   { athlete: 'Mariko Kinoshita', wins: 1, runnerUps: 0, thirds: 1 },
//   { athlete: 'Kim So-hee', wins: 1, runnerUps: 1, thirds: 0 },
//   { athlete: 'Park Seung-hi', wins: 1, runnerUps: 2, thirds: 1 },
//   { athlete: 'Cho Ha-ri', wins: 1, runnerUps: 0, thirds: 0 },
//   { athlete: 'Li Jianrou', wins: 1, runnerUps: 0, thirds: 0 },
//   { athlete: 'Shim Suk-hee', wins: 1, runnerUps: 3, thirds: 2 },
//   { athlete: 'Elise Christie', wins: 1, runnerUps: 0, thirds: 0 },
//   { athlete: 'Yang Yang (S)', wins: 0, runnerUps: 2, thirds: 2 },
//   { athlete: 'Mika Kato', wins: 0, runnerUps: 3, thirds: 0 },
//   { athlete: 'Wang Chunlu', wins: 0, runnerUps: 2, thirds: 0 },
//   { athlete: 'Valérie Maltais', wins: 0, runnerUps: 2, thirds: 0 },
//   { athlete: 'Arianna Fontana', wins: 0, runnerUps: 1, thirds: 2 },
//   { athlete: 'Kalyna Roberge', wins: 0, runnerUps: 0, thirds: 2 },
//   { athlete: 'Kim Boutin', wins: 0, runnerUps: 2, thirds: 0 },
//   { athlete: 'Zhou Yang', wins: 0, runnerUps: 1, thirds: 2 },
//   { athlete: 'Byun Chun-sa', wins: 0, runnerUps: 0, thirds: 1 },
//   { athlete: 'Ko Gi-hyun', wins: 0, runnerUps: 1, thirds: 0 },
//   { athlete: 'Yumiko Yamada', wins: 0, runnerUps: 1, thirds: 0 },
//   { athlete: 'Yang Shin-young', wins: 0, runnerUps: 0, thirds: 1 },
//   { athlete: 'Courtney Sarault', wins: 0, runnerUps: 1, thirds: 0 },
//   { athlete: 'Xandra Velzeboer', wins: 0, runnerUps: 0, thirds: 1 },
// ];

// export default function BarChartHorizontal({ className }) {
//   const theme = useTheme();

//   return (
//     <div className={`chatbot-container ${className || ''}`}>
//       <Box
//         sx={{
//           width: '100%',
//           aspectRatio: '16 / 9',   // ⭐ RATIO DYNAMIQUE
//           maxHeight: '100%',       // évite les débordements
//           // overflow: 'hidden',
//         }}
//       >
//         <Typography marginBottom={2}>
//           Palmarès des athlètes (🥇 Wins / 🥈 Runner-up / 🥉 Third)
//         </Typography>
//         <BarChart
//           height={900}
//           dataset={athleteStats}
//           series={[
//             { dataKey: 'wins', label: '🥇 Winner', color: '#ffc800ff' },
//             { dataKey: 'runnerUps', label: '🥈 Runner-up', color: '#405b50ff' },
//             { dataKey: 'thirds', label: '🥉 Third', color: '#903c00ff' },
//           ]}
//           layout="horizontal"
//           xAxis={[{ label: 'Number of podiums',
//                     valueFormatter: (v) => `${v}`,
//           }]}
//           yAxis={[{ scaleType: 'band', dataKey: 'athlete', width: 180 }]}
//         />
//       </Box>
//     </div>
//   );
// }

import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import { BarChart } from '@mui/x-charts/BarChart';
import Box from '@mui/material/Box';

const athleteStats = [
  { athlete: 'Yang Yang (A)', wins: 6, runnerUps: 1, thirds: 1 },
  { athlete: 'Sylvie Daigle', wins: 5, runnerUps: 3, thirds: 0 },
  { athlete: 'Choi Min-jeong', wins: 4, runnerUps: 1, thirds: 1 },
  { athlete: 'Nathalie Lambert', wins: 3, runnerUps: 2, thirds: 0 },
  { athlete: 'Chun Lee-kyung', wins: 3, runnerUps: 1, thirds: 0 },
  { athlete: 'Jin Sun-yu', wins: 3, runnerUps: 1, thirds: 0 },
  { athlete: 'Wang Meng', wins: 3, runnerUps: 2, thirds: 1 },
  { athlete: 'Miyoshi Kato', wins: 2, runnerUps: 2, thirds: 1 },
  { athlete: 'Eiko Shishii', wins: 2, runnerUps: 1, thirds: 1 },
  { athlete: 'Bonnie Blair', wins: 2, runnerUps: 1, thirds: 0 },
  { athlete: 'Choi Eun-kyung', wins: 2, runnerUps: 1, thirds: 0 },
  { athlete: 'Suzanne Schulting', wins: 2, runnerUps: 0, thirds: 0 },
  { athlete: 'Maryse Perreault', wins: 1, runnerUps: 3, thirds: 2 },
  { athlete: 'Mariko Kinoshita', wins: 1, runnerUps: 0, thirds: 1 },
  { athlete: 'Kim So-hee', wins: 1, runnerUps: 1, thirds: 0 },
  { athlete: 'Park Seung-hi', wins: 1, runnerUps: 2, thirds: 1 },
  { athlete: 'Cho Ha-ri', wins: 1, runnerUps: 0, thirds: 0 },
  { athlete: 'Li Jianrou', wins: 1, runnerUps: 0, thirds: 0 },
  { athlete: 'Shim Suk-hee', wins: 1, runnerUps: 3, thirds: 2 },
  { athlete: 'Elise Christie', wins: 1, runnerUps: 0, thirds: 0 },
  { athlete: 'Yang Yang (S)', wins: 0, runnerUps: 2, thirds: 2 },
  { athlete: 'Mika Kato', wins: 0, runnerUps: 3, thirds: 0 },
  { athlete: 'Wang Chunlu', wins: 0, runnerUps: 2, thirds: 0 },
  { athlete: 'Valérie Maltais', wins: 0, runnerUps: 2, thirds: 0 },
  { athlete: 'Arianna Fontana', wins: 0, runnerUps: 1, thirds: 2 },
  { athlete: 'Kalyna Roberge', wins: 0, runnerUps: 0, thirds: 2 },
  { athlete: 'Kim Boutin', wins: 0, runnerUps: 2, thirds: 0 },
  { athlete: 'Zhou Yang', wins: 0, runnerUps: 1, thirds: 2 },
  { athlete: 'Byun Chun-sa', wins: 0, runnerUps: 0, thirds: 1 },
  { athlete: 'Ko Gi-hyun', wins: 0, runnerUps: 1, thirds: 0 },
  { athlete: 'Yumiko Yamada', wins: 0, runnerUps: 1, thirds: 0 },
  { athlete: 'Yang Shin-young', wins: 0, runnerUps: 0, thirds: 1 },
  { athlete: 'Courtney Sarault', wins: 0, runnerUps: 1, thirds: 0 },
  { athlete: 'Xandra Velzeboer', wins: 0, runnerUps: 0, thirds: 1 },
];

export default function BarChartHorizontal({ className }) {
  const theme = useTheme();

  return (
    <div
      className={`chatbot-container ${className || ''}`}
      style={{
        width: '100%',
        height: '100%',              // 🟢 occupe toute la hauteur du container
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Typography
        marginBottom={2}
        sx={{
          color: theme.palette.text.primary,
          flexShrink: 0,            // 🟢 ne se fait pas écraser par le graphe
          fontWeight: 500,
        }}
      >
        Athletes' Record (🥇 Wins / 🥈 Runner-up / 🥉 Third)
      </Typography>

      {/* Zone du graphe qui prend tout l'espace restant */}
      <Box
        sx={{
          flex: 1,                  // 🟢 prend tout l'espace restant
          minHeight: 0,
          width: '100%',
        }}
      >
        <BarChart
          dataset={athleteStats}
          series={[
            { dataKey: 'wins',      label: '🥇 Winner',    color: '#ffc800ff' },
            { dataKey: 'runnerUps', label: '🥈 Runner-up', color: '#405b50ff' },
            { dataKey: 'thirds',    label: '🥉 Third',     color: '#903c00ff' },
          ]}
          layout="horizontal"
          xAxis={[
            {
              label: 'Number of podiums',
              valueFormatter: (v) => `${v}`,
            },
          ]}
          yAxis={[
            {
              scaleType: 'band',
              dataKey: 'athlete',
              width: 180,
            },
          ]}
        />
      </Box>
    </div>
  );
}
