import {default as axiosBase} from 'axios';
import {
  LOGIN_SUCCESS,
  LOGIN_FAILED,
  SHOW_LOADER,
  SHOW_MESSAGE,
  HIDE_LOADER,
  HIDE_MESSAGE,
  REGISTER_FAILED,
  REGISTER_SUCCESS,
  GET_USER_SUCCESS,
  GET_USER_FAILED,
  ADD_HOBBY_SUCCESS,
  DELETE_HOBBY_SUCCESS,
  LOGOUT,
  GET_USERS,
  CLEAR_USER,
  CLEAR_USERS
} from "./actions";
import {
  deleteTokenFromStorage,
  storeTokenIntoStorage,
  parsePayloadError,
  toQueryString
} from "./utils";
import {store} from './store';

export const API_BASE = "http://localhost:8000/api/v1";

// TODO: show loader on all actions

const AXIOS_CONFIG = {
  timeout: 20000,
  headers: {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  },
}

const axios = axiosBase.create(AXIOS_CONFIG);

const getAuthorizedAxios = () => {
  const state = store.getState();
  const config = {
    ...AXIOS_CONFIG,
    headers: {
      ...AXIOS_CONFIG.headers,
      "X-Auth-Token": state.accessToken && state.accessToken.value
    }
  }
  return axiosBase.create(config)
}

const messageTimeout = 3;


export const showMessage = message => {
  return dispatch => {
    dispatch({type: SHOW_MESSAGE, payload: message});
    setTimeout(() => dispatch({type: HIDE_MESSAGE}), messageTimeout * 1000);
  }
}

export const showLoader = () => {
  return dispatch => {
    dispatch({type: SHOW_LOADER});
  }
}

export const hideLoader = () => {
  return dispatch => {
    dispatch({type: HIDE_LOADER});
  }
}

export const login = (email, password) => {
  return async dispatch => {
    dispatch(showLoader());
    let isSuccess = false;
    try {
      const response = await axios.post(`${API_BASE}/auth/login/`, {email, password});
      isSuccess = true;
      storeTokenIntoStorage(response.data);
      dispatch({type: LOGIN_SUCCESS, payload: response.data});
    } catch (e) {
      switch (e.response.status) {
        case 422: {
          dispatch({
            type: LOGIN_FAILED,
            payload: parsePayloadError(e.response)
          });
          break;
        }
        case 400: {
          dispatch({
            type: LOGIN_FAILED,
            payload: {email: e.response.data.detail}
          });
          break;
        }
        default: {
          dispatch({
            type: LOGIN_FAILED,
            payload: {general: "Unexpected error"}
          });
        }
      }
      dispatch(showMessage("Login failed"));
    }
    dispatch(hideLoader());
    return isSuccess;
  }
}

export const logout = () => {
  return dispatch => {
    deleteTokenFromStorage();
    dispatch({type: LOGOUT})
  }
}


export const register = (
  {
    email,
    password,
    first_name,
    last_name,
    age,
    gender,
    city
  }
) => {
  return async dispatch => {
    dispatch(showLoader());
    const payload = {email, password, first_name, last_name, age, gender, city};
    let isSuccess = false;
    try {
      await axios.post(`${API_BASE}/auth/register/`, payload);
      isSuccess = true;
      dispatch(showMessage("Success!"));
      dispatch({type: REGISTER_SUCCESS});
    } catch (e) {
      dispatch(showMessage("Failed!"));
      switch (e.response.status) {
        case 422: {
          dispatch({
            type: REGISTER_FAILED,
            payload: parsePayloadError(e.response)
          });
          break;
        }
        case 400: {
          dispatch({
            type: REGISTER_FAILED,
            payload: {email: e.response.data.detail}
          });
          break;
        }
        default: {
          dispatch({
            type: REGISTER_FAILED,
            payload: {general: "Unexpected error"}
          });
        }
      }
    }
    dispatch(hideLoader());
    return isSuccess;
  }
}


export const getUser = userId => {
  return async dispatch => {
    let isSuccess = false;
    dispatch(showLoader());
    try {
      const response = await axios.get(`${API_BASE}/users/${userId}/`);
      isSuccess = true;
      dispatch({type: GET_USER_SUCCESS, payload: response.data});
    } catch (e) {
      switch (e.response.status) {
        case 404: {
          dispatch({
            type: GET_USER_FAILED,
            payload: e.response.data.detail
          });
          break;
        }
        default: {
          dispatch({
            type: GET_USER_FAILED,
            payload: {general: "Unexpected error"}
          });
        }
      }
      dispatch(showMessage('Failed'))
    }
    dispatch(hideLoader());
    return isSuccess;
  }
}


export const addHobby = name => {
  return async dispatch => {
    dispatch(showLoader());
    const axios = getAuthorizedAxios();
    try {
      // todo: optimize it
      const createResponse = await axios.post(`${API_BASE}/hobbies/`, {name});
      await axios.put(`${API_BASE}/users/hobbies/${createResponse.data.id}`);
      dispatch({type: ADD_HOBBY_SUCCESS, payload: createResponse.data});
    } catch (e) {
      dispatch(showMessage('Failed'))
    }
    dispatch(hideLoader());
  }
}

export const deleteHobby = id => {
  return async dispatch => {
    dispatch(showLoader());
    const axios = getAuthorizedAxios();
    try {
      await axios.delete(`${API_BASE}/users/hobbies/${id}`);
      dispatch({type: DELETE_HOBBY_SUCCESS, payload: id});
    } catch (e) {
      dispatch(showMessage('Failed'));
    }
    dispatch(hideLoader());
  }
}

// TODO: fix loader many requests
export const getFriends = id => {
  return async dispatch => {
    dispatch(showLoader());
    try {
      const response = await axios.get(`${API_BASE}/users/?friends_of=${id}`,);
      dispatch({type: GET_USERS, payload: response.data});
    } catch (e) {
      dispatch(showMessage('Failed'));
    }
    dispatch(hideLoader());
  }
}

export const clearUser = () => {
  return dispatch => {
    dispatch({type: CLEAR_USER});
  }
}

export const clearUsers = () => {
  return dispatch => {
    dispatch({type: CLEAR_USERS});
  }
}

export const getUsers = (first_name, last_name) => {
  return async dispatch => {
    dispatch(showLoader());
    const query = toQueryString({first_name, last_name});
    try {
      const response = await axios.get(`${API_BASE}/users/?${query}`,);
      dispatch({type: GET_USERS, payload: response.data});
    } catch (e) {
      dispatch(showMessage('Failed'));
    }
    dispatch(hideLoader());
  }
}

