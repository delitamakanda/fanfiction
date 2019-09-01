import VueFetch, { $fetch } from '../../plugins/fetch'

export function getAllComments(fanficId) {
    return $fetch(`comments/${fanficId}/fanfic`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getChapterComments(fanficId) {
    return $fetch(`comments/fanfic/${fanficId}/list`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function postComChapter (name, email, body, fanfic, chapter) {
    return $fetch('comments-by-chapter/new', {
        method: 'post',
        body: JSON.stringify({
            name: name,
            email: email,
            body: body,
            fanfic: fanfic,
            chapter: chapter
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}

export function postCom (name, email, body, fanfic) {
    return $fetch('comments/new', {
        method: 'post',
        body: JSON.stringify({
            name: name,
            email: email,
            body: body,
            fanfic: fanfic,
        })
    })
    .then(res => res)
    .catch(err => console.log(err))
}
