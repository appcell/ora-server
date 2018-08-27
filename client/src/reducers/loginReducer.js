import * as actionType from '../actions/types';

const loginInitialState = {
	authentication_token: '',
	id: '',
	email: ''
};

const login = (state = loginInitialState, action) => {
  switch(action.type) {
    case actionType.SET_TOKEN:
      return action.data
    case actionType.UNSET_TOKEN:
    	return loginInitialState
    default:
      return state;
  }
}

export default login;