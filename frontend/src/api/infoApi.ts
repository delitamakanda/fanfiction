import api from './api';
import { requiredParam } from '../helpers/requiredParam';

const URLS = {
    contactMailUrl: 'contact-mail/',
    fetchPagesUrl: 'pages/',
    fetchPageUrl: (slug) =>`pages/${slug}/html/`,
    fetchPoststUrl: 'posts/',
    fetchPostUrl: (slug) => `posts/${slug}/`,
};

export const contactMail = (data) => {
    return api.post(URLS.contactMailUrl, data, {
        baseURL: 'api/',
    })
};

export const fetchPages = () => {
    return api.get(URLS.fetchPagesUrl, {
        baseURL: 'api/',
    })
};

export const fetchPage = (slug) => {
    return api.get(URLS.fetchPageUrl(slug), {
        baseURL: 'api/',
    })
};

export const fetchPosts = () => {
    return api.get(URLS.fetchPoststUrl, {
        baseURL: 'api/',
    })
};

export const fetchPost = (slug) => {
    return api.get(URLS.fetchPostUrl(slug), {
        baseURL: 'api/',
    } )
};
