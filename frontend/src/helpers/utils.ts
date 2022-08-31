export const getRandomUUID = () => 
    Math.random().toString(36).toString().substring(2, 15) +
    Math.random().toString(36).toString().substring(2, 15);


export const options_FR = {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
};

export const options_US = {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
};

export const formatDate = (date, options) => {
    return new Intl.DateTimeFormat('fr-FR', options).format(date);
};

const divisions = [
    { amount: 60, name: 'seconds' },
    { amount: 60, name: 'minutes' },
    { amount: 24, name: 'hours' },
    { amount: 7, name: 'days' },
    { amount: 4.34524, name: 'weeks' },
    { amount: 12, name: 'months' },
    { amount: Number.POSITIVE_INFINITY, name: 'years' },
];

export const formatRelativeDate = (date) => {
    const dateTime = new Date(date.split('T')[0]);
    const deltaDays = Math.round((dateTime.getTime() - Date.now()) / (1000 * 3600 * 24));
    if (deltaDays === 0) {
        let duration = (dateTime.getTime() - new Date().getTime()) / 1000;
        for (let i = 0; i <= divisions.length; i++) {
            const division = divisions[i];
            if (Math.abs(duration) < division.amount) {
                return new Intl.RelativeTimeFormat('fr', {
                    numeric: 'auto',
                }).format(Math.round(duration), division.name as any);
            }
            duration /= division.amount;
        }
    }
    return new Intl.RelativeTimeFormat('fr', {
        localeMatcher: 'best fit',
        numeric: 'always',
        style: 'long',
    }).format(deltaDays, 'days');
};

export const readMore = (text, length = 150, suffix = '...') => {
    return text.substring(0, length) + suffix;
};


