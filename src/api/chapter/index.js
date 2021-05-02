import VueFetch, { $fetch } from '../../plugins/fetch'

export function getChapters(fanficId, status) {
    if (typeof status === 'undefined') { return ; }
    return $fetch(`chapters/${fanficId}/list/?status=${status}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getChapter(chapterId) {
    return $fetch(`chapters/${chapterId}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function createChapter(title, description, text, fanficId, authorId, status) {
    return $fetch('chapters/create/', {
        method: 'post',
        body: JSON.stringify({
            title: title,
            description: description,
            text: text,
            fanfic: fanficId,
            author: authorId,
            status: status
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}

export function updateChapter(chapterId, title, description, text, fanficId, authorId, status) {
    return $fetch(`chapters/${chapterId}/`, {
        method: 'put',
        body: JSON.stringify({
            title: title,
            description: description,
            text: text,
            fanfic: fanficId,
            author: authorId,
            status: status
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}
export function deleteChapter(chapterId) {
    return $fetch(`chapters/${chapterId}/`, {
        method: 'delete',
        body: JSON.stringify({
            id: chapterId
        })
    })
    .then(res => res.json())
    .catch(err => console.log(err));
}
