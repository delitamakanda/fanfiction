import 'whatwg-fetch'

import state from '../state'
import store from '../store'
import router from '../router/index'
import get_cookie from '../cookie'

let baseUrl


export async function $fetch(url, options) {

    const finalOptions = Object.assign({}, {
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": get_cookie("csrftoken"),
            "Accept": "application/json",
            'Access-Control-Allow-Origin': '*'
        },
        credentials: 'include',
    }, options)

    const response = await fetch(`${baseUrl}${url}`, finalOptions)
    if (response.ok) {
        const data = await response.json()
        return data
    } else if (response.status === 403) {
        /*state.user = null
        if (router.currentRoute.matched.some(r => r.meta.private)) {
            router.replace({ name: 'Login', params: {
                wantedRoute: router.currentRoute.fullPath
            }})
        }*/
        store.dispatch('user/logout')
    } else {
        const message = await response.text()
        const error = new Error(message)
        error.response = response
        throw error
    }
}

export default {
    install (Vue, options) {

        baseUrl = options.baseUrl

        Vue.prototype.$fetch = $fetch
    },
}
