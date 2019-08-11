import { getFanficsPublish, getCategories, getFanficsPublishCategory, getFanficsPublishSearch } from '@/api/fanfic';

export const namespaced = true;

export const state = {
    categories: [],
    fanfics: []
};

export const mutations = {
    setCategories (state, data) {
        state.categories = data
    },
    setFanfics (state, data) {
        state.fanfics = data
    }
};

export const actions = {
    async fetchCategories ({commit}) {
        return commit('setCategories', await getCategories());
    },
    async fetchFanficsPublished ({commit}, data) {
        return commit('setFanfics', await getFanficsPublish(data.status));
    },
    async fetchFanficsPublishedCategory ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishCategory(data.status, data.categoryId));
    },
    async fetchFanficsPublishedSearch ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishSearch(data.status, data.search_term));
    },
    clearFanficsPublished ({commit}) {
        return commit('setFanfics', [])
    }
}

export const getters = {

};
