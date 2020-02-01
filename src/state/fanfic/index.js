import { getFanficsPublish, getGenres, getEditFanfic, getFanficsPublishCategory, getFanficsPublishSearch, getFanfic, getFanficsPublishByAuthor, getStarredAuthor, getStarredFanfic, postFanfic, putFanfic, deleteFanfic, getClassement, getStatus } from '@/api/fanfic';

export const namespaced = true;

export const state = {
    genres: [],
    status: [],
    classement: [],
    fanfics: [],
    obj_fanfic: {},
    starred_authors: [],
    starred_fanfics: [],
};

export const mutations = {
    setStarredAuthors (state, data) {
        state.starred_authors = data
    },
    setStarredFanfics (state, data) {
        state.starred_fanfics = data
    },
    incrementLike (state, data) {
        state.obj_fanfic.total_likes++
    },
    decrementLike (state, data) {
        state.obj_fanfic.total_likes--
    },
    setGenres (state, data) {
        state.genres = data
    },
    setClassement (state, data) {
        state.classement = data
    },
    setStatus (state, data) {
        state.status = data
    },
    setFanfics (state, data) {
        state.fanfics = data
    },
    createFanfic (state, data) {
        state.fanfics.push(data)
    },
    setFanfic (state, data) {
        state.obj_fanfic = data
    }
};

export const actions = {
    async fetchFanfic ({commit}, data) {
        return commit('setFanfic', await getFanfic(data.slug));
    },
    async editFanfic ({commit}, data) {
        return commit('setFanfic', await getEditFanfic(data.id));
    },
    clearFanfic ({commit}) {
        return commit('setFanfic', []);
    },
    async fetchGenres ({commit}) {
        return commit('setGenres', await getGenres());
    },
    async fetchStatus ({commit}) {
        return commit('setStatus', await getStatus());
    },
    async fetchClassement ({commit}) {
        return commit('setClassement', await getClassement());
    },
    async fetchFanficsPublished ({commit}, data) {
        return commit('setFanfics', await getFanficsPublish(data.status));
    },
    async postFanfic ({commit}, data) {
        console.log(data)
        return commit('createFanfic', await postFanfic(data.title, data.description, data.synopsis, data.credits, data.author, data.genres, data.classement, data.status, data.category, data.subcategory));
    },
    async changeFanfic({commit}, data) {
        return commit('setFanfic', await putFanfic(data.id, data.title, data.description, data.synopsis, data.credits, data.author, data.genres, data.classement, data.status, data.category, data.subcategory));
    },
    async removeFanfic({}, data) {
        await deleteFanfic(data.id);
    },
    async fetchFanficsPublishedByAuthor ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishByAuthor(data.status, data.author));
    },
    async fetchFanficsPublishedCategory ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishCategory(data.status, data.categoryId));
    },
    async fetchFanficsPublishedSearch ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishSearch(data.status, data.search_term));
    },
    clearFanficsPublished ({commit}) {
        return commit('setFanfics', [])
    },
    async fetchStarredAuthors ({commit}, data) {
        return commit('setStarredAuthors', await getStarredAuthor(data.author));
    },
    async fetchStarredFanfics ({commit}, data) {
        return commit('setStarredFanfics', await getStarredFanfic(data.author));
    },
}

export const getters = {};
