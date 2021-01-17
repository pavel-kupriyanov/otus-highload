import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {Form} from "react-final-form";


import {getUsers, clearUsers} from "../../../app/actionCreators";
import {UserList} from "../../common";
import SearchForm from "./Form";

class UsersPage extends React.Component {

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    this.props.getUsers('', '');
  }

  componentWillUnmount() {
    this.props.clearUsers();
  }

  handleSubmit(values) {
    // TODO: rewrite it
    this.props.getUsers(values.first_name, values.last_name);
  }


  render() {
    const {users} = this.props;

    return (
      <div>
        <Form
          component={SearchForm}
          onSubmit={this.handleSubmit}
        />
        <UserList users={users}/>
      </div>
    );
  }
}

UsersPage.propTypes = {
  users: PropTypes.array,
  getUsers: PropTypes.func.isRequired,
  clearUsers: PropTypes.func.isRequired,
}

const mapStateToProps = state => ({
  users: state.users,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({getUsers, clearUsers}, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(UsersPage);
