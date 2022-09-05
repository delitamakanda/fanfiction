import api from './api';
import authHeader from './services/auth-header';
const URLS = {
    currentUserUrl: 'user',
};

export const getCurrentUser = () => {
    return api.post(URLS.currentUserUrl, {
        baseURL: 'api/',
        headers: authHeader()
    })
};
