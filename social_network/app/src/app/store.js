import {createStore, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import {composeWithDevTools} from 'redux-devtools-extension';

import {loadTokenFromStorage, REQUEST_STATUSES} from './utils';

import {
  LOGIN_SUCCESS,
  LOGIN_FAILED,
  SHOW_LOADER,
  HIDE_LOADER,
  SHOW_MESSAGE,
  HIDE_MESSAGE,
  REGISTER_SUCCESS,
  REGISTER_FAILED,
  GET_USER_SUCCESS,
  ADD_HOBBY_SUCCESS,
  DELETE_HOBBY_SUCCESS,
  LOGOUT,
  GET_USERS,
  CLEAR_USERS,
  CLEAR_USER,
  DELETE_FRIENDSHIP,
  ADD_FRIEND_REQUEST,
  DELETE_FRIEND_REQUEST,
  ACCEPT_FRIEND_REQUEST,
  DECLINE_FRIEND_REQUEST,
  GET_USER_DATA,
  GET_FRIEND_REQUEST_USERS,
} from './actions';


const DEFAULT_TOKEN = {
  id: 0,
  value: '',
  user_id: 0,
  expired_at: '',
}

const DEFAULT_USER = {
  id: 0,
  first_name: '',
  last_name: '',
  age: 0,
  gender: null,
  city: '',
  hobbies: []
}

const initialState = {
  userData: {
    isAuthenticated: !!loadTokenFromStorage(),
    authentication: loadTokenFromStorage() || DEFAULT_TOKEN,
    user: DEFAULT_USER,
    friends: [],
    friendRequests: [],
    friendRequestUsers: []
  },
  user: DEFAULT_USER,
  users: [],
  requestCount: 0,
  message: '',
  registerErrors: {
    email: null,
    first_name: null,
    last_name: null,
    password: null,
    city: null,
    age: null,
    gender: null,
    general: null,
  },
  loginErrors: {
    email: null,
    password: null,
  },
  error: ''
}
export const store = createStore(
  reducer,
  initialState,
  composeWithDevTools(
    applyMiddleware(thunk)
  )
);

export default function reducer(state = initialState, action) {
  const payload = action.payload;

  switch (action.type) {
    case SHOW_MESSAGE: {
      return {...state, message: payload}
    }
    case HIDE_MESSAGE: {
      return {...state, message: ''}
    }
    case SHOW_LOADER: {
      return {...state, requestCount: state.requestCount + 1}
    }
    case HIDE_LOADER: {
      return {...state, requestCount: state.requestCount - 1}
    }
    case REGISTER_SUCCESS: {
      return {...state, registerErrors: {}}
    }
    case REGISTER_FAILED: {
      return {...state, registerErrors: payload}
    }
    case LOGIN_SUCCESS: {
      return {
        ...state,
        userData: {
          ...state.userData,
          authentication: payload,
          isAuthenticated: true,
        },
        loginErrors: {}
      }
    }
    case LOGIN_FAILED: {
      return {...state, loginErrors: payload}
    }
    case LOGOUT: {
      return {
        ...state,
        userData: {
          user: DEFAULT_USER,
          friends: [],
          friendRequests: [],
          friendRequestUsers: [],
          authentication: DEFAULT_TOKEN,
          isAuthenticated: false,
        },
      }
    }
    case GET_USER_DATA: {
      return {
        ...state,
        userData: {
          ...state.userData,
          user: payload.user,
          friends: payload.friends,
          friendRequests: payload.friendRequests
        },
      }
    }
    case GET_USER_SUCCESS: {
      return {...state, user: payload}
    }
    case CLEAR_USER: {
      return {...state, user: DEFAULT_USER}
    }
    case ADD_HOBBY_SUCCESS: {
      return {
        ...state,
        userData: {
          ...state.userData,
          user: {
            ...state.userData.user,
            hobbies: [...state.userData.user.hobbies, payload]
          }
        }
      }
    }
    case DELETE_HOBBY_SUCCESS: {
      return {
        ...state,
        userData: {
          ...state.userData,
          user: {
            ...state.userData.user,
            hobbies: state.userData.user.hobbies.filter(h => h.id !== payload)
          }
        }
      }
    }
    case GET_USERS: {
      return {...state, users: payload}
    }
    case CLEAR_USERS: {
      return {...state, users: []}
    }

    case DELETE_FRIENDSHIP: {
      return {
        ...state,
        userData: {
          ...state.userData,
          friends: state.userData.friends.filter(user => user.id !== payload)
        }
      }
    }

    case ADD_FRIEND_REQUEST: {
      return {
        ...state,
        userData: {
          ...state.userData,
          friendRequests: [...state.userData.friendRequests, payload]
        }
      }
    }

    case DELETE_FRIEND_REQUEST: {
      return {
        ...state,
        userData: {
          ...state.userData,
          friendRequests: state.userData.friendRequests.filter(req => req.id !== payload)
        }
      }
    }

    case ACCEPT_FRIEND_REQUEST: {
      return {
        ...state,
        userData: {
          ...state.userData,
          friendRequests: state.userData.friendRequests.filter(req => req.id !== payload.requestId),
          friends: [...state.userData.friends, payload.friend]
        }
      }
    }

    case DECLINE_FRIEND_REQUEST: {
      const friendRequests = state.userData.friendRequests;
      const requestsWithoutChanges = friendRequests.filter(req => req.id !== payload);
      const changedRequest = friendRequests.find(req => req.id === payload);
      changedRequest.status = REQUEST_STATUSES.DECLINED;
      return {
        ...state,
        userData: {
          ...state.userData,
          friendRequests: [...requestsWithoutChanges, changedRequest],
        }
      }
    }
    case GET_FRIEND_REQUEST_USERS: {
      return {
        ...state,
        userData: {
          ...state.userData,
          friendRequestUsers: payload,
        }
      }
    }

    default:
      return state
  }
}
