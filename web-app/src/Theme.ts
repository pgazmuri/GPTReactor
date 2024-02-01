import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Blue color used in buttons, you may need to use a color picker tool to get the exact color from the design comp.
      contrastText: '#fff', // Assuming buttons have white text.
    },
    secondary: {
      main: '#9e9e9e', // Gray color for less prominent elements, adjust the shade as needed.
    },
    background: {
      default: '#f5f5f5', // Background color for the main content area.
      paper: '#ffffff', // Background for paper elements.
    },
    text: {
      primary: '#333333', // Main text color, adjust as needed.
      secondary: '#585858', // Secondary text color for less emphasis, adjust as needed.
    },
    // Add any other color overrides from the design comp as needed.
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontSize: '1.3rem',
      fontWeight: 500, // Semi-bold for section titles as per design.
    },
    // Adjust other typographic styles as per the design comp, including font sizes and weights.
    button: {
      textTransform: 'none', // The buttons in the design don't seem to have uppercase text.
    },
    //... other variants
  },
  components: {
    // Example for overriding Button styles
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px', // Assuming buttons have rounded corners.
          // Add other styles like padding, border, etc., to match the design comp.
        },
      },
    },
    // Add overrides for other MUI components as needed to match the design comp.
  },
});

export default theme;