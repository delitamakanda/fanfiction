import { getNotificationsUser, getPages, sendMail } from "@/api/other"

export const namespaced = true;

export const state = {
    news: [],
    notifications: [],
    pages: [],
    contact: null
};

export const mutations = {
    postContactForm (state, data) {
        state.contact = data
    },
    setNotifications(state, data) {
        state.notifications = data;
    },
    setNews(state, data) {
        state.news = data;
    },
    setPages(state, data) {
        state.pages = data;
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
    },
    async fetchPages({commit}, data) {
        return commit('setPages', await getPages(data));
    },
    clearPages({commit}) {
        return commit('setPages', []);
    },
    async sendFormContactEmail({ commit }, data) {
        return commit('postContactForm', await sendMail(data.from_email, data.subject, data.message));
    }
}

export const getters = {};
