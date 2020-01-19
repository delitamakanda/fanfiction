import { getCategories, getSubcategories } from '@/api/category';

export const namespaced = true;

export const state = {
    categories: [],
    subcategories: []
};

export const mutations = {
    setCategory (state, data) {
        state.categories = data
    },
    setSubCategory (state, data) {
        state.subcategories = data
    }
};

export const actions = {
    async fetchCategories ({commit}) {
        return commit('setCategory', await getCategories());
    },
    async fetchSubCategories ({commit}) {
        return commit('setSubCategory', await getSubcategories());
    }
};

export const getters = {};
