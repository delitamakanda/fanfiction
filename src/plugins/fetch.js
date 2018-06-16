import state from '../state'
import router from '../router/index'

let baseUrl

function get_cookie(name) {
    var value;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function (c) {
            var m = c.trim().match(/(\w+)=(.*)/);

            if(m !== undefined && m[1] == name) {
                value = decodeURIComponent(m[2]);
            }
        });
    }
    return value;
}

export async function $fetch(url, options) {

    const finalOptions = Object.assign({}, {
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": get_cookie("csrftoken"),
            "Accept": "application/json",
        },
        credentials: 'include',
    }, options)

    const response = await fetch(`${baseUrl}${url}`, finalOptions)
    if (response.ok) {
        const data = await response.json()
        return data
    } else if (response.status === 403) {
        state.user = null
        if (router.currentRoute.matched.some(r => r.meta.private)) {
            router.replace({ name: 'Login', params: {
                wantedRoute: router.currentRoute.fullPath
            }})
        }
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
