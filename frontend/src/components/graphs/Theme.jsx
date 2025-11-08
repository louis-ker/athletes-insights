// import { createTheme } from "@mui/material/styles";

// const theme = createTheme({
//   palette: {
//     primary: { main: "#007AFF" },
//     secondary: { main: "#FF3B30" },
//     text: {
//       primary: '#ffffffff' // Couleur visible des axes, labels, légendes
//     },
//   },
// });

// export default theme;

// Theme.jsx
import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { deepmerge } from '@mui/utils';

// Fabrique un thème MUI. Tu peux ajuster les couleurs ici.
export const getAppTheme = (mode = 'light', overrides = {}) => {
  const base = createTheme({
    palette: {
      mode,
      primary: { main: '#ffae00ff' },   // bleu
      secondary: { main: '#ff8080ff' }, // indigo clair
      error: { main: '#dd00ffff' },     // rouge
    },
    // Petites surcharges utiles pour X-Charts
    components: {
      MuiChartsAxis: {
        styleOverrides: {
          root: ({ theme }) => ({
            '& text': { fill: theme.palette.text.primary },
          }),
        },
      },
      MuiChartsLegend: {
        styleOverrides: {
          root: ({ theme }) => ({
            color: theme.palette.text.primary,
          }),
        },
      },
    },
  });

  return createTheme(deepmerge(base, overrides));
};

// Provider prêt à l’emploi : <AppThemeProvider>{...}</AppThemeProvider>
export default function AppThemeProvider({
  children,
  mode = 'light',
  themeOverrides = {},
}) {
  const theme = React.useMemo(
    () => getAppTheme(mode, themeOverrides),
    [mode, themeOverrides]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
