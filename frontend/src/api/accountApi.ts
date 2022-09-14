import api from './api';
import authHeader from './services/auth-header';
const URLS = {
    currentUserUrl: 'user/',
    disableAccountUrl: 'disable-account/',
};

export const getCurrentUser = () => {
    return api.get(URLS.currentUserUrl, {
        baseURL: 'api/',
        headers: authHeader()
    })
};

export const disableAccount = () => {
    return api.get(URLS.disableAccountUrl, {
        baseURL: 'api/',
        headers: authHeader()
    })
};
