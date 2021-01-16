import React from 'react';
import PropTypes from "prop-types";

import {Field, Form} from "react-final-form";
import {required, SimpleField} from "../../common";
import {bindActionCreators} from "redux";
import {addHobby, deleteHobby} from "../../../app/actionCreators";
import {connect} from "react-redux";


class EditableHobbies extends React.Component {

  constructor(props) {
    super(props);
    this.addHobby = this.addHobby.bind(this);
  }

  addHobby(values, form) {
    this.props.addHobby(values.hobby);
    setTimeout(() => form.restart(), 0);
  }

  deleteHobby(id) {
    this.props.deleteHobby(id);
  }

  render() {
    const {hobbies} = this.props;
    const alreadyAdded = value => hobbies.find(hobby => hobby.name === value) ? 'Already added': null;
    const composeValidators = (...validators) => value =>
      validators.reduce((error, validator) => error || validator(value), undefined)


    return (
      <div>
        {hobbies.map(hobby => {
          return <p key={'hobby_' + hobby.id}>
            <span>{hobby.name}</span>
            <button onClick={() => this.deleteHobby(hobby.id)}>Delete</button>
          </p>
        })}
        <Form onSubmit={this.addHobby}>
          {props => (
            <form onSubmit={props.handleSubmit}>
              <Field name="hobby" validate={composeValidators(alreadyAdded, required)} type="text">
                {({input, meta}) => {
                  return <SimpleField
                    input={input}
                    meta={meta}
                    label={"Hobby"}
                    placeholder={"Hobby"}
                  />
                }}
              </Field>
              <button type="submit">Add</button>
            </form>
          )}
        </Form>
      </div>
    );
  }
}

// TODO: autocomplete
EditableHobbies.propTypes = {
  hobbies: PropTypes.array.isRequired,
  addHobby: PropTypes.func,
  deleteHobby: PropTypes.func
}


const mapDispatchToProps = dispatch => {
  return bindActionCreators({addHobby, deleteHobby}, dispatch)
}


export default connect(null, mapDispatchToProps)(EditableHobbies);






