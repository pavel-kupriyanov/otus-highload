import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {getUser} from "../../../app/actionCreators";


class UserPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {loading: true,};
  }

  async componentDidMount() {
    await this.props.getUser(this.props.id);
    this.setState({loading: false});
  }


  render() {
    const {user} = this.props;

    return (
      <div>
        {(this.state.loading || !user)
          ? <div>Loading...</div> :
          <div>
            <h1>User</h1>
            <p>{user.first_name} {user.last_name}</p>
            <p>Age: {user.age}</p>
            {user.city && <p>City: {user.city}</p>}
            {user.gender && <p>Gender: {user.gender}</p>}
          </div>}
      </div>
    );
  }
}

UserPage.propTypes = {
  id: PropTypes.string.isRequired,
  user: PropTypes.object,
  getUser: PropTypes.func.isRequired,
}

const mapStateToProps = state => ({
  user: state.user,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUser,
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(UserPage);
