import { getFanficsPublish, getGenres, getEditFanfic, getFanficsPublishCategory, getFanficsPublishSearch, getFanfic, getFanficsPublishByAuthor, getStarredAuthor, getStarredFanfic, postFanfic, putFanfic, deleteFanfic } from '@/api/fanfic';

export const namespaced = true;

export const state = {
    genres: [],
    status: [],
    classement: [],
    fanfics: [],
    obj_fanfic: [],
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
    editGenres (state, data) {
        state.obj_fanfic.genres = data
    },
    editTitle(state, data) {
        state.obj_fanfic.title = data
    },
    editSynopsis(state, data) {
        state.obj_fanfic.synopsis = data
    },
    editCredits(state, data) {
        state.obj_fanfic.credits = data
    },
    editDescription(state, data) {
        state.obj_fanfic.description = data
    },
    editClassement(state, data) {
        state.obj_fanfic.classement = data
    },
    editStatus(state, data) {
        state.obj_fanfic.status = data
    },
    decrementLike (state, data) {
        state.obj_fanfic.total_likes--
    },
    setGenres (state, data) {
        state.genres = data
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
    async fetchFanficsPublished ({commit}, data) {
        return commit('setFanfics', await getFanficsPublish(data.status));
    },
    async postFanfic ({commit}, data) {
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
