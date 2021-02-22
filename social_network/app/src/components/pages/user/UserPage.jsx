import React from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import {bindActionCreators} from 'redux';
import {getUser, getFriends, clearUser, clearUsers} from '../../../app/actionCreators';
import {Hobbies, UserInfo, UserCard} from '../../common';
import EditableHobbies from './EditableHobbies';
import FriendRequests from './FriendRequests';
import {Card, Grid, Typography, FormControlLabel, Checkbox, Paper, Tabs, Tab} from '@material-ui/core';
import New from "../../common/components/New";

const cardStyle = {
  padding: '20px',
  height: '100%',
  marginTop: '10px'
}

const gridStyle = {
  marginTop: '40px',
  padding: '20px'
}

const TABS = {
  FRIENDS: 'FRIENDS',
  POSTS: 'POSTS'
}

const feed = [
  {
    "id": "809e8405-b0db-4760-b8ae-bdfa8696725f",
    "author_id": 2,
    "type": "ADDED_HOBBY",
    "payload": {
      "author": {
        "id": 2,
        "first_name": "Pavel",
        "last_name": "Kupriyanov"
      },
      "hobby": {
        "id": 5,
        "name": "Rt"
      }
    },
    "created": 1613741844.0,
    "populated": false,
    "stored": false
  },
  {
    "id": "63a233f1-897d-4a4e-ac01-b188f85e2004",
    "author_id": 2,
    "type": "ADDED_HOBBY",
    "payload": {
      "author": {
        "id": 2,
        "first_name": "Pavel",
        "last_name": "Kupriyanov"
      },
      "hobby": {
        "id": 2,
        "name": "Foobar"
      }
    },
    "created": 1613741907.0,
    "populated": false,
    "stored": false
  },
  {
    "id": "98000374-e848-4459-88eb-82d6866935f0",
    "author_id": 2,
    "type": "ADDED_FRIEND",
    "payload": {
      "author": {
        "id": 2,
        "first_name": "Pavel",
        "last_name": "Kupriyanov"
      },
      "new_friend": {
        "id": 1,
        "first_name": "sender",
        "last_name": "sender"
      }
    },
    "created": 1613742983.0,
    "populated": false,
    "stored": false
  }
]


class UserPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      showDeclinedFriendRequests: true,
      tab: TABS.POSTS
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
    const {id, user, users, userData} = this.props;
    const news = feed;
    const {showDeclinedFriendRequests, tab} = this.state;
    const isMyPage = Number(id) === userData.user.id;
    const friends = isMyPage ? userData.friends : users;

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
          {isMyPage ? <EditableHobbies hobbies={userData.user.hobbies}/> :
            <Hobbies hobbies={user ? user.hobbies : []}/>}
        </Card>
      </Grid>
      {(isMyPage && !!userData.friendRequests.length) && <>
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
      <Grid item xs={12} style={{marginTop: 70}}>
        <Paper square>
          <Tabs
            value={tab}
            indicatorColor="primary"
            textColor="primary"
            onChange={(e, value) => this.setState({...this.state, tab: value})}
            aria-label="disabled tabs example"
          >
            <Tab label="Friends" value={TABS.FRIENDS}/>
            <Tab label="Posts" value={TABS.POSTS}/>
          </Tabs>
        </Paper>
      </Grid>
      <Grid item xs={12} container spacing={2} justify='space-between' direction='row'>
        {tab === TABS.FRIENDS && friends.map(user => <Grid item xs={6} key={'friend_' + user.id}>
            <UserCard user={user}/>
          </Grid>
        )}
        {tab === TABS.POSTS && news.map(newItem => <Grid item xs={12} key={'new_' + newItem.id}>
            <New newItem={newItem}/>
          </Grid>
        )}
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
  userData: state.userData,
  users: state.users,
});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    getUser, getFriends, clearUser, clearUsers
  }, dispatch)
}


export default connect(mapStateToProps, mapDispatchToProps)(UserPage);
