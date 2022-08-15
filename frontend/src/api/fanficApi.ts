import api from './api';

const URLS = {
    fetchHomeFanficsUrl: 'browse-fanfics/',
    fetchFanficsUrl: 'fanfics/',
};

export const fetchHomeFanfics = () => {
    return api.get(URLS.fetchHomeFanficsUrl, {
        baseURL: 'api/'
    })
};

export const fetchFanfics = () => {
    return api.get(URLS.fetchFanficsUrl, {
        baseURL: 'api/'
    })
};
