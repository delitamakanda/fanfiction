import { getComments, getAllComments, postComment } from '@/api/comment';
import * as _ from 'lodash';

export const namespaced = true;

export const state = {
    comments: [],
};

export const mutations = {
    setComments (state, data) {
        state.comments = data
    },
    addComment (state, data) {
        state.comments.push(data)
    },
};

export const actions = {
    async postComment ({commit}, data) {
        return commit('addComment', await postComment(data.name, data.email, data.body, data.fanfic, data.chapter));
    },
    async fetchAllComments ({commit}, data) {
        return commit('setComments', await getComments(data.id, data.isActive));
    },
    async fetchComments ({commit}) {
        return commit('setComments', await getAllComments());
    },
    async clearComments ({commit}) {
        state.comments = []
    },
}

export const getters = {
    commentsCount: state => {
        return state.comments.length
    },
    commentsByAuthor: (state) => (user) => {
        return state.comments.filter(c => c.fanfic.author.id === user.id);
    }
};
