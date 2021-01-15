import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import {LoginPage, RegisterPage, UserPage} from "./components/pages";


class App extends React.Component {

  render() {
    const {message, isLoading} = this.props;

    return (
      <Router>
        <div className="App">
          <p><Link to="/login">Login</Link></p>
          <p><Link to="/register">Register</Link></p>
          {message && <p>Message: {message}</p>}
          {isLoading && <p>Loading...</p>}
          <Switch>
            <Route path="/login">
              <LoginPage/>
            </Route>
            <Route path="/register">
              <RegisterPage/>
            </Route>
            <Route path="/:id" render={({match}) => {
              return <UserPage id={match.params.id}/>
            }}>
            </Route>
          </Switch>
        </div>
      </Router>
    );
  }
}

App.propTypes = {
  isLoading: PropTypes.bool.isRequired,
  message: PropTypes.string.isRequired,
}


const mapStateToProps = state => ({
  isLoading: state.isLoading,
  message: state.message,
});


export default connect(mapStateToProps, null)(App);

