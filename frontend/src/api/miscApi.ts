import api from './api';
import { requiredParam } from '../helpers/requiredParam';

const URLS = {
    fetchFaqUrl: 'faq/',
    fetchLexiqueUrl: 'lexique/',
};

export const fetchFaq = () => {
    return api.get(URLS.fetchFaqUrl, {
        baseURL: 'api/'
    })
};

export const fetchLexique = () => {
    return api.get(URLS.fetchLexiqueUrl, {
        baseURL: 'api/'
    })
};

export const searchLexique = (query, config = requiredParam('config')) => {
    return api.get(URLS.fetchLexiqueUrl, {
        baseURL: 'api/',
        params: {
            q: query,
        },
        ...config as any,
    });
};
