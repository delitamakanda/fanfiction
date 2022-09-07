import * as authTypes from './authTypes';
import AuthService from '../../../api/services/auth.service';

// https://github.com/bezkoder/vue-3-jwt-refresh-token/blob/master/src/services/token.service.js

export default {
    login({ commit}, { username, password }) {
        return AuthService.connect(username, password)
            .then(({ response, error }) => {
                if (response && response.data) {
                    commit(authTypes.loginSuccess, response.data.access);
                    return Promise.resolve(response.data);
                }
                if (error) {
                    commit(authTypes.loginFailure);
                    return Promise.reject(error);
                }
            });
    },
    logout({ commit}) {
        AuthService.logout();
        commit(authTypes.logout);
    },
    signup({ commit }, data) {
        return AuthService.register(data)
            .then(({response, error}) => {
                if (response && response.data) {
                    commit(authTypes.registerSuccess, response.data);
                    return Promise.resolve(response.data);
                }
                if (error) {
                    commit(authTypes.registerFailure);
                    return Promise.reject(error);
                }
            });
    },
    refreshToken({ commit }, token) {
        commit(authTypes.refreshTokenSuccess, token);
    },
    refreshTokenFailure({ commit }, error) {
        commit(authTypes.refreshTokenFailure, error);
    },
};
