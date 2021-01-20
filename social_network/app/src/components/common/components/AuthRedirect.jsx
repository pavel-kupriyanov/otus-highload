import React from 'react';
import {Redirect} from "react-router-dom";
import PropTypes from "prop-types";
import {connect} from "react-redux";


class AuthRedirect extends React.Component {


  render() {
    const {currentUser} = this.props;
    const redirect = currentUser && currentUser.isAuthenticated;
    return (
      <React.Fragment>
        {redirect ? <Redirect to={{pathname: `/${currentUser.authentication.user_id}`}}/> :
          this.props.children}
      </React.Fragment>
    );
  }
}


AuthRedirect.propTypes = {
  currentUser: PropTypes.object.isRequired,
}


const mapStateToProps = state => ({
  currentUser: state.currentUser,
});


export default connect(mapStateToProps, null)(AuthRedirect);
