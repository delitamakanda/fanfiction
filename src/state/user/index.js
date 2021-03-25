import VueFetch, { $fetch } from '../../plugins/fetch'
import router from '../../router'
import store from '../../store'
import { getProfile, editProfile, editPhoto, deletePhoto, editUserEmail, changePassword, deleteSocialAccount, createSocialAccount } from '../../api/user'

export const namespaced = true;

export const state = {
    user: {},
    error: null,
    profile: []
}

export const mutations = {
    user (state, user) {
        state.user = user
    },
    error (state, error) {
        state.error = error
    },
    setProfile (state, data) {
        state.profile = data
    },
    setUserEmail (state, data) {
        state.user.email = data
    },
    setSocialAccount (state, data) {
        state.profile.social.push(data)
    },
    editProfile(state, data) {
        state.profile = data
    },
    editPhoto(state, data) {
        state.profile.photo = data.photo
    },
    deleteAccount (state, data) {
        let tmp = state.profile.social.filter(c => c.id !== data)
        state.profile.social = tmp
    },
    deleteProfilePhoto (state) {
        state.profile.photo = null
    }
};

export const actions = {
    async init ({dispatch}) {
        await dispatch('connect')
    },
    async fetchProfileUser({ commit }, data) {
        return commit('setProfile', await getProfile(data.username));
    },
    async editProfileUser({commit}, data) {
        commit('editProfile', data)
        await editProfile(data.username, data.date_of_birth, data.bio)
    },
    async editPhotoUser({commit}, data) {
        commit('editPhoto', data)
        await editPhoto(data.username, data.photo)
    },
    async createSocialAccount({ commit }, data) {
        return commit('setSocialAccount', await createSocialAccount(data.account, data.network, data.nichandle, data.user))
    },
    async deleteSocialAccount({ commit }, data) {
        commit('deleteAccount', data.id)
        await deleteSocialAccount(data.id)
    },
    async deleteProfilePhoto({commit}, data) {
        commit('deleteProfilePhoto')
        await deletePhoto(data.id)
    },
    async changeUserMail({commit}, data) {
        commit('setUserEmail', data.email)
        await editUserEmail(data.userId, data.email);
    },
    async updatePassword({}, data) {
        await changePassword(data.old_password, data.new_password);
    },
    async connect ({commit}) {
        try {
            const user = await $fetch('user/')
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
            const user = await $fetch('login/', {
                method: 'POST',
                body: JSON.stringify({
                    username: data.username,
                    password: data.password,
                })
            }).then((user) => {

                commit('user', user)

                if (user) {
                    router.replace({ name: 'Dashboard'})
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
            const user = await $fetch('signup/', {
                method: 'POST',
                body: JSON.stringify({
                    username: data.username,
                    password: data.password,
                    email: data.email,
                })

            })

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
    },
    clearError({commit}) {
        commit('error', null)
    },
    async removeAccount({commit}) {

        try {

            const result = await $fetch('disable-account/')

            if ((result.status === 'ok') && (router.currentRoute.matched.some(m => m.meta.private))) {
                commit('user', {})
                router.replace({ name: 'List', params: {wantedRoute: router.currentRoute.fullPath } })
            }
        } catch (e) {
            console.log(e)
        }
    }
}

export const getters = {
    user: state => state.user,
    error: state => state.error
};
