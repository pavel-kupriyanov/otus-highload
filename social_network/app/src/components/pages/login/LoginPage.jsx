import React from 'react';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {Form} from "react-final-form";
import {Redirect} from "react-router-dom";

import {login} from "../../../app/actionCreators";
import LoginForm from "./Form";
import PropTypes from "prop-types";


class LoginPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {redirect: false};
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  async handleSubmit(form) {
    const isSuccess = await this.props.login(form.email, form.password);
    if (isSuccess) {
      this.setState({redirect: true});
    }
  }

  render() {
    const {accessToken} = this.props;
    return (
      <div>
        {accessToken && accessToken.user_id ?
          <Redirect to={{pathname: `/${accessToken.user_id}`}}/> :
          <div>
            <h1>Login</h1>
            <Form
              component={LoginForm}
              onSubmit={this.handleSubmit}
            />
          </div>}
      </div>
    );
  }
}

LoginPage.propTypes = {
  accessToken: PropTypes.object.isRequired,
}
const mapStateToProps = state => ({
  accessToken: state.accessToken,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    login,
  }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginPage);
