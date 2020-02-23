import VueFetch, { $fetch } from '../../plugins/fetch'

export function getNews(postSlug) {
    return $fetch(`posts/${postSlug}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function editNews(data) {
    return $fetch(`posts/${data.id}/edit`, {
        method: 'put',
        body: JSON.stringify({
            user: data.user,
            header: data.header,
            title: data.title,
            content: data.content,
            tags: data.tags
        })
    })
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function addNews(data) {
    return $fetch(`posts/create`, {
        method: 'post',
        body: JSON.stringify({
            user: data.user,
            header: data.header,
            title: data.title,
            content: data.content,
            tags: data.tags
        })
    })
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}