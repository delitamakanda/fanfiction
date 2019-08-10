import VueFetch, { $fetch } from '../../plugins/fetch'

export function getNotificationsUser() {
    return $fetch('notifications')
    .then(res => res.results)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function getPages(page) {
    return $fetch(`pages/${page}`)
    .then(res => res)
    .catch(err => {
        console.log(err);
        throw err;
    });
}

export function sendMail(user, subject, message) {
    return $fetch('contact-mail', {
        method: 'post',
        body: JSON.stringify({
            from_email: user,
            subject: subject,
            message: message
        })
    });
}
