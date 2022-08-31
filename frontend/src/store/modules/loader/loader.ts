import getters from './loaderGetters';
import actions from './loaderActions';
import mutations from './loaderMutations';

const state = {
  loading: false,
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
