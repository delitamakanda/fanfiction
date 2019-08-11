import VueFetch, { $fetch } from '../../plugins/fetch'

export function getFanficsPublish(status) {
    return $fetch(`fanfics/v1?status=${status}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishCategory(status, categoryId) {
    return $fetch(`fanfics/v1?status=${status}&category=${categoryId}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFanficsPublishSearch(status, searchTerm) {
    return $fetch(`fanfics/v1?status=${status}&search=${searchTerm}`)
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
