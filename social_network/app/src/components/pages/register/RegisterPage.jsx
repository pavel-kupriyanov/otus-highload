import React from 'react';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {Redirect} from "react-router-dom";
import {Form} from "react-final-form";
import PropTypes from "prop-types";

import {register} from "../../../app/actionCreators";
import RegisterForm from "./Form";


const validateForm = values => {
  if (values.password !== values.confirm) {
    return {
      confirmPassword: "Passwords mismatch"
    }
  }
}


class RegisterPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {redirect: false};
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  async handleSubmit(form) {
    const isSuccess = await this.props.register(form);
    if (isSuccess) {
      this.setState({redirect: true});
    }
  }

  render() {

    return (
      <div>
        {this.state.redirect ?
          <Redirect to={{pathname: "/login"}}/> :
          <div>
            <h1>Register</h1>
            <Form
              component={RegisterForm}
              onSubmit={this.handleSubmit}
              validate={validateForm}
            />
          </div>}
      </div>);
  }
}

RegisterPage.propTypes = {
  register: PropTypes.func
}


const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    register,
  }, dispatch)
}

export default connect(null, mapDispatchToProps)(RegisterPage);
