import { PayloadAction, createSlice } from "@reduxjs/toolkit";

//example of user state typedef
export interface UserState {
    name: string;
    email: string;
 }

// Example of a user slice
export const userSlice = createSlice({
    name: 'user',
    initialState: {
      name: '',
      email: ''
      // Add other user-related state properties
    },
    reducers: {
      // Define actions like updating user details
      setUser: (state, action: PayloadAction<{ name: string; email: string }>) => {
        state.name = action.payload.name;
        state.email = action.payload.email;
        // Handle other properties
      },
      // Add other reducers as needed
    },
  });