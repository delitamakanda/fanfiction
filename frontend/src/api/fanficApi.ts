import api from './api';
import { requiredParam } from '../helpers/requiredParam';

const URLS = {
    fetchHomeFanficsUrl: 'browse-fanfics/',
    fetchFanficsUrl: 'fanfics/?status=publié',
    fetchFanficDetailUrl: (slug) => `fanfics/${slug}/detail/`,
    fetchChaperslUrl: (id: number) => `chapters/${id}/list/`,
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

export const fetchChaptersList = (id) => {
    return api.get(URLS.fetchChaperslUrl(id), {
        baseURL: 'api/'
    })
};

export const searchFanfics = (query, config = requiredParam('config'), pageNumber = 1) => {
    return api.get(URLS.fetchFanficsUrl, {
        baseURL: 'api/',
        params: {
            q: query,
            page: pageNumber
        },
        ...config as any,
    });
};
