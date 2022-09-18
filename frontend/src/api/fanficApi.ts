import api from './api';
import { requiredParam } from '../helpers/requiredParam';

const URLS = {
    fetchHomeFanficsUrl: 'browse-fanfics/',
    fetchFanficsUrl: 'fanfics/?status=publié',
    fetchFanficDetailUrl: (slug) => `fanfics/${slug}/detail/`,
};

export const fetchHomeFanfics = () => {
    return api.get(URLS.fetchHomeFanficsUrl, {
        baseURL: 'api/'
    })
};

export const fetchFanficDetail = (slug) => {
    return api.get(URLS.fetchFanficDetailUrl(slug), {
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
