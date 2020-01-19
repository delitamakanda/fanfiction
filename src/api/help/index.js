import VueFetch, { $fetch } from '../../plugins/fetch'

export function getLexique() {
    return $fetch('lexique')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFaq() {
    return $fetch('faq')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}