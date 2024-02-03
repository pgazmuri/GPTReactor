import { PayloadAction, createSlice } from "@reduxjs/toolkit";

// Example of user state typedef
export interface UserState {
    name: string;
    email: string;
    // Add other user-related state properties as needed
}

// Example of a user slice with mock data in initialState
export const userSlice = createSlice({
    name: 'user',
    initialState: {
      name: 'John Doe', // Mock data for name
      email: 'john.doe@example.com' // Mock data for email
      // Retain other user-related state properties if any
    },
    reducers: {
      // Define actions like updating user details
      setUser: (state, action: PayloadAction<{ name: string; email: string }>) => {
        state.name = action.payload.name;
        state.email = action.payload.email;
        // Handle other properties as needed
      },
      // Add other reducers as needed
    },
});

// Export actions for use in components
export const { setUser } = userSlice.actions;

// Export the reducer for use in the store configuration
export default userSlice.reducer;