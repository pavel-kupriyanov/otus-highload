import React from 'react';
import PropTypes from "prop-types";
import Hobbies from "./Hobbies";
import {Link} from "react-router-dom";


export default class UserCard extends React.Component {

  render() {
    const {user} = this.props;

    return (
      <div>
        <hr/>
        <div>
          <Link to={`/${user.id}`}>
            <h3>{user.first_name} {user.last_name}</h3>
          </Link>
          <p>Age: {user.age}</p>
          {user.city && <p>City: {user.city}</p>}
          {user.gender && <p>Gender: {user.gender}</p>}
        </div>
        <Hobbies hobbies={user.hobbies}/>
      </div>
    );
  }
}

UserCard.propTypes = {
  user: PropTypes.object.isRequired,
}



