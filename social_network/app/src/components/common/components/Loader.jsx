import React from 'react';
import {connect} from "react-redux";
import {CircularProgress} from "@material-ui/core";



class Loader extends React.Component {


  render() {

    return (
      <>
        {this.props.isLoading && <CircularProgress color="white"/>}
      </>
    );
  }
}


const mapStateToProps = state => ({
  isLoading: state.isLoading,
});


export default connect(mapStateToProps, null)(Loader);
