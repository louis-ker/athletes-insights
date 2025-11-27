// import Box from '@mui/material/Box';
// import { BarChart } from '@mui/x-charts/BarChart';
// import { useTheme } from '@mui/material/styles';
// import Typography from '@mui/material/Typography';

// const nations = [
//   'South Korea',
//   'Canada',
//   'China',
//   'Netherlands',
//   'United States',
//   'Japan',
//   'Great Britain',
//   'Hungary',
//   'Italy',
//   'Russia',
//   'Australia',
//   'Belgium',
//   'Poland',
//   'Kazakhstan',
//   'France',
// ];

// // Données médailles (alignées avec l’ordre de `nations`)
// const goldData =  [117, 73, 69, 26, 17, 13, 7, 7, 6, 3, 2, 1, 0, 0, 0];
// const silverData = [85, 89, 51, 18, 18, 19, 10, 4,17, 5, 5, 3, 2, 2, 1];
// const bronzeData = [74, 75, 45, 21, 33, 22, 20, 2,25, 9, 4, 2, 3, 0, 0];

// export default function MixedBarChart({ className }) {
//   const theme = useTheme();

//   return (
//     <div className={`chatbot-container ${className || ''}`}>
//       <Box
//         sx={{
//           width: '100%',
//           aspectRatio: '4 / 3',   // ⭐ RATIO DYNAMIQUE
//           maxHeight: '100%',       // évite les débordements
//           // overflow: 'hidden',
//         }}
//       >
//         <Typography
//           variant="h6"
//           align="center"
//           sx={{
//             color: theme.palette.text.primary,
//             mb: 2,
//             fontWeight: 600,
//             // textTransform: 'uppercase',
//             letterSpacing: 1,
//           }}
//         >
//           All-Time Medal Count – World Short-Track Speed Skating Championships
//         </Typography>
//           <BarChart
//             series={[
//               // Empilement des médailles par nation
//               { data: goldData,   label: 'Gold',   stack: 'medals', color: theme.palette.warning.main },
//               { data: silverData, label: 'Silver', stack: 'medals', color: theme.palette.info.main },
//               { data: bronzeData, label: 'Bronze', stack: 'medals', color: theme.palette.secondary.main },
//             ]}
//             xAxis={[{
//               data: nations,
//               scaleType: 'band',
//             }]}
//             yAxis={[{ width: 50,
//                       label: 'Count',
//             }]}
//             tooltip={{ trigger: 'item' }}
//             sx={(t) => ({
//               '& .MuiChartsAxis-root text': { fill: t.palette.text.primary },
//               '& .MuiChartsLegend-root': { color: t.palette.text.primary },
//               '& .MuiChartsAxis-line, & .MuiChartsAxis-tick': { stroke: t.palette.divider },
//             })}
//           />
//       </Box>
//     </div>
//   );
// }


import Box from '@mui/material/Box';
import { BarChart } from '@mui/x-charts/BarChart';
import { useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

const nations = [
  'South Korea',
  'Canada',
  'China',
  'Netherlands',
  'United States',
  'Japan',
  'Great Britain',
  'Hungary',
  'Italy',
  'Russia',
  'Australia',
  'Belgium',
  'Poland',
  'Kazakhstan',
  'France',
];

// Données médailles (alignées avec l’ordre de `nations`)
const goldData   = [117, 73, 69, 26, 17, 13, 7, 7, 6, 3, 2, 1, 0, 0, 0];
const silverData = [85, 89, 51, 18, 18, 19,10, 4,17, 5, 5, 3, 2, 2, 1];
const bronzeData = [74, 75, 45, 21, 33, 22,20, 2,25, 9, 4, 2, 3, 0, 0];

export default function MixedBarChart({ className }) {
  const theme = useTheme();

  return (
    <div
      className={`chatbot-container ${className || ''}`}
      style={{
        width: '100%',
        height: '100%',              // 🟢 prend toute la hauteur du container
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Typography
        variant="h6"
        align="center"
        sx={{
          color: theme.palette.text.primary,
          mb: 2,
          fontWeight: 600,
          letterSpacing: 1,
          flexShrink: 0,            // ne se fait pas écraser par le graphe
        }}
      >
        All-Time Medal Count – World Short-Track Speed Skating Championships
      </Typography>

      {/* Zone du graphe qui prend tout le reste */}
      <Box
        sx={{
          flex: 1,                  // 🟢 occupe tout l'espace restant
          minHeight: 0,             // important pour que le contenu puisse se shrink
          width: '100%',
        }}
      >
        <BarChart
          series={[
            { data: goldData,   label: 'Gold',   stack: 'medals', color: theme.palette.warning.main },
            { data: silverData, label: 'Silver', stack: 'medals', color: theme.palette.info.main },
            { data: bronzeData, label: 'Bronze', stack: 'medals', color: theme.palette.secondary.main },
          ]}
          xAxis={[{
            data: nations,
            scaleType: 'band',
          }]}
          yAxis={[{
            width: 50,
            label: 'Count',
          }]}
          tooltip={{ trigger: 'item' }}
          sx={(t) => ({
            '& .MuiChartsAxis-root text': { fill: t.palette.text.primary },
            '& .MuiChartsLegend-root': { color: t.palette.text.primary },
            '& .MuiChartsAxis-line, & .MuiChartsAxis-tick': { stroke: t.palette.divider },
          })}
        />
      </Box>
    </div>
  );
}
