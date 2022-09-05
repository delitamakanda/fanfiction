import getters from './userGetters';
import actions from './userActions';
import mutations from './userMutations';

const state = {
    user: null,
}

export default {
    namespaced: true,
    state,
    actions,
    getters,
    mutations,
};
