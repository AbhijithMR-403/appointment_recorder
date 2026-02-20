import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  // Add app-wide state here
  loading: false,
}

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setLoading: (state, action) => {
      state.loading = action.payload
    },
  },
})

export const { setLoading } = appSlice.actions
export default appSlice.reducer
