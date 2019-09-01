import VueFetch, { $fetch } from '../../plugins/fetch'

export function getFanficsPublish(status) {
    if (typeof status === 'undefined') { return ; }
    return $fetch(`fanfics/v1/?status=${status}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishByAuthor(status, authorUsername) {
    if (typeof status === 'undefined') { return ; }
    return $fetch(`fanfics/v1/${authorUsername}?status=${status}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishCategory(status, categoryId) {
    return $fetch(`fanfics/v1/?status=${status}&category=${categoryId}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishSearch(status, searchTerm) {
    if (typeof status === 'undefined') { return ; }
    return $fetch(`fanfics/v1/?status=${status}&search=${searchTerm}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getCategories() {
    return $fetch('category')
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getChapters(fanficId, status) {
    return $fetch(`chapters/${fanficId}/list?status=${status}`)
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

export function getFanfic(slug) {
    return $fetch(`fanfics/v1/${slug}/detail`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getEditFanfic(id) {
    return $fetch(`fanfics/${id}/detail`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getStarredAuthor(authorUsername) {
    return $fetch(`following-authors/${authorUsername}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getStarredFanfic(authorUsername) {
    return $fetch(`following-stories/${authorUsername}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getGenres() {
    return $fetch('genres')
    .then(res => res[0]['genres'])
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getSubcategories() {
    return $fetch('subcategory')
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function putFanfic(fanficId, title, description, synopsis, credits, userId, genre, classement, status, category, subcategory) {
    return $fetch(`fanfics/${fanficId}/detail`, {
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

export function deleteFanfic(fanficId) {
    return $fetch(`fanfics/${fanficId}/detail`, {
        method: 'delete',
        body: JSON.stringify({
            id: fanficId
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

export function createChapter(title, description, text, fanficId, authorId, status) {
    return $fetch('chapters/create', {
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
    return $fetch(`chapters/${chapterId}`, {
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
    return $fetch(`chapters/${chapterId}`, {
        method: 'delete',
        body: JSON.stringify({
            id: chapterId
        })
    })
    .then(res => res.json())
    .catch(err => console.log(err));
}
