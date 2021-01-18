import React from 'react';
import PropTypes from "prop-types";
import {connect} from "react-redux";

import {You, Friend, WaitingYou, WaitingUser, Unknown} from './statuses'


const statusComponents = {
  YOU: You,
  FRIEND: Friend,
  WAITING_YOU_RESPONSE: WaitingYou,
  WAITING_USER_RESPONSE: WaitingUser,
  UNKNOWN: Unknown,
}


class UserStatus extends React.Component {

  getComponent() {
    // TODO: rename currentUser in props
    const {user, currentUser} = this.props;
    const current = currentUser.user;

    if (!currentUser.isAuthenticated) {
      return statusComponents.UNKNOWN;
    }

    if (user.id === currentUser.authentication.user_id) {
      return statusComponents.YOU;
    }
    if (currentUser.friends.find(friend => friend.id === user.id)) {
      return statusComponents.FRIEND;
    }
    const friendRequestFrom = currentUser.friendRequests.find(req => {
      return req.from_user === current.id && req.to_user === user.id;
    })
    if (friendRequestFrom) {
      return statusComponents.WAITING_USER_RESPONSE
    }
    const friendRequestTo = currentUser.friendRequests.find(req => {
      return req.to_user === current.id && req.from_user === user.id;
    })
    if (friendRequestTo) {
      return statusComponents.WAITING_YOU_RESPONSE;
    }
    return statusComponents.UNKNOWN;
  }

  render() {
    const StatusComponent = this.getComponent();
    return <StatusComponent user={this.props.user}/>;
  }
}

UserStatus.propTypes = {
  user: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  currentUser: state.currentUser,
});


export default connect(mapStateToProps, null)(UserStatus);



