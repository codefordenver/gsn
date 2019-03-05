import React from "react";
import {storiesOf} from "@storybook/react";
import { Provider } from "react-redux";
import store from "../../src/state/store";

import Login from "../../src/pages/login/LoginForm"
import { Router} from 'react-router-dom';
import history from "../../src/utils/history"

export default storiesOf("Login", module).add ("Login", () => 
<Provider store={store}>
<Router  history={history}>
<Login/>
</Router>
</Provider>
)