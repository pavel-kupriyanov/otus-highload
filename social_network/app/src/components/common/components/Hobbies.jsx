import React from 'react';
import PropTypes from "prop-types";

import {Chip} from "@material-ui/core";

const chipStyle = {
  marginTop: '3px',
  marginRight: '5px',
}

export default class Hobbies extends React.Component {

  render() {
    const {hobbies} = this.props;
    // TODO: not unique key, add user
    return (
      <>
        {hobbies.map(hobby =>
          <Chip key={'hobby_' + hobby.id} label={hobby.name} style={chipStyle}/>
        )}
      </>
    );
  }
}

Hobbies.propTypes = {
  hobbies: PropTypes.array.isRequired,
}



