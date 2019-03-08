import React from "react";
import {storiesOf} from "@storybook/react";
import Layout from "../../src/components/layouts/Default"
import { MuiThemeProvider } from '@material-ui/core';
import theme from "../../src/utils/theme"
import { Router} from 'react-router-dom';
import history from "../../src/utils/history"

export default storiesOf("Components", module).add ("Layout", () => 
<Router history={history}><MuiThemeProvider theme={theme} >
<Layout /></MuiThemeProvider></Router>)