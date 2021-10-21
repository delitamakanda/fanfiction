import VueFetch, { $fetch } from '../../plugins/fetch'

export function getFanficsPublish(status, offset, categoryId) {
    if (typeof status === undefined) { return ; }
    return $fetch(`fanfics/?limit=4&offset=${offset}&status=${status}&category=${categoryId}`)
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishByAuthor(status, authorUsername) {
    if (typeof status === undefined) { return ; }
    return $fetch(`fanfics/${authorUsername}/?status=${status}`)
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishCategory(status, categoryId) {
    return $fetch(`fanfics/?status=${status}&category=${categoryId}`)
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishSearch(status, searchTerm) {
    if (typeof status === undefined) { return ; }
    return $fetch(`fanfics/?q=${searchTerm}&status=${status}`)
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanfic(slug) {
    return $fetch(`fanfics/${slug}/detail/`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getEditFanfic(id) {
    return $fetch(`fanfics/${id}/fanfic-detail/`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getStarredAuthor(authorUsername) {
    return $fetch(`following-authors/${authorUsername}/`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getStarredFanfic(authorUsername) {
    return $fetch(`following-stories/${authorUsername}/`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getGenres() {
    return $fetch('genres/')
    .then(res => {
        return res[0].genres;
    })
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getClassement() {
    return $fetch('classement/')
    .then(res => res[0].classement)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getStatus() {
    return $fetch('status/')
    .then(res => res[0].status)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function putFanfic(id, title, description, synopsis, credits, userId, genre, classement, status, category, subcategory) {
    return $fetch(`fanfics/${id}/fanfic-detail/`, {
        method: 'put',
        body: JSON.stringify({
            title: title,
            description: description,
            synopsis: synopsis,
            credits: credits,
            author: userId,
            genres: genre,
            classement: classement,
            status: status,
            category: category,
            subcategory: subcategory
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}

export function deleteFanfic(id) {
    return $fetch(`fanfics/${id}/fanfic-detail/`, {
        method: 'delete',
        body: JSON.stringify({
            id: id
        })
    })
    .then(res => res.json())
    .catch(err => console.log(err));
}

export function postFanfic(title, description, synopsis, credits, userId, genre, classement, status, category, subcategory) {
    return $fetch('fanfics/', {
        method: 'post',
        body: JSON.stringify({
            title: title,
            description: description,
            synopsis: synopsis,
            credits: credits,
            author: userId,
            genres: genre,
            classement: classement,
            status: status,
            category: category,
            subcategory: subcategory
        })
    })
    .then(res => res)
    .catch(err => console.log(err));
}
