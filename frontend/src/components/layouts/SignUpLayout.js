import React from "react";
import {Grid, withStyles, createMuiTheme, MuiThemeProvider} from "@material-ui/core"

const theme = createMuiTheme({  palette: {
  type: 'dark',
},})

const styles = theme => ({
  root: { height: "100vh", backgroundImage: "url('/img/students.jpeg')" },
  login: { height: "100%", background: "#272121cc", display: "flex", alignItems: "center" },
  content: {
    marginLeft: theme.spacing.unit * 2, // 16px
    marginRight: theme.spacing.unit * 2,
    textAlign: "center",
    width: "100%"
  } 
})

function Layout (props) {
  const {classes: {root, login, content}} = props;
  return (
    <MuiThemeProvider theme={theme} >
      <Grid container alignItems="center" className={root}>
        <Grid item sm={false} md={7}></Grid>
        <Grid item sm={12} md={5} className={login}>
          <div className={content}> 
          {props.children}
          </div>
        </Grid>
      </Grid>
    </MuiThemeProvider>
  )
}

export default withStyles(styles)(Layout);