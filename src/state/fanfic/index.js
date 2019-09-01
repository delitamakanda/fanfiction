import { getFanficsPublish, getCategories, getGenres, getEditFanfic, getSubcategories, getFanficsPublishCategory, getFanficsPublishSearch, getChapters, getFanfic, getFanficsPublishByAuthor, getStarredAuthor, getStarredFanfic, postFanfic, getChapter, putFanfic, deleteFanfic, createChapter, updateChapter, deleteChapter } from '@/api/fanfic';

export const namespaced = true;

export const state = {
    categories: [],
    subcategories: [],
    genres: [],
    fanfics: [],
    chapters: [],
    obj_chapter: [],
    obj_fanfic: [],
    starred_authors: [],
    starred_fanfics: [],
};

export const mutations = {
    setChapterTitle (state, data) {
        state.obj_chapter.title = data;
    },
    setChapterDescription (state, data) {
        state.obj_chapter.description = data;
    },
    setChapterText (state, data) {
        state.obj_chapter.text = data;
    },
    setChapterStatus (state, data) {
        state.obj_chapter.status = data;
    },
    setStarredAuthors (state, data) {
        state.starred_authors = data
    },
    setStarredFanfics (state, data) {
        state.starred_fanfics = data
    },
    incrementLike (state, data) {
        state.obj_fanfic.total_likes++
    },
    editGenres (state, data) {
        state.obj_fanfic.genres = data
    },
    editCategory (state, data) {
        state.obj_fanfic.category = data
    },
    editSubCategory (state, data) {
        state.obj_fanfic.subcategory = data
    },
    editTitle(state, data) {
        state.obj_fanfic.title = data
    },
    editSynopsis(state, data) {
        state.obj_fanfic.synopsis = data
    },
    editCredits(state, data) {
        state.obj_fanfic.credits = data
    },
    editDescription(state, data) {
        state.obj_fanfic.description = data
    },
    editClassement(state, data) {
        state.obj_fanfic.classement = data
    },
    editStatus(state, data) {
        state.obj_fanfic.status = data
    },
    decrementLike (state, data) {
        state.obj_fanfic.total_likes--
    },
    setCategories (state, data) {
        state.categories = data
    },
    setSubCategories (state, data) {
        state.subcategories = data
    },
    setGenres (state, data) {
        state.genres = data
    },
    setFanfics (state, data) {
        state.fanfics = data
    },
    createFanfic (state, data) {
        state.fanfics.push(data)
    },
    setChapters (state, data) {
        state.chapters = data
    },
    setChapter (state, data) {
        state.obj_chapter = data
    },
    addChapter (state, data) {
        state.chapters.push(data)
    },
    setFanfic (state, data) {
        state.obj_fanfic = data
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
    async fetchFanfic ({commit}, data) {
        return commit('setFanfic', await getFanfic(data.slug));
    },
    async editFanfic ({commit}, data) {
        return commit('setFanfic', await getEditFanfic(data.id));
    },
    clearFanfic ({commit}) {
        return commit('setFanfic', []);
    },
    async fetchCategories ({commit}) {
        return commit('setCategories', await getCategories());
    },
    async fetchSubCategories ({commit}) {
        return commit('setSubCategories', await getSubcategories());
    },
    async fetchGenres ({commit}) {
        return commit('setGenres', await getGenres());
    },
    async fetchFanficsPublished ({commit}, data) {
        return commit('setFanfics', await getFanficsPublish(data.status));
    },
    async postFanfic ({commit}, data) {
        return commit('createFanfic', await postFanfic(data.title, data.description, data.synopsis, data.credits, data.author, data.genres, data.classement, data.status, data.category, data.subcategory));
    },
    async changeFanfic({commit}, data) {
        return commit('setFanfic', await putFanfic(data.id, data.title, data.description, data.synopsis, data.credits, data.author, data.genres, data.classement, data.status, data.category, data.subcategory));
    },
    async removeFanfic({}, data) {
        await deleteFanfic(data.id);
    },
    async removeChapter({commit}, data) {
        commit('deletedChapter', data);
        await deleteChapter(data.id);
    },
    async fetchFanficsPublishedByAuthor ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishByAuthor(data.status, data.author));
    },
    async fetchFanficsPublishedCategory ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishCategory(data.status, data.categoryId));
    },
    async fetchFanficsPublishedSearch ({commit}, data) {
        return commit('setFanfics', await getFanficsPublishSearch(data.status, data.search_term));
    },
    clearFanficsPublished ({commit}) {
        return commit('setFanfics', [])
    },
    async fetchChapters ({commit}, data) {
        return commit('setChapters', await getChapters(data.id, data.status));
    },
    clearChapters ({commit}) {
        return commit('setChapters', []);
    },
    async fetchStarredAuthors ({commit}, data) {
        return commit('setStarredAuthors', await getStarredAuthor(data.author));
    },
    async fetchStarredFanfics ({commit}, data) {
        return commit('setStarredFanfics', await getStarredFanfic(data.author));
    },
}

export const getters = {};
