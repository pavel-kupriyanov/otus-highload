import React from 'react';
import PropTypes from "prop-types";
import UserCard from "./UserCard";


export default class UserList extends React.Component {

  render() {
    const {users} = this.props;

    return (
      <div>
        {users.map(user => <UserCard user={user} key={'user_' + user.id}/>)}
      </div>
    );
  }
}

UserList.propTypes = {
  users: PropTypes.array.isRequired,
}



