import React from 'react';
import {
  Grid, withStyles, createMuiTheme, MuiThemeProvider,
} from '@material-ui/core';

// This supports the custom layout of these pages
const theme = createMuiTheme({
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
      contrastText: '#074462',
    },
  },
  grays: {
    g0: '#f2f5f7',
    g1: '#f2f5f7',
    g2: '#dae3e7',
    g3: '#989898',
    g4: '#2e3033',
  },
  typography: {
    useNextVariants: true,
  },
  overrides: {
    MuiInputBase: { // Name of the component ⚛️ / style sheet
      root: {
        background: 'white',
        borderRadius: '0px 32px 32px 0px',
        fontSize: 12,
        marginBottom: 16,
      },
      input: {
        textAlign: 'center',
        minHeight: 24,
        '&:-webkit-autofill': {
          transitionDelay: '9999s',
          transitionProperty: 'background-color, color',
        },
      },
    },
    MuiButton: {
      root: {
        borderRadius: '0px 32px 32px 0px',
        fontSize: 12,
        textTransform: 'none',
      },
    },
  },
});

const styles = theme => ({
  // background image is waaaaay too big right now
  root: {
    backgroundImage: "url('/img/background2.jpg')",
    height: '100vh',
    width: '100%',
  },
  login: {
    height: '100%', background: '#272121cc', display: 'flex', alignItems: 'center',
  },
  content: {
    marginRight: theme.spacing.unit * 2, // 16px
    textAlign: 'center',
    width: '100%',
  },
});

function Layout(props) {
  const { classes: { root, login, content } } = props;
  return (
      <MuiThemeProvider theme={theme}>
          <Grid container alignItems="center" className={root}>
              <Grid item xs={false} sm={4} md={8} />
              <Grid item xs={12} sm={8} md={3} className={login}>
                  <div className={content}>
                      {props.children}
                  </div>
              </Grid>
              <Grid item sm={false} md={1} className={login} />
          </Grid>
      </MuiThemeProvider>
  );
}

export default withStyles(styles)(Layout);
