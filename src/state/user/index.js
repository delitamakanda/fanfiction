import VueFetch, { $fetch } from '../../plugins/fetch'
import router from '../../router'
import store from '../../store'

export const namespaced = true;

export const state = {
    user: {},
    error: null
}

export const mutations = {
    user (state, user) {
        state.user = user
    },
    error (state, error) {
        state.error = error
    }
};

export const actions = {
    async init ({dispatch}) {
        await dispatch('connect')
    },
    async connect ({commit}) {
        try {
            const user = await $fetch('user')
            commit('user', user)
            if (user && user.id != null) {
                router.replace(router.currentRoute.params.wantedRoute || { name: 'Dashboard'})
            }
        } catch (e) {
            console.warn(e);
        }

    },
    async authenticate ({commit}, data) {

        try {
            const user = await $fetch('login', {
                method: 'POST',
                body: JSON.stringify({
                    username: data.username,
                    password: data.password,
                })
            }).then((user) => {

                commit('user', user)

                if (user) {
                    router.replace({ name: 'Dashboard'})
                    commit('error', null)
                }
            }).catch((error) => {
                commit('error', error.message)
            });

        } catch (e) {
            console.warn(e);
        }
    },
    async register ({commit}, data) {
        try {
            const user = await $fetch('signup', {
                method: 'POST',
                body: JSON.stringify({
                    username: data.username,
                    password: data.password,
                    email: data.email,
                })

            })

            if (user) {
                commit('error', null)
            }

        } catch (e) {
            console.warn(e);
            commit('error', e.message)
        }
    },
    logout ({commit}) {
        commit('user', {})

        $fetch('logout')
        if (router.currentRoute.matched.some(m => m.meta.private)) {
            router.replace({ name: 'Login', params: {wantedRoute: router.currentRoute.fullPath } })
        }
    }
}

export const getters = {
    user: state => state.user,
    error: state => state.error
};
