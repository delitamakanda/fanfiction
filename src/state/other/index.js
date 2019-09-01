import { getNotificationsUser, getPages, sendMail, followFanfic, disFollowFanfic, followAuthor, disFollowAuthor, preventAbuse, favorite, unfavorite, getFollowAuthor, getFollowFanfic } from "@/api/other"

export const namespaced = true;

export const state = {
    news: [],
    notifications: [],
    pages: [],
    contact: null,
    feedback: null,
    favorited: null,
    followedStory: [],
    followedAuthor: [],
    followStory: null,
    followAuthor: null,
    followUserId: null,
    followStoryId: null
};

export const mutations = {
    setFollowUserId (state, data) {
        state.followUserId = data
    },
    setFollowStoryId (state, data) {
        state.followStoryId = data
    },
    postFollowAuthor (state, data) {
        state.followAuthor = data
    },
    postFollowStory (state, data) {
        state.followStory = data
    },
    setFollowAuthor (state, data) {
        state.followedAuthor = data
    },
    setFollowStory (state, data) {
        state.followedStory = data
    },
    postFavoritedByUser (state, data) {
        state.favorited = data
    },
    postUnFavoritedByUser (state, data) {
        state.favorited = data
    },
    postContactForm (state, data) {
        state.contact = data
    },
    postFeedbackForm (state, data) {
        state.feedback = data
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
    async addFollowStory({commit}, data) {
        commit('postFollowStory')
        await followFanfic(data.from_user, data.to_fanfic)
        .then(res => {
            commit('setFollowStoryId', res.id)
        })
        .catch(err => console.log(err));
    },
    async removeFollowStory({commit}, data) {
        return commit('postFollowStory', await disFollowFanfic(data.id));
    },
    async addFollowAuthor({commit}, data) {
        commit('postFollowAuthor')
        await followAuthor(data.user_from, data.user_to)
        .then(res => {
            commit('setFollowUserId', res.id)
        })
        .catch(err => console.log(err));
    },
    async removeFollowAuthor({commit}, data) {
        return commit('postFollowAuthor', await disFollowAuthor(data.id));
    },
    async fetchFollowStory({commit}) {
        return commit('setFollowStory', await getFollowFanfic());
    },
    async fetchFollowAuthor({commit}) {
        return commit('setFollowAuthor', await getFollowAuthor());
    },
    clearFollowAuthor({commit}) {
        return commit('setFollowAuthor', [])
    },
    clearFollowStory({commit}) {
        return commit('setFollowStory', [])
    },
    async postUnfavorited({commit}, data) {
        return commit('postUnFavoritedByUser', await unfavorite(data.id, data.user));
    },
    async postFavorited({commit}, data) {
        return commit('postFavoritedByUser', await favorite(data.id, data.user));
    },
    clearNews({commit}) {
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
    },
    async sendFormPreventAbuse({commit}, data) {
        return commit('postFeedbackForm', await preventAbuse(data.id));
    }
}

export const getters = {};
