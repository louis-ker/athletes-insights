import * as React from 'react';
import { ScatterChart } from '@mui/x-charts/ScatterChart';
import { useSeries, useXScale, useYScale } from '@mui/x-charts/hooks';
import { ChartsClipPath } from '@mui/x-charts/ChartsClipPath';
import useId from '@mui/utils/useId';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';
import { rainbowSurgePalette } from '@mui/x-charts/colorPalettes';

const diamonds = [
  { carat: 0.23, price: 326 },
  { carat: 0.75, price: 2760 },
  { carat: 0.7, price: 2777 },
  { carat: 0.77, price: 2798 },
  { carat: 0.3, price: 554 },
  { carat: 0.71, price: 2822 },
  { carat: 0.7, price: 2838 },
  { carat: 0.7, price: 2854 },
  { carat: 1.22, price: 2862 },
  { carat: 0.73, price: 2876 },
  { carat: 0.75, price: 2898 },
  { carat: 0.71, price: 2913 },
  { carat: 0.8, price: 2935 },
  { carat: 0.72, price: 2954 },
  { carat: 0.32, price: 559 },
  { carat: 0.87, price: 2993 },
  { carat: 0.61, price: 3011 },
  { carat: 0.71, price: 3035 },
  { carat: 0.81, price: 3053 },
  { carat: 0.83, price: 3078 },
  { carat: 0.94, price: 3099 },
  { carat: 0.86, price: 3115 },
  { carat: 0.73, price: 3140 },
  { carat: 0.9, price: 3162 },
  { carat: 0.7, price: 3176 },
  { carat: 0.71, price: 3198 },
  { carat: 1.18, price: 3219 },
  { carat: 0.31, price: 562 },
  { carat: 1.04, price: 3261 },
  { carat: 0.8, price: 3283 },
  { carat: 0.7, price: 3303 },
  { carat: 0.71, price: 3321 },
  { carat: 0.7, price: 3345 },
  { carat: 0.9, price: 3368 },
  { carat: 0.3, price: 567 },
  { carat: 0.92, price: 3400 },
  { carat: 0.71, price: 3425 },
  { carat: 1, price: 3450 },
  { carat: 1, price: 3465 },
  { carat: 0.72, price: 3489 },
  { carat: 0.53, price: 3517 },
  { carat: 1.01, price: 3535 },
  { carat: 1.01, price: 3563 },
  { carat: 1.08, price: 3590 },
  { carat: 0.31, price: 571 },
  { carat: 0.9, price: 3629 },
  { carat: 1.01, price: 3658 },
  { carat: 0.9, price: 3677 },
  { carat: 0.9, price: 3697 },
  { carat: 0.9, price: 3722 },
  { carat: 0.87, price: 3742 },
  { carat: 1.01, price: 3756 },
  { carat: 0.9, price: 3780 },
  { carat: 1.01, price: 3801 },
  { carat: 1.01, price: 3818 },
  { carat: 0.93, price: 3844 },
  { carat: 1.2, price: 3871 },
  { carat: 0.3, price: 574 },
  { carat: 0.95, price: 3907 },
  { carat: 1.01, price: 3932 },
  { carat: 1.01, price: 3959 },
  { carat: 0.91, price: 3975 },
  { carat: 0.91, price: 3998 },
  { carat: 1.14, price: 4022 },
  { carat: 1.03, price: 4038 },
  { carat: 0.97, price: 4063 },
  { carat: 1, price: 4081 },
  { carat: 0.35, price: 409 },
  { carat: 0.98, price: 4116 },
  { carat: 0.9, price: 4135 },
  { carat: 1, price: 4155 },
  { carat: 1.17, price: 4167 },
  { carat: 1, price: 4189 },
  { carat: 1, price: 4202 },
  { carat: 0.33, price: 579 },
  { carat: 0.91, price: 4240 },
  { carat: 0.9, price: 4258 },
  { carat: 1.01, price: 4276 },
  { carat: 1.02, price: 4291 },
  { carat: 1, price: 4312 },
  { carat: 1.01, price: 4327 },
  { carat: 1.52, price: 4345 },
  { carat: 1, price: 4368 },
  { carat: 0.9, price: 4386 },
  { carat: 1.07, price: 4401 },
  { carat: 1.12, price: 4422 },
  { carat: 1.03, price: 4441 },
  { carat: 0.3, price: 585 },
];

const dollarFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

export default function ScatterRegressionLine() {
  return (
    <Stack width="100%">
      <Typography variant="h6" component="span" textAlign="center">
        Relation between Weight and Price of Diamonds
      </Typography>
      <ScatterChart
        dataset={diamonds}
        height={300}
        xAxis={[{ min: 0, label: 'Weight (carats)' }]}
        yAxis={[
          {
            min: 0,
            width: 80,
            valueFormatter: (value) => dollarFormatter.format(value),
            label: 'Price (USD)',
          },
        ]}
        series={[
          {
            id: 'diamonds',
            datasetKeys: { x: 'carat', y: 'price' },
            markerSize: 2,
            valueFormatter: (v) => `${dollarFormatter.format(v.y)} for ${v.x} carat`,
          },
        ]}
      >
        <RegressionLine seriesId="diamonds" />
      </ScatterChart>

      <Typography variant="caption">Source: OpenML</Typography>
    </Stack>
  );
}

function RegressionLine({ seriesId }) {
  const theme = useTheme();
  const palette = rainbowSurgePalette(theme.palette.mode);
  const stroke = palette[2];
  const allSeries = useSeries();
  const series = allSeries.scatter.series[seriesId];
  const xScale = useXScale(series.xAxisId);
  const yScale = useYScale(series.yAxisId);
  const clipPathId = `linear-regression-clip-${useId()}`;

  const { m, b } = linearRegression(series.data ?? []);

  const xDomain = xScale.domain();
  const x1 = xScale(xDomain[0]);
  const x2 = xScale(xDomain[1]);
  const y1 = yScale(m * xDomain[0] + b);
  const y2 = yScale(m * xDomain[1] + b);

  return (
    <React.Fragment>
      <ChartsClipPath id={clipPathId} />
      <g clipPath={`url(#${clipPathId})`}>
        <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={stroke} strokeWidth={2} />
      </g>
    </React.Fragment>
  );
}

function linearRegression(points) {
  const n = points.length;

  // Calculate sums
  let sumX = 0,
    sumY = 0,
    sumXY = 0,
    sumX2 = 0;

  for (let i = 0; i < n; i += 1) {
    const x = points[i].x;
    const y = points[i].y;
    sumX += x;
    sumY += y;
    sumXY += x * y;
    sumX2 += x * x;
  }

  // Calculate slope (m) and intercept (b)
  const m = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const b = (sumY - m * sumX) / n;

  return { m, b };
}