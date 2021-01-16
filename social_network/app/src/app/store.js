import {createStore, applyMiddleware} from "redux";
import thunk from 'redux-thunk';
import {composeWithDevTools} from 'redux-devtools-extension';

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
} from "./actions";


const initialState = {
  user: {
    id: 0,
    first_name: '',
    last_name: '',
    age: 0,
    gender: null,
    city: '',
    hobbies: []
  },
  accessToken: {
    id: 0,
    value: '',
    user_id: 0,
    expired_at: '',
  },
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
  switch (action.type) {
    case SHOW_MESSAGE: {
      return {...state, message: action.payload}
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
      return {...state, registerErrors: action.payload}
    }
    case LOGIN_SUCCESS: {
      return {...state, accessToken: action.payload, loginErrors: {}}
    }
    case LOGIN_FAILED: {
      return {...state, loginErrors: action.payload}
    }
    case GET_USER_SUCCESS: {
      return {...state, user: action.payload}
    }
    case GET_USER_FAILED: {
      return {...state, error: action.payload}
    }
    case ADD_HOBBY_SUCCESS: {
      return {
        ...state, user: {
          ...state.user,
          hobbies: [...state.user.hobbies, action.payload]
        }
      }
    }
    case DELETE_HOBBY_SUCCESS: {
      return {
        ...state, user: {
          ...state.user,
          hobbies: state.user.hobbies.filter(h => h.id !== action.payload)
        }
      }
    }

    default:
      return state
  }
}
