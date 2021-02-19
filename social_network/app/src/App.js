import React from 'react';
import {BrowserRouter as Router, Switch, Route,} from "react-router-dom";
import {bindActionCreators} from "redux";
import {getUserData} from "./app/actionCreators";
import {connect} from "react-redux";
import {Container, Grid} from "@material-ui/core";

import {AuthRedirect, NotAuthRedirect} from "./components/common";
import {LoginPage, RegisterPage, UserPage, UsersPage, ChatPage} from "./components/pages";
import Header from "./components/common/components/Header";
import {Notification} from "./components/common";

import './style.css'

class App extends React.Component {


  componentDidMount() {
    const {userData, getUserData} = this.props;
    const {isAuthenticated, authentication, user} = userData;
    if (isAuthenticated && user.id === 0) {
      getUserData(authentication.user_id);
    }
    this.interval = setInterval(() => {
      const {isAuthenticated, authentication} = this.props.userData;
      if (isAuthenticated) {
        getUserData(authentication.user_id);
      }
    }, 20 * 1000);
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const {userData, getUserData} = this.props;
    const stateChanged = prevProps.userData.isAuthenticated !== userData.isAuthenticated;
    if (stateChanged && userData.isAuthenticated) {
      getUserData(userData.authentication.user_id);
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
                <Route path="/chat/:id" render={({match}) =>
                  <NotAuthRedirect>
                    <ChatPage
                      key={match.params.id}
                      chatUserId={match.params.id}
                    />
                  </NotAuthRedirect>
                }>
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
  userData: state.userData,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUserData
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(App);

