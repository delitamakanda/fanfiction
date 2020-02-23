import { getNews, editNews, addNews } from '@/api/post';

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
        console.log(data)
        // let tmp = state.news.find(c => data.newsId === c.id)
        // Object.assign(tmp, data)
    }
};

export const actions = {
    async addNews({ commit}, data) {
        return commit('postNews', await addNews(data))
    },
    async getNews({ commit }, data) {
        return commit('setNews', await getNews(data.slug))
    },
    async updateNews({ commit}, data) {
        commit('updateNews')
        await editNews(data)
    },
    clearNews({commit}) {
        return commit('setNews', []);
    },
}

export const getters = {};
