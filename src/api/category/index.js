import VueFetch, { $fetch } from '../../plugins/fetch'

export function getCategories() {
    return $fetch('category')
    .then(res => res)
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
