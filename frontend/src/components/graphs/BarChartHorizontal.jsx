// import * as React from 'react';
// import { useTheme, styled } from '@mui/material/styles';
// import Typography from '@mui/material/Typography';
// import { BarChart } from '@mui/x-charts/BarChart';
// import { useAnimate, useAnimateBar, useDrawingArea } from '@mui/x-charts/hooks';
// import { PiecewiseColorLegend } from '@mui/x-charts/ChartsLegend';
// import { interpolateObject } from '@mui/x-charts-vendor/d3-interpolate';
// import Box from '@mui/material/Box';

// const votesTurnout = [
//   { country: 'Slovakia', turnout: 43 },
//   { country: 'Romania', turnout: 51 },
//   { country: 'Lithuania', turnout: 52 },
//   { country: 'Croatia', turnout: 54 },
//   { country: 'Belgium', turnout: 89 },
//   { country: 'Italy', turnout: 71 },
//   { country: 'Sweden', turnout: 75 },
//   { country: 'Denmark', turnout: 87 },
// ];

// export default function ShinyBarChartHorizontal() {
//   return (
//     <Box width="100%">
//       <Typography marginBottom={2}>
//         European countries with lowest & highest voter turnout
//       </Typography>
//       <BarChart
//         height={300}
//         dataset={votesTurnout}
//         series={[
//           {
//             id: 'turnout',
//             dataKey: 'turnout',
//             stack: 'voter turnout',
//             valueFormatter: (value) => `${value}%`,
//           },
//         ]}
//         layout="horizontal"
//         xAxis={[
//           {
//             id: 'color',
//             min: 0,
//             max: 100,
//             colorMap: {
//               type: 'piecewise',
//               thresholds: [50, 85],
//               colors: ['#d32f2f', '#78909c', '#1976d2'],
//             },
//             valueFormatter: (value) => `${value}%`,
//           },
//         ]}
//         barLabel={(v) => `${v.value}%`}
//         yAxis={[
//           {
//             scaleType: 'band',
//             dataKey: 'country',
//             width: 140,
//           },
//         ]}
//         slots={{
//           legend: PiecewiseColorLegend,
//           barLabel: BarLabelAtBase,
//           bar: BarShadedBackground,
//         }}
//         slotProps={{
//           legend: {
//             axisDirection: 'x',
//             markType: 'square',
//             labelPosition: 'inline-start',
//             labelFormatter: ({ index }) => {
//               if (index === 0) return 'lowest turnout';
//               if (index === 1) return 'average';
//               return 'highest turnout';
//             },
//           },
//         }}
//       />
//     </Box>
//   );
// }

// export function BarShadedBackground(props) {
//   const { ownerState, skipAnimation, id, dataIndex, xOrigin, yOrigin, ...other } =
//     props;
//   const theme = useTheme();

//   const animatedProps = useAnimateBar(props);
//   const { width } = useDrawingArea();
//   return (
//     <React.Fragment>
//       <rect
//         {...other}
//         fill={(theme.vars || theme).palette.text.primary}
//         opacity={theme.palette.mode === 'dark' ? 0.05 : 0.1}
//         x={other.x}
//         width={width}
//       />
//       <rect
//         {...other}
//         filter={ownerState.isHighlighted ? 'brightness(120%)' : undefined}
//         opacity={ownerState.isFaded ? 0.3 : 1}
//         data-highlighted={ownerState.isHighlighted || undefined}
//         data-faded={ownerState.isFaded || undefined}
//         {...animatedProps}
//       />
//     </React.Fragment>
//   );
// }

// const Text = styled('text')(({ theme }) => ({
//   ...theme?.typography?.body2,
//   stroke: 'none',
//   fill: (theme.vars || theme).palette.common.white,
//   transition: 'opacity 0.2s ease-in, fill 0.2s ease-in',
//   textAnchor: 'start',
//   dominantBaseline: 'central',
//   pointerEvents: 'none',
//   fontWeight: 600,
// }));

// function BarLabelAtBase(props) {
//   const {
//     xOrigin,
//     y,
//     height,
//     skipAnimation,
//     ...otherProps
//   } = props;

//   const animatedProps = useAnimate(
//     { x: xOrigin + 8, y: y + height / 2 },
//     {
//       initialProps: { x: xOrigin, y: y + height / 2 },
//       createInterpolator: interpolateObject,
//       transformProps: (p) => p,
//       applyProps: (element, p) => {
//         element.setAttribute('x', p.x.toString());
//         element.setAttribute('y', p.y.toString());
//       },
//       skip: skipAnimation,
//     }
//   );

//   return <Text {...otherProps} {...animatedProps} />;
// }

