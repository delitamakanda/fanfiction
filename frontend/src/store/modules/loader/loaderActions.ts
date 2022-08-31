import * as loaderTypes from './loaderTypes';

export default {
    show({ commit }) {
        commit('show');
    },
    hide({ commit }) {
        commit('hide');
    },
};
