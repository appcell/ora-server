import * as actionType from './types';
import axios from 'axios';
import _ from 'lodash';
import { URL, LOGIN, LOGOUT } from '../config/Api';

import { push } from 'connected-react-router'

export const setToken = (data) => {
  return {
    type: actionType.SET_TOKEN,
    data
  }
}

export const unsetToken = () => {
  return {
    type: actionType.UNSET_TOKEN
  }
}

export function InvalidCredentialsException(message) {
    this.message = message;
    this.name = 'InvalidCredentialsException';
}

export function login(email, password, closeModal) {
  return (dispatch, getState) => {
    let csrf_token = window.csrf_token
    if ( getState().login.authentication_token !== "" ){
      dispatch(push('/route/home'))
      closeModal()
    } else {
    return axios
      .post(URL + LOGIN, {
        email,
        password,
        csrf_token
      })
      .then(function (response) {
        let data = {
          ...response.data.response.user,
          email: email
        }
        dispatch(setToken(data));
        dispatch(push('/route/home'))
        closeModal()
      })
      .catch(function (error) {
        // raise different exception if due to invalid credentials
        if (_.get(error, 'response.status') === 400) {
          throw new InvalidCredentialsException(error);
        }
        throw error;
      });
    }
  }
}

export function logout() {
  return (dispatch, getState) => {
    return axios
      .get(URL + LOGOUT)
      .then(function (response) {
        dispatch(unsetToken())
        dispatch(push('/'))
      })
      .catch(function (error) {
        // raise different exception if due to invalid credentials
        if (_.get(error, 'response.status') === 400) {
          console.log('logout error')
        }
      });
  }
}