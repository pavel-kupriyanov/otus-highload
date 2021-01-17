import React from 'react';
import PropTypes from "prop-types";


export default class Hobbies extends React.Component {

  render() {
    const {hobbies} = this.props;

    return (
      <div>
        {hobbies.map(hobby => <p key={'hobby_' + hobby.id}>{hobby.name}</p>)}
      </div>
    );
  }
}

Hobbies.propTypes = {
  hobbies: PropTypes.array.isRequired,
}



