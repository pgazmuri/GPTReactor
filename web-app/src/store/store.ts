import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { UserState, userSlice } from './UserStore';

const rootReducer = combineReducers({
  user: userSlice.reducer,
  // Add other reducers here
});

const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== 'production',
  // Middleware settings could be added here
});

export type RootState = ReturnType<typeof rootReducer> & {
  user: UserState
};
export type AppDispatch = typeof store.dispatch;
export default store;