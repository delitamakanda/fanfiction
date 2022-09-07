import api from './api';
import authHeader from './services/auth-header';
const URLS = {
    signinUrl: 'token',
    signupUrl: 'signup/',
    logoutUrl: 'logout/',
    refreshTokenUrl: 'refresh-token',
};

export const login = ({ username, password }) => {
    return api.post(URLS.signinUrl, 
        { 
            username,
            password
        }, {
        baseURL: 'api/'
    })
};

export const signup = (data) => {
    return api.post(URLS.signupUrl, { ...data }, {
        baseURL: 'api/'
    })
};

export const logout = () => {
    return api.get(URLS.logoutUrl, {
        baseURL: 'api/',
        headers: authHeader()
    })
};

export const refreshToken = (token) => {
    return api.post(URLS.refreshTokenUrl, { refresh: token }, {
        baseURL: 'api/',
    })
};


