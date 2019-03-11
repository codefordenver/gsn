import { createMuiTheme } from '@material-ui/core/styles';

export default createMuiTheme({
  palette: {
    primary: {
      // light: '#757ce8',
      main: '#074462',
      // dark: '#002884',
      contrastText: '#fff',
    },
    secondary: {
      // light: '#ff7961',
      main: '#f3bc47',
      // dark: '#ba000d',
      contrastText: '#000',
    },
  },
  grays: {
    g0: "#f2f5f7",
    g1: "#f2f5f7",
    g2: "#dae3e7",
    g3: "#989898",
    g4: "#2e3033"
  },
  typography: {
    useNextVariants: true,
    fontFamily: [
      '"Nunito Sans"',
      'Roboto',
      '-apple-system',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
  overrides: {
    // TODO Revisit the spacing between the left nav and toolbar
    MuiListItem: {
      button: {
        paddingLeft: "26px"
      },
      'root' : {
        '&$selected': {
          borderLeft: `6px solid #074462`,
          backgroundColor: '#dae3e7',
          paddingLeft: "20px"
        }
      }
    },
    MuiToolbar: {
      gutters:{
        paddingLeft: "12px",
        '@media (min-width: 600px)': {
          paddingLeft: "12px"
        }
      },
    }
  },
});