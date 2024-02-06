import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#F9D59B', // Example pastel color, replace with the exact color from the design comp
      contrastText: '#fff',
    },
    secondary: {
      main: '#F3B27A', // Example pastel color, replace with the exact color from the design comp
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
    // Add new typography styles based on the design comp
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
    // Add new component styles based on the design comp
  },
});

export default theme;