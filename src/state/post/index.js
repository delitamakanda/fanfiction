import { getNews, fetchNews, deleteNews, editNews, addNews } from '@/api/post';

export const namespaced = true;

export const state = {
    news: []
};


export const mutations = {
    setNews(state, data) {
        state.news = data;
    },
    postNews(state, data) {
        state.news.push(data)
    },
    updateNews(state, data) {
        state.news = data
    },
    deleteNews(state, data) {
        let tmp = state.news.filter(c => c.id !== data)
        state.news = tmp
    }
};

export const actions = {
    async fetchNews({ commit }) {
        return commit('setNews', await fetchNews())
    },
    async addNews({ commit}, data) {
        return commit('postNews', await addNews(data))
    },
    async getNews({ commit }, data) {
        return commit('setNews', await getNews(data.slug))
    },
    async updatePost({ commit}, data) {
        commit('updateNews', data)
        await editNews(data)
    },
    async deletePost({ commit}, data) {
        commit('deleteNews', data)
        await deleteNews(data)
    },
    clearNews({commit}) {
        return commit('setNews', []);
    },
}

export const getters = {};
