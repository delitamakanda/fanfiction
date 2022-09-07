import getters from './authGetters';
import actions from './authActions';
import mutations from './authMutations';

const token = localStorage.getItem('token') as any;

const initialState = token ? { status: { loggedIn: true}, token, error: null} : { status: { loggedIn: false }, token: null, error: null };

const state = initialState;

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
