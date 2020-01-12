import VueFetch, { $fetch } from '../../plugins/fetch'

export function getLexique() {
    return $fetch('help/lexique')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getFaq() {
    return $fetch('help/faq')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}