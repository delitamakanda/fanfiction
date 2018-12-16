import VueFetch, { $fetch } from '../../plugins/fetch'
import router from '../../router'
import store from '../../store'

export const namespaced = true;

export const state = {
    user: {}
}

export const mutations = {
    user (state, user) {
        state.user = user
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
            if (user) {
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
                }),
            })

            commit('user', user)

            if (user) {
                router.replace({ name: 'Dashboard'})
            }

        } catch (e) {
            console.warn(e);
        }
    },
    register ({commit}) {

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

    user: state => state.user
};
