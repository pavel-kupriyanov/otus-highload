import React from 'react';
import {Link} from "react-router-dom";
import PropTypes from "prop-types";
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {logout} from "../../../app/actionCreators";


class Header extends React.Component {


  render() {
    const {message, isLoading, isAuthenticated, logout} = this.props;

    return (
      <div>
        <p><Link to="/login">Login</Link></p>
        <p><Link to="/register">Register</Link></p>
        {message && <p>Message: {message}</p>}
        {isLoading && <p>Loading...</p>}
        {isAuthenticated && <button onClick={logout}>Logout</button>}
      </div>
    );
  }
}


Header.propTypes = {
  isLoading: PropTypes.bool.isRequired,
  message: PropTypes.string.isRequired,
  isAuthenticated: PropTypes.bool.isRequired,
  logout: PropTypes.func
}


const mapStateToProps = state => ({
  isLoading: state.isLoading,
  message: state.message,
  isAuthenticated: state.currentUser.isAuthenticated
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    logout,
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(Header);
