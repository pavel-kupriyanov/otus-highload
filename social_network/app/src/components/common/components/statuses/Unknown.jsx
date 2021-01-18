import React from "react";
import {bindActionCreators} from "redux";
import {addFriendRequest} from "../../../../app/actionCreators";
import {connect} from "react-redux";
import PropTypes from "prop-types";


// TODO: check that UserCard will re-render after it
class Unknown extends React.Component {

  constructor(props) {
    super(props);
    this.handleAdd = this.handleAdd.bind(this);
  }

  handleAdd() {
    const {user, addFriendRequest} = this.props;
    addFriendRequest(user.id);
  }

  render() {
    return <div>
      <button onClick={this.handleAdd}>Add friend</button>
    </div>
  }
}

Unknown.propTypes = {
  user: PropTypes.object.isRequired,
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    addFriendRequest,
  }, dispatch)
}

export default connect(null, mapDispatchToProps)(Unknown);
