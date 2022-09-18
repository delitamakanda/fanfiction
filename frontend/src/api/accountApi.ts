import api from './api';
import authHeader from './services/auth-header';
const URLS = {
    currentUserUrl: 'user/',
    disableAccountUrl: 'disable-account/',
    viewProfileUrl: (username) => `users/${username}/profile/`,
    followStoriesUrl: (username) => `follow-stories/${username}/`,
    followAuthorsUrl: (username) => `follow-user/${username}/`,
    fanficsByAuthorUrl: (username, status) => `fanfics/${username}/?status=${status}`,
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

export const getFollowAuthors = (username: string) => {
    return api.get(URLS.followAuthorsUrl(username), {
        baseURL: 'api/',
    })
};

export const getFollowStories = (username: string) => {
    return api.get(URLS.followStoriesUrl(username), {
        baseURL: 'api/',
    })
};

export const getFanficsByAuthor = (username, status) => {
    return api.get(URLS.fanficsByAuthorUrl(username, status), {
        baseURL: 'api/',
    })
};
