import api from './api';
import authHeader from './services/auth-header';
const URLS = {
    currentUserUrl: 'user/',
    disableAccountUrl: 'disable-account/',
    viewProfileUrl: (username) => `users/${username}/profile/`,
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

export const getCurrentProfile = (username: string) => {
    return api.get(URLS.viewProfileUrl(username), {
        baseURL: 'api/',
    })
};
