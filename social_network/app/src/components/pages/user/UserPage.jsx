import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {getUser} from "../../../app/actionCreators";
import {Hobbies} from "../../common";
import EditableHobbies from "./EditableHobbies";


class UserPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {loading: true};
  }

// todo: is ready flag?
// TODO: check move on same page with other user

  // todo: clear data in store on unmount
  async componentDidMount() {
    await this.props.getUser(this.props.id);
    this.setState({loading: false});
  }

  isMyPage() {
    const {accessToken, user} = this.props;
    const tokenUserId = accessToken && accessToken.user_id;
    const userId = user && user.id;
    return (tokenUserId && userId && (tokenUserId === userId));
  }


  render() {
    const {user} = this.props;

    return (
      <div>
        {(this.state.loading || !(user && user.id))
          ? <div>Loading...</div> :
          <div>
            <h1>User</h1>
            <p>{user.first_name} {user.last_name}</p>
            <p>Age: {user.age}</p>
            {user.city && <p>City: {user.city}</p>}
            {user.gender && <p>Gender: {user.gender}</p>}
          </div>}
        <h2>Hobbies</h2>
        {this.isMyPage() ?
          <EditableHobbies hobbies={user.hobbies}/> :
          <Hobbies hobbies={user.hobbies}/>}
        <h2>Friends</h2>
      </div>
    );
  }
}

UserPage.propTypes = {
  id: PropTypes.string.isRequired,
  user: PropTypes.object,
  accessToken: PropTypes.object,
  getUser: PropTypes.func.isRequired,
}

const mapStateToProps = state => ({
  user: state.user,
  accessToken: state.accessToken
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUser,
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(UserPage);
