import { getNotificationsUser } from "@/api/getNotificationsUser"

export const namespaced = true;

export const state = {
    news: [],
    notifications: []
};

export const mutations = {
    setNotifications(state, data) {
        state.notifications = data;
    },
    setNews(state, data) {
        state.news = data;
    }
};

export const actions = {
    getNews({commit}) {
        return commit('setNews', []);
    },
    clearNotifications({commit}) {
        return commit('setNotifications', []);
    },
    async getNotifications({commit}) {
        return commit('setNotifications', await getNotificationsUser());
    }
}

export const getters = {};
