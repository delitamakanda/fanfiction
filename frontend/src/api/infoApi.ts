import api from './api';

const URLS = {
    fetchPagesUrl: 'pages/',
    fetchPageUrl: (slug) => `pages/${slug}/html/`,
    fetchPoststUrl: 'posts/',
    fetchPostUrl: (slug) => `posts/${slug}/`,
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
    })
};
