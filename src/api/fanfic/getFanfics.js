import VueFetch, { $fetch } from '../../plugins/fetch'

export function getFanficsPublish() {
    return $fetch('fanfics/v1')
    .then(res => {
        console.log(res)
    })
    .catch(err => {
        console.log(err);
        throw err;
    });
}
