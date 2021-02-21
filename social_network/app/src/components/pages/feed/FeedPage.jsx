import React from 'react';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {Container, Grid, Typography} from "@material-ui/core";

import New from "../../common/components/New";
// import {animateScroll} from "react-scroll";
//
// import {
//   getChatUser,
//   clearChatUser,
//   getMessages,
//   clearMessages,
//   sendMessage
// } from "../../../app/actionCreators";
//
// import Paper from '@material-ui/core/Paper';
// import Grid from '@material-ui/core/Grid';
// import Divider from '@material-ui/core/Divider';
// import List from '@material-ui/core/List';
//
// import {Form} from "react-final-form";
//
// import Message from "./Message";
// import MessageForm from "./Form";
// import {Button} from "@material-ui/core";

// const PAGE_LIMIT = 10;


// const chatStyle = {
//   width: '100%',
//   height: '70vh',
//   marginTop: 10,
//   minWidth: 650,
//   overflowY: 'auto'
// }


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


class FeedPage extends React.Component {

  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     page: 1,
  //     isAll: false,
  //   }
  //   this.handleSubmit = this.handleSubmit.bind(this);
  //   this.scrollToBottom = this.scrollToBottom.bind(this);
  //   this.handleOlder = this.handleOlder.bind(this);
  // }


  // componentDidMount() {
  //   const {getMessages, getChatUser, chatUserId, chat} = this.props;
  //   getChatUser(chatUserId);
  //   getMessages(chatUserId, 0, 1, PAGE_LIMIT);
  //
  //   this.interval = setInterval(() => {
  //     const messages = this.props.chat.messages;
  //     const lastMessage = messages[messages.length - 1];
  //     if (lastMessage) {
  //       getMessages(chatUserId, lastMessage.created, 1, PAGE_LIMIT);
  //     }
  //   }, 2 * 1000);
  // }
  //
  // componentDidUpdate(prevProps, prevState, snapshot) {
  //   const prevMessages = prevProps.chat.messages;
  //   const messages = this.props.chat.messages;
  //
  //   const lastPrevMessage = prevMessages[prevMessages.length - 1];
  //   const lastMessage = messages[messages.length - 1];
  //
  //   if (lastPrevMessage !== lastMessage) {
  //     this.scrollToBottom();
  //   }
  // }
  //
  // componentWillUnmount() {
  //   const {clearChatUser, clearMessages} = this.props;
  //   clearChatUser();
  //   clearMessages();
  //   clearInterval(this.interval);
  // }
  //
  // scrollToBottom() {
  //   animateScroll.scrollToBottom({containerId: "scroll-end", duration: 0});
  // }
  //
  // handleSubmit(form) {
  //   const {sendMessage, chatUserId} = this.props;
  //   sendMessage(chatUserId, form.text);
  // }
  //
  // async handleOlder(page) {
  //   const {getMessages, chatUserId} = this.props;
  //   const isNotEmpty = await getMessages(chatUserId, 0, page, PAGE_LIMIT);
  //   this.setState({...this.state, page: page, isAll: !isNotEmpty});
  // }

  // render() {
  //   const {chat, currentUser} = this.props;
  //   const {page, isAll} = this.state;
  //   const users = [chat.user, currentUser];
  //   const isReady = chat.user.id && currentUser.id;
  //   return (
  //     <>
  //       <Grid container component={Paper} style={chatStyle} id="scroll-end">
  //         <Grid item xs={12}>
  //           <List>
  //             {!isAll && <Button
  //               variant="contained"
  //               color="primary"
  //               type="submit"
  //               size="small"
  //               style={{marginLeft: '10px'}}
  //               onClick={() => this.handleOlder(page + 1)}>
  //               Older messages
  //             </Button>}
  //             {isReady && chat.messages.map(m =>
  //               <Message user={users.find(u => u.id === m.author_id)} message={m} key={m.id}/>)}
  //           </List>
  //           <Divider/>
  //         </Grid>
  //       </Grid>
  //       <Form onSubmit={this.handleSubmit} component={MessageForm}/>
  //     </>
  //   );
  // }

  render() {
    const news = feed;

    return <Container>
      <Grid item container spacing={2} justify="space-between" direction="row">
        {news.map(user => <Grid item xs={12} key={'user_' + user.id}>
            <New newItem={user}/>
          </Grid>
        )}
        {!news.length && <Typography variant="h5" component="h2" style={{marginBottom: "10px"}}>
          News not found
        </Typography>}
      </Grid>
    </Container>
  }
}

const mapStateToProps = state => ({});

const mapDispatchToProps = dispatch => {
  return bindActionCreators({}, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(FeedPage);
