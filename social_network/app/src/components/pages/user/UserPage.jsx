import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {getUser, getFriends, clearUser, clearUsers} from "../../../app/actionCreators";
import {Hobbies, UserList} from "../../common";
import EditableHobbies from "./EditableHobbies";
import FriendRequests from "./FriendRequests";


class UserPage extends React.Component {


  componentDidMount() {
    const {id, getUser, getFriends} = this.props;
    getUser(id);
    getFriends(id);
  }

  componentWillUnmount() {
    const {clearUser, clearUsers} = this.props;
    clearUser();
    clearUsers();
  }


  render() {
    const {id, user, users, currentUser} = this.props;
    const isMyPage = Number(id) === currentUser.user.id;

    return <div>
        {user && user.id && <div>
          <h1>{user.first_name} {user.last_name}</h1>
          <p>Age: {user.age}</p>
          {user.city && <p>City: {user.city}</p>}
          {user.gender && <p>Gender: {user.gender}</p>}
        </div>}
        <h2>Hobbies</h2>
        {isMyPage ? <EditableHobbies hobbies={currentUser.user.hobbies}/> :
          <Hobbies hobbies={user ? user.hobbies: []}/>}
        {isMyPage && <React.Fragment>
          <h2>Friend requests</h2>
          <FriendRequests/>
        </React.Fragment>}
        <h2>Friends</h2>
        <UserList users={users}/>
      </div>
  }
}

UserPage.propTypes = {
  id: PropTypes.string.isRequired,
  user: PropTypes.object,
  accessToken: PropTypes.object,
  getUser: PropTypes.func.isRequired,
  getFriends: PropTypes.func.isRequired,
  clearUser: PropTypes.func.isRequired,
  clearUsers: PropTypes.func.isRequired,
}

const mapStateToProps = state => ({
  user: state.user,
  currentUser: state.currentUser,
  users: state.users,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUser, getFriends, clearUser, clearUsers
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(UserPage);
