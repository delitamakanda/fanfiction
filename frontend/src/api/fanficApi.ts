import api from './api';
import { requiredParam } from '../helpers/requiredParam';

const URLS = {
    fetchHomeFanficsUrl: 'browse-fanfics/',
    fetchFanficsUrl: 'fanfics/',
};

export const fetchHomeFanfics = () => {
    return api.get(URLS.fetchHomeFanficsUrl, {
        baseURL: 'api/'
    })
};

export const searchFanfics = (query, config = requiredParam('config')) => {
    return api.get(URLS.fetchFanficsUrl, {
        baseURL: 'api/',
        params: {
            q: query,
        },
        ...config as any,
    });
};
