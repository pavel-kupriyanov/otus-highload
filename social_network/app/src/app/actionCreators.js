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
  GET_USER_FAILED
} from "./actions";

export const API_BASE = "http://localhost:8000/api/v1";

const axios = axiosBase.create({
  timeout: 20000,
  headers: {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json"
  },
});

const messageTimeout = 3;

const parsePayloadError = response => {
  const errors = {};
  response.data.detail.forEach(item => {
    const name = item.loc[item.loc.length - 1];
    errors[name] = item.msg;
  });
  return errors;
}


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
