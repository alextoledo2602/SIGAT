import axios from 'axios'

export default {
  namespaced: true,
  state: () => ({
    user: null,
    authenticated: false
  }),
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.authenticated = !!user
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/auth/login/', credentials)
        commit('SET_USER', response.data.user)
        return response
      } catch (error) {
        throw error.response.data
      }
    },
    async logout({ commit }) {
      await axios.post('/api/auth/logout/')
      commit('SET_USER', null)
    },
    initialize({ commit }) {
      if (window.userData) {
        commit('SET_USER', window.userData)
      }
    }
  }
}