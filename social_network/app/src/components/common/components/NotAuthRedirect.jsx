import React from 'react';
import {Redirect} from "react-router-dom";
import PropTypes from "prop-types";
import {connect} from "react-redux";


class NotAuthRedirect extends React.Component {


  render() {
    const {currentUser} = this.props;

    return (
      <React.Fragment>
        {!(currentUser && currentUser.isAuthenticated) ? <Redirect to={{pathname: '/login'}}/> : ''}
      </React.Fragment>
    );
  }
}


NotAuthRedirect.propTypes = {
  currentUser: PropTypes.object.isRequired,
}


const mapStateToProps = state => ({
  currentUser: state.currentUser,
});


export default connect(mapStateToProps, null)(NotAuthRedirect);
