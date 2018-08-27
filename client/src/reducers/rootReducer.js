import { combineReducers } from 'redux';
import login from './loginReducer';

const appReducer = combineReducers({
  login,
})

const rootReducer = (state, action) => {
  return appReducer(state, action);
}

export default rootReducer;