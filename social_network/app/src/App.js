import React from 'react';
import {BrowserRouter as Router, Switch, Route,} from "react-router-dom";
import {bindActionCreators} from "redux";
import {getUserData} from "./app/actionCreators";
import {connect} from "react-redux";
import {Container, Grid} from "@material-ui/core";

import AuthRedirect from "./components/common/components/AuthRedirect";
import {LoginPage, RegisterPage, UserPage, UsersPage} from "./components/pages";
import Header from "./components/common/components/Header";
import {Loader, Notification} from "./components/common";

import './style.css'

class App extends React.Component {


  componentDidMount() {
    const {currentUser, getUserData} = this.props;
    if (currentUser.isAuthenticated && currentUser.user.id === 0) {
      getUserData(currentUser.authentication.user_id);
    }
    this.interval = setInterval(() => {
      if (currentUser.isAuthenticated) {
        getUserData(currentUser.authentication.user_id);
      }
    }, 60 * 1000);

  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const {currentUser, getUserData} = this.props;
    const stateChanged = prevProps.currentUser.isAuthenticated !== currentUser.isAuthenticated;
    if (stateChanged && currentUser.isAuthenticated) {
      getUserData(currentUser.authentication.user_id);
    }
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {

    return (
      <Router>
        <Header/>
        <Notification/>
        <Container>
          <Grid>
            <Grid container justify='center'>
              <Switch>
                <Route path="/login">
                  <AuthRedirect>
                    <LoginPage/>
                  </AuthRedirect>
                </Route>
                <Route path="/register">
                  <AuthRedirect>
                    <RegisterPage/>
                  </AuthRedirect>
                </Route>
                <Route path="/:id" render={({match}) =>
                  <UserPage
                    key={match.params.id}
                    id={match.params.id}/>
                }>
                </Route>
                <Route path="/">
                  <UsersPage/>
                </Route>
              </Switch>
            </Grid>
          </Grid>
        </Container>
      </Router>
    );
  }
}


const mapStateToProps = state => ({
  currentUser: state.currentUser,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUserData
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(App);

