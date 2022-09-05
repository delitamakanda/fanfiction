import * as authTypes from './authTypes';

export default {
    loginSuccess(state, token) {
        state.status.loggedIn = true;
        state.token = token;
    },
    loginFailure(state) {
        state.status.loggedIn = false;
        state.token = null;
    },
    logout(state) {
        state.status.loggedIn = false;
        state.token = null;
    },
    registerSuccess(state, token) {
        state.status.loggedIn = false;
    },
    registerFailure(state) {
        state.status.loggedIn = false;
    },
    refreshTokenSuccess(state, token) {
        state.status.loggedIn = true;
        state.token = { ...state.token, ...token };
    },
    refreshTokenFailure(state) {
        state.status.loggedIn = false;
    },
};
