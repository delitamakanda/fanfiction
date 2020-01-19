import VueFetch, { $fetch } from '../../plugins/fetch'

export function getComments(fanficId, chapterId, isActive) {
    return $fetch(`comments/?fanfic=${fanficId}&chapter=${chapterId}&active=${isActive}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function postComment (name, email, body, fanfic, chapter) {
    return $fetch('comments/', {
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
