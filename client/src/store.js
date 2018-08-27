import { compose, createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger';
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import { createBrowserHistory } from 'history'
import { connectRouter, routerMiddleware } from 'connected-react-router'

import rootReducer from './reducers/rootReducer';

const history = createBrowserHistory()

const loggerMiddleware = createLogger()

const persistConfig = {
  key: 'root',
  storage: storage,
  blacklist: ['router'],
}

const connectedRouter = connectRouter(history)(rootReducer)

const persistedReducer = persistReducer(persistConfig, connectedRouter)

const store = createStore(
  persistedReducer,
  compose(
    applyMiddleware(
      thunkMiddleware,
      routerMiddleware(history), 
      loggerMiddleware,
    )
  )
);

let persistor = persistStore(store)
window.persistor = persistor

export { store, history, persistor };