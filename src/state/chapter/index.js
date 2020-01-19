import { getChapter, createChapter, getChapters, updateChapter, deleteChapter } from '@/api/chapter';

export const namespaced = true;

export const state = {
    chapters: [],
    chapter: {}
};

export const mutations = {
    setChapters (state, data) {
        state.chapters = data
    },
    setChapter (state, data) {
        state.chapter = data
    },
    addChapter (state, data) {
        state.chapters.push(data)
    },
    editedChapter (state, data) {
        let tmp = state.chapters.find(c => data.chapterId === c.id)
        Object.assign(tmp, data)
    },
    deletedChapter (state, data) {
        let tmp = state.chapters.filter(c => c.id !== data.id)
        state.chapters = tmp
    }
};

export const actions = {
    async putChapter({commit}, data) {
        commit('editedChapter', data)
        await updateChapter(data.chapterId, data.title, data.description,data.text,data.fanfic, data.author, data.status);
    },
    async postChapter({commit}, data) {
        return commit('addChapter', await createChapter(data.title,data.description,data.text,data.fanfic, data.author,data.status));
    },
    async fetchChapter ({commit}, data) {
        return commit('setChapter', await getChapter(data.id));
    },
    clearChapter ({commit}) {
        return commit('setChapter', []);
    },
    async removeChapter({commit}, data) {
        commit('deletedChapter', data);
        await deleteChapter(data.id);
    },
    async fetchChapters ({commit}, data) {
        return commit('setChapters', await getChapters(data.id, data.status));
    },
    clearChapters ({commit}) {
        return commit('setChapters', []);
    },
};
