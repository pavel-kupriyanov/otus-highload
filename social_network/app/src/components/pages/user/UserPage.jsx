import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {getUser, getFriends, clearUser, clearUsers} from "../../../app/actionCreators";
import {Hobbies, UserList} from "../../common";
import EditableHobbies from "./EditableHobbies";


class UserPage extends React.Component {

// TODO: check move on same page with other user

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

  isMyPage() {
    const {id, currentUser} = this.props;
    return Number(id) === currentUser.authentication.id;
  }


  render() {
    const {user, users, currentUser} = this.props;

    return (
      <div>
        {user && user.id && <div>
          <h1>{user.first_name} {user.last_name}</h1>
          <p>Age: {user.age}</p>
          {user.city && <p>City: {user.city}</p>}
          {user.gender && <p>Gender: {user.gender}</p>}
        </div>}
        <h2>Hobbies</h2>
        {this.isMyPage() ?
          <EditableHobbies hobbies={currentUser.user.hobbies}/> :
          <Hobbies hobbies={user.hobbies}/>}
        <h2>Friends</h2>
        <UserList users={users}/>
      </div>
    );
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
