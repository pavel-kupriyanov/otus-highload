import {createStore, applyMiddleware} from "redux";
import thunk from 'redux-thunk';
import {composeWithDevTools} from 'redux-devtools-extension';

import {loadTokenFromStorage, REQUEST_STATUSES} from "./utils";

import {
  LOGIN_SUCCESS,
  LOGIN_FAILED,
  SHOW_LOADER,
  HIDE_LOADER,
  SHOW_MESSAGE,
  HIDE_MESSAGE,
  REGISTER_SUCCESS,
  REGISTER_FAILED,
  GET_USER_FAILED,
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
  DECLINE_FRIEND_REQUEST, GET_USER_DATA, GET_FRIEND_REQUEST_USERS,
} from "./actions";


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
  currentUser: {
    isAuthenticated: !!loadTokenFromStorage(),
    authentication: loadTokenFromStorage() || DEFAULT_TOKEN,
    user: DEFAULT_USER,
    friends: [],
    friendRequests: [],
    friendRequestUsers: []
  },
  user: DEFAULT_USER,
  users: [],
  isLoading: false,
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
      return {...state, message: ""}
    }
    case SHOW_LOADER: {
      return {...state, isLoading: true}
    }
    case HIDE_LOADER: {
      return {...state, isLoading: false}
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
        currentUser: {
          ...state.currentUser,
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
        currentUser: {
          ...state.currentUser,
          authentication: DEFAULT_TOKEN,
          isAuthenticated: false,
        },
      }
    }
    case GET_USER_DATA: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          user: payload.user,
          friends: payload.friends,
          friendRequests: payload.friendRequests
        },
      }
    }
    case GET_USER_SUCCESS: {
      return {...state, user: payload}
    }
    case GET_USER_FAILED: {
      return {...state, error: payload}
    }
    case CLEAR_USER: {
      return {...state, user: DEFAULT_USER}
    }
    case ADD_HOBBY_SUCCESS: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          hobbies: [...state.currentUser.hobbies, payload]
        }
      }
    }
    case DELETE_HOBBY_SUCCESS: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          hobbies: state.currentUser.hobbies.filter(h => h.id !== payload)
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
        currentUser: {
          ...state.currentUser,
          friends: state.currentUser.friends.filter(user => user.id !== payload)
        }
      }
    }

    case ADD_FRIEND_REQUEST: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          friendRequests: [...state.currentUser.friendRequests, payload]
        }
      }
    }

    case DELETE_FRIEND_REQUEST: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          friendRequests: state.currentUser.friendRequests.filter(req => req.id !== payload)
        }
      }
    }

    case ACCEPT_FRIEND_REQUEST: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          friendRequests: state.currentUser.friendRequests.filter(req => req.id !== payload.requestId),
          friends: [...state.currentUser.friends, payload.friend]
        }
      }
    }

    case DECLINE_FRIEND_REQUEST: {
      const friendRequests = state.currentUser.friendRequests;
      const requestsWithoutChanged = friendRequests.filter(req => req.id !== payload);
      const changedRequest = friendRequests.find(req => req.id === payload);
      changedRequest.status = REQUEST_STATUSES.DECLINED;
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          friendRequests: [...requestsWithoutChanged, changedRequest],
        }
      }
    }
    case GET_FRIEND_REQUEST_USERS: {
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          friendRequestUsers: payload,
        }
      }
    }

    default:
      return state
  }
}
