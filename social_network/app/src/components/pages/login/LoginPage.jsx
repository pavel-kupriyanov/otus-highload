import React from 'react';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {Form} from "react-final-form";

import {login} from "../../../app/actionCreators";
import LoginForm from "./Form";


class LoginPage extends React.Component {

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  async handleSubmit(form) {
    await this.props.login(form.email, form.password);
  }

  render() {
    return (
      <div>
        <h1>Login</h1>
        <Form
          component={LoginForm}
          onSubmit={this.handleSubmit}
        />
      </div>
    );
  }
}


const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    login,
  }, dispatch)
}

export default connect(null, mapDispatchToProps)(LoginPage);
