import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import AuthRedirect from "./components/common/components/AuthRedirect";
import {LoginPage, RegisterPage, UserPage, UsersPage} from "./components/pages";
import Header from "./components/common/components/Header";


export default class App extends React.Component {

  render() {

    return (
      <Router>
        <div className="App">
          <Header/>
          <Switch>
            <Route path="/login" render={() =>
              <React.Fragment>
                <AuthRedirect/>
                <LoginPage/>
              </React.Fragment>
            }>
            </Route>
            <Route path="/register" render={() =>
              <React.Fragment>
                <AuthRedirect/>
                <RegisterPage/>
              </React.Fragment>
            }>
            </Route>
            <Route path="/:id" render={({match}) =>
              <UserPage
                key={match.params.id}
                id={match.params.id}/>
            }>
            </Route>
            <Route path="/" render={() => <UsersPage/>}>
            </Route>
          </Switch>
        </div>
      </Router>
    );
  }
}



