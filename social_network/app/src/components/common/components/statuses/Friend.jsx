import React from "react";
import {bindActionCreators} from "redux";
import {deleteFriendship} from "../../../../app/actionCreators";
import {connect} from "react-redux";
import PropTypes from "prop-types";


class Friend extends React.Component {

  constructor(props) {
    super(props);
    this.handleDelete = this.handleDelete.bind(this);
  }

  handleDelete() {
    const {user, deleteFriendship} = this.props;
    deleteFriendship(user.id);
  }

  render() {
    return <div>
      <h4>Friend</h4>
      <button onClick={this.handleDelete}>Delete</button>
    </div>
  }
}

Friend.propTypes = {
  user: PropTypes.object.isRequired,
}


const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    deleteFriendship,
  }, dispatch)
}

export default connect(null, mapDispatchToProps)(Friend);
