import React from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import {bindActionCreators} from 'redux';
import {getUser, getFriends, clearUser, clearUsers} from '../../../app/actionCreators';
import {Hobbies, UserInfo, UserCard} from '../../common';
import EditableHobbies from './EditableHobbies';
import FriendRequests from './FriendRequests';
import {Card, Grid, Typography, FormControlLabel, Checkbox} from '@material-ui/core';

const cardStyle = {
  padding: '20px',
  height: '100%',
  marginTop: '10px'
}

const gridStyle = {
  marginTop: '40px',
  padding: '20px'
}

class UserPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      showDeclinedFriendRequests: true
    }
  }

  componentDidMount() {
    const {id, getUser, getFriends} = this.props;
    getUser(id);
    getFriends(id);
  }

  componentWillUnmount() {
    const {clearUser, clearUsers} = this.props;
    clearUser();
    clearUsers();
  }


  render() {
    const {id, user, users, currentUser} = this.props;
    const {showDeclinedFriendRequests} = this.state;
    const isMyPage = Number(id) === currentUser.user.id;

    return <Grid item container spacing={2} justify='space-between' direction='row'>
      <Grid item xs={6}>
        <Card style={cardStyle}>
          <Typography variant='h5' component='h2'>
            Common info
          </Typography>
          {user && user.id && <UserInfo user={user}/>}
        </Card>
      </Grid>
      <Grid item xs={6}>
        <Card style={cardStyle}>
          <Typography variant='h5' component='h2'>
            Hobbies
          </Typography>
          {isMyPage ? <EditableHobbies hobbies={currentUser.user.hobbies}/> :
            <Hobbies hobbies={user ? user.hobbies : []}/>}
        </Card>
      </Grid>
      {(isMyPage && !!currentUser.friendRequests.length) && <>
        <Grid item xs={12} style={gridStyle}>
          <Typography variant='h5' component='h2' style={
            {justifyContent: 'space-between', display: 'flex'}}
          >
            Friend requests
            <FormControlLabel
              control={
                <Checkbox
                  checked={showDeclinedFriendRequests}
                  onChange={() => this.setState({
                    showDeclinedFriendRequests: !showDeclinedFriendRequests
                  })}
                  name='showDeclined'
                  color='primary'
                />
              }
              label='Show declined requests'
            />
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <FriendRequests showDeclined={showDeclinedFriendRequests}/>
        </Grid>
      </>}
      <Grid item xs={12} style={gridStyle}>
        <Typography variant='h5' component='h2'>
          Friends
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <Grid item container spacing={2} justify='space-between' direction='row' xs={12}>
          {users.map(user => <Grid item xs={6} key={'friend_' + user.id}>
              <UserCard user={user}/>
            </Grid>
          )}
        </Grid>
      </Grid>
    </Grid>
  }
}

UserPage.propTypes = {
  id: PropTypes.string.isRequired,
  user: PropTypes.object,
  accessToken: PropTypes.object,
  getUser: PropTypes.func.isRequired,
  getFriends: PropTypes.func.isRequired,
  clearUser: PropTypes.func.isRequired,
  clearUsers: PropTypes.func.isRequired,
}

const mapStateToProps = state => ({
  user: state.user,
  currentUser: state.currentUser,
  users: state.users,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUser, getFriends, clearUser, clearUsers
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(UserPage);
