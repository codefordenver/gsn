import React from "react";
import {storiesOf} from "@storybook/react";
import { Provider } from "react-redux";
import store from "../../src/state/store";

import Login from "../../src/pages/Login"
import { Router} from 'react-router-dom';
import history from "../../src/utils/history"
import { MuiThemeProvider } from '@material-ui/core';
import theme from "../../src/utils/theme"

export default storiesOf("Login", module).add ("Login", () => 
<Provider store={store}>
<Router  history={history}>
<MuiThemeProvider theme={theme} >
<Login/>
</MuiThemeProvider>
</Router>
</Provider>
)