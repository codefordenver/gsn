import React from "react";
import {storiesOf} from "@storybook/react";
import Breadcrumbs from "../../src/components/Breadcrumbs"
import { MuiThemeProvider } from '@material-ui/core';
import theme from "../../src/utils/theme"
import { Router} from 'react-router-dom';
import history from "../../src/utils/history"

export default storiesOf("Components", module).add ("Breadcrumbs", () => 
  <Router history={history}>
    <MuiThemeProvider theme={theme} >
      <Breadcrumbs />
    </MuiThemeProvider>
  </Router>)