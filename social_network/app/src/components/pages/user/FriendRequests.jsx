import React from 'react';

import {UserList} from "../../common";
import {bindActionCreators} from "redux";
import {getFriendRequestUsers} from "../../../app/actionCreators";
import {connect} from "react-redux";
import {REQUEST_STATUSES} from "../../../app/utils";


class FriendRequests extends React.Component {

  constructor(props) {
    super(props);
    this.state = {showDeclined: false}
  }

  componentDidMount() {
    const {currentUser} = this.props;
    const friendRequests = currentUser.friendRequests;
    const ids = friendRequests.map(req =>
      req.from_user === currentUser.user.id ? req.to_user : req.from_user
    )
    this.props.getFriendRequestUsers(ids);
  }

  render() {
    const {friendRequestUsers, friendRequests, user} = this.props.currentUser;
    const {showDeclined} = this.state;
    let users = friendRequestUsers;
    if (!showDeclined) {
      const declinedIds = friendRequests
        .filter(req => req.status !== REQUEST_STATUSES.DECLINED)
        .map(req => req.from_user === user.id ? req.to_user : req.from_user)
      users = users.filter(user => declinedIds.find(id => id === user.id))
    }

    console.log(friendRequestUsers);
    return <div>
      Show declined:
      <input
        type='checkbox'
        value={showDeclined}
        onChange={() => this.setState({showDeclined: !showDeclined})}
      />
      <UserList users={users}/>
    </div>
  }
}

const mapStateToProps = state => ({
  currentUser: state.currentUser,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({getFriendRequestUsers}, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(FriendRequests);






