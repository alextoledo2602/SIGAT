let nextId = 1

export default {
  namespaced: true,
  state: () => ({
    list: []
  }),
  mutations: {
    ADD_NOTIFICATION(state, notification) {
      state.list.push({
        id: nextId++,
        ...notification
      })
    },
    REMOVE_NOTIFICATION(state, id) {
      state.list = state.list.filter(notification => notification.id !== id)
    }
  },
  actions: {
    add({ commit }, notification) {
      commit('ADD_NOTIFICATION', notification)
      
      // Auto-remove after 5 seconds if not persistent
      if (!notification.persistent) {
        setTimeout(() => {
          commit('REMOVE_NOTIFICATION', notification.id)
        }, 5000)
      }
    },
    remove({ commit }, id) {
      commit('REMOVE_NOTIFICATION', id)
    },
    success({ dispatch }, message) {
      dispatch('add', {
        type: 'success',
        title: 'Éxito',
        message,
        persistent: false
      })
    },
    error({ dispatch }, message) {
      dispatch('add', {
        type: 'error',
        title: 'Error',
        message,
        persistent: true
      })
    },
    // Métodos similares para warning e info
  }
}