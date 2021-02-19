import React from 'react';
import {Redirect} from "react-router-dom";
import PropTypes from "prop-types";
import {connect} from "react-redux";


class NotAuthRedirect extends React.Component {


  render() {
    const {userData} = this.props;
    const authenticated = userData && userData.isAuthenticated;
    return (
      <React.Fragment>
        {!authenticated ? <Redirect to={{pathname: '/login'}}/> :
          this.props.children}
      </React.Fragment>
    );
  }
}


NotAuthRedirect.propTypes = {
  userData: PropTypes.object.isRequired,
}


const mapStateToProps = state => ({
  userData: state.userData,
});


export default connect(mapStateToProps, null)(NotAuthRedirect);
