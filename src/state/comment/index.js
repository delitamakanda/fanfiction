import { getAllComments, getChapterComments, postComChapter, postCom } from '@/api/comment';
import * as _ from 'lodash';

export const namespaced = true;

export const state = {
    all_comments: [],
    chapter_comments: [],
    follow_stories: []
};

export const mutations = {
    setAllComments (state, data) {
        state.all_comments = data
    },
    setChapterComments (state, data) {
        state.chapter_comments = data
    },
    updateComment (state, data) {
        state.all_comments.push(data)
    },
    updateChapterComment (state, data) {
        state.all_comments.push(data)
        state.chapter_comments.push(data)
    },
    addChapterComment (state, data) {
        state.chapter_comments.push(data)
    }
};

export const actions = {
    async postComment ({commit}, data) {
        return commit('updateComment', await postCom(data.name, data.email, data.body, data.fanfic));
    },
    async postChapterCom ({commit}, data) {
        return commit('updateChapterComment', await postComChapter(data.name, data.email, data.body, data.fanfic, data.chapter));
    },
    async fetchAllComments ({commit}, data) {
        return commit('setAllComments', await getAllComments(data.id));
    },
    async clearChapterComments ({commit}, data) {
        return commit('setChapterComments', []);
    },
    async fetchChapterComments ({commit}, data) {
        return commit('setChapterComments', await getChapterComments(data.id));
    },
}

export const getters = {
    commentsCount: state => {
        return (state.all_comments != undefined ? state.all_comments
        .filter( a => a.in_reply_to === null) : []).length
    },
    allComments: state => {
        let aComments = []
        aComments = _.concat(aComments, state.all_comments, state.chapter_comments)

        return _.uniqBy(aComments, 'id');
    },
    commentsChapterCount: (state) => (chapterId) => {
        return (state.chapter_comments != undefined ? state.chapter_comments
        .filter(c => (c.in_reply_to === null) && (c.chapter.id === chapterId)) : []).length
    },
    getAllChapersComm: state => state.chapter_comments
};