// BarChartHorizontal.jsx
import * as React from 'react';
import { useTheme, styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import { BarChart } from '@mui/x-charts/BarChart';
import { useAnimate, useAnimateBar, useDrawingArea } from '@mui/x-charts/hooks';
import { PiecewiseColorLegend } from '@mui/x-charts/ChartsLegend';
import { interpolateObject } from '@mui/x-charts-vendor/d3-interpolate';
import Box from '@mui/material/Box';

const votesTurnout = [
  { country: 'Slovakia', turnout: 43 },
  { country: 'Romania', turnout: 51 },
  { country: 'Lithuania', turnout: 52 },
  { country: 'Croatia', turnout: 54 },
  { country: 'Belgium', turnout: 89 },
  { country: 'Italy', turnout: 71 },
  { country: 'Sweden', turnout: 75 },
  { country: 'Denmark', turnout: 87 },
];

export default function ShinyBarChartHorizontal({ className }) {
  const theme = useTheme();

  return (
    <div className={`chatbot-container ${className || ''}`}>
      <Box width="100%">
        <Typography marginBottom={2}>
          European countries with lowest & highest voter turnout
        </Typography>
        <BarChart
          height={300}
          dataset={votesTurnout}
          series={[
            {
              id: 'turnout',
              dataKey: 'turnout',
              stack: 'voter turnout',
              valueFormatter: (value) => `${value}%`,
            },
          ]}
          layout="horizontal"
          xAxis={[
            {
              id: 'color',
              min: 0,
              max: 100,
              colorMap: {
                type: 'piecewise',
                thresholds: [50, 85],
                // Couleurs issues du thème (plus de hex en dur)
                colors: [
                  theme.palette.error.main,       // < 50% : "faible"
                  theme.palette.grey[500],        // entre 50 et 85 : "moyen"
                  theme.palette.primary.main,     // > 85% : "élevé"
                ],
              },
              valueFormatter: (value) => `${value}%`,
            },
          ]}
          barLabel={(v) => `${v.value}%`}
          yAxis={[
            {
              scaleType: 'band',
              dataKey: 'country',
              width: 140,
            },
          ]}
          slots={{
            legend: PiecewiseColorLegend,
            barLabel: BarLabelAtBase,
            bar: BarShadedBackground,
          }}
          slotProps={{
            legend: {
              axisDirection: 'x',
              markType: 'square',
              labelPosition: 'inline-start',
              labelFormatter: ({ index }) => {
                if (index === 0) return 'lowest turnout';
                if (index === 1) return 'average';
                return 'highest turnout';
              },
            },
          }}
        />
      </Box>
    </div>
  );
}

export function BarShadedBackground(props) {
  const { ownerState, skipAnimation, id, dataIndex, xOrigin, yOrigin, ...other } =
    props;
  const theme = useTheme();

  const animatedProps = useAnimateBar(props);
  const { width } = useDrawingArea();
  return (
    <React.Fragment>
      {/* fond d'aide à la lecture → couleur texte (thème) + opacité selon mode */}
      <rect
        {...other}
        fill={(theme.vars || theme).palette.text.primary}
        opacity={theme.palette.mode === 'dark' ? 0.05 : 0.1}
        x={other.x}
        width={width}
      />
      <rect
        {...other}
        filter={ownerState.isHighlighted ? 'brightness(120%)' : undefined}
        opacity={ownerState.isFaded ? 0.3 : 1}
        data-highlighted={ownerState.isHighlighted || undefined}
        data-faded={ownerState.isFaded || undefined}
        {...animatedProps}
      />
    </React.Fragment>
  );
}

const Text = styled('text')(({ theme }) => ({
  ...theme?.typography?.body2,
  stroke: 'none',
  fill: (theme.vars || theme).palette.common.white, // lisible sur les barres
  transition: 'opacity 0.2s ease-in, fill 0.2s ease-in',
  textAnchor: 'start',
  dominantBaseline: 'central',
  pointerEvents: 'none',
  fontWeight: 600,
}));

function BarLabelAtBase(props) {
  const { xOrigin, y, height, skipAnimation, ...otherProps } = props;

  const animatedProps = useAnimate(
    { x: xOrigin + 8, y: y + height / 2 },
    {
      initialProps: { x: xOrigin, y: y + height / 2 },
      createInterpolator: interpolateObject,
      transformProps: (p) => p,
      applyProps: (element, p) => {
        element.setAttribute('x', p.x.toString());
        element.setAttribute('y', p.y.toString());
      },
      skip: skipAnimation,
    }
  );

  return <Text {...otherProps} {...animatedProps} />;
}
