import React from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import PropTypes from "prop-types";

// TODO: remove ../../ ...
import {deleteFriendRequest} from "../../../../app/actionCreators";
import {REQUEST_STATUSES} from "../../../../app/utils";


class WaitingUser extends React.Component {

  constructor(props) {
    super(props);
    this.handleDelete = this.handleDelete.bind(this);
    this.getFriendRequest = this.getFriendRequest.bind(this);
  }

  getFriendRequest() {
    const {currentUser, user} = this.props;
    return currentUser.friendRequests.find(req => {
      return req.from_user === currentUser.user.id && req.to_user === user.id;
    })
  }


  handleDelete(friendRequest) {
    this.props.deleteFriendRequest(friendRequest.id);
  }

  render() {
    const friendRequest = this.getFriendRequest();
    const isWaiting = friendRequest.status === REQUEST_STATUSES.WAITING;

    return <div>
      {isWaiting ? <h4>Waiting user response</h4> : <h4>User decline your request</h4>}
      <button onClick={() => this.handleDelete(friendRequest)}>Delete</button>
    </div>
  }
}

WaitingUser.propTypes = {
  user: PropTypes.object.isRequired,
}

const mapStateToProps = state => ({
  currentUser: state.currentUser
});


const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    deleteFriendRequest
  }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(WaitingUser);
