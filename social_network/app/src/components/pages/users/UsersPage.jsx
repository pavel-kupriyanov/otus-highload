import React from 'react';
import {connect} from "react-redux";
import PropTypes from "prop-types";
import {bindActionCreators} from "redux";
import {Form} from "react-final-form";


import {getUsers, clearUsers} from "../../../app/actionCreators";
import {UserList} from "../../common";
import SearchForm from "./Form";

const PAGE_LIMIT = 100

class UsersPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      page: 1,
      isAll: false,
      lastQuery: {
        first_name: '',
        last_name: ''
      }
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handlePage = this.handlePage.bind(this);
  }

  componentDidMount() {
    this.props.getUsers('', '', 1, PAGE_LIMIT);
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const {users} = this.props;
    if (prevProps.users.length === users.length) {
      return
    }
    let isAll = false;
    if (users.length < PAGE_LIMIT) {
      isAll = true;
    }
    this.setState({...this.state, isAll});
  }

  componentWillUnmount() {
    this.props.clearUsers();
  }

  handleSubmit(values) {
    this.props.getUsers(values.first_name, values.last_name, 1, PAGE_LIMIT);
    this.setState({...this.state, lastQuery: values});
  }

  handlePage(pageNum) {
    const {lastQuery} = this.state;
    this.props.getUsers(lastQuery.first_name, lastQuery.last_name, pageNum, PAGE_LIMIT);
    this.setState({...this.state, page: pageNum});
  }


  render() {
    const {users} = this.props;
    const {page, isAll} = this.state;


    return (
      <div>
        <Form
          component={SearchForm}
          onSubmit={this.handleSubmit}
        />
        <UserList users={users}/>
        {(page > 1) && <button onClick={() => this.handlePage(page - 1)}>Previous</button>}
        {!isAll && <button onClick={() => this.handlePage(page + 1)}>Next</button>}
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
