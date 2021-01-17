import React from 'react';
import PropTypes from 'prop-types';
import {Field} from 'react-final-form';

import {SimpleField} from "../../common";


export default class SearchForm extends React.Component {

  render() {
    const {handleSubmit} = this.props;

    return (
      <form onSubmit={handleSubmit}>
        <Field name="first_name" type="text" parse={value => value || ''} initialValue={''}>
          {({input, meta}) => {
            return <SimpleField
              input={input}
              meta={meta}
              label={"First Name"}
              placeholder={"First Name"}
            />
          }}
        </Field>
        <Field name="last_name" type="text" parse={value => value || ''} initialValue={''}>
          {({input, meta}) => {
            return <SimpleField
              input={input}
              meta={meta}
              label={"Last Name"}
              placeholder={"Last Name"}
            />
          }}
        </Field>
        <button type="submit">Submit</button>
      </form>
    )
  }
}

SearchForm.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
}
