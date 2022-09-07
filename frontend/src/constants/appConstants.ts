export const APP_NAME = 'Fanfiction';
export const APP_BASE_URL = 'https://fanfiction-fr.herokuapp.com/';
export const APP_VERSION = 2;

export const menuDashboard = [
    {
        name: 'Add',
        title: 'create',
        icon: 'add',
        route: '/add-fanfic',
        navigation: true,
    }, {
        name: 'List',
        title: 'list',
        icon: 'collection',
        route: '/your-fanfic',
        navigation: true,
    },{
        name: 'Profile',
        title: 'profile',
        icon: 'user-circle',
        route: '/profile',
        navigation: true,
    },{
        name: 'Settings',
        title: 'settings',
        icon: 'cog',
        route: '/settings',
        navigation: true,
    }, {
        name: 'Inbox',
        title: 'inbox',
        icon: 'inbox',
        route: '/inbox',
        navigation: true,
    }, {
        name: 'Logout',
        title: 'logout',
        icon: 'logout',
        route: 'disconnect',
        navigation: false,
    }
];

export const footerPages = [{
    type: 'legal',
    title: 'legalLabel',
}, {
    type: 'rgpd',
    title: 'rgpdLabel',
},{
    type: 'licensing',
    title: 'licensingLabel',
}];

export const menuAsideConnected = [
    {
        name: 'Dashboard',
        icon: 'dashboard',
        title: 'dashboardLabel',
        route: '/dashboard',
        navigation: true,
        isLoggedIn: true,
    }
];

export const menuAsideNotConnected = [
    {
        name: 'Signin',
        icon: 'login',
        title: 'signinLabel',
        route: '/signin',
        navigation: true,
        isLoggedIn: false,
    },
    {
        name: 'Signup',
        icon: 'register',
        title: 'signupLabel',
        route: '/signup',
        navigation: true,
        isLoggedIn: false,
    },
];
export const menuAside = [
    {
        name: 'Fanfics',
        icon: 'fanfics',
        title: 'fanficsLabel',
        route: '/fanfics',
        navigation: true,
        isLoggedIn: null,
    },
    {
        name: 'FAQ',
        icon: 'faq',
        title: 'documentationLabel',
        route: '/faq',
        navigation: true,
        isLoggedIn: null,
    },
    {
        name: 'Forum',
        icon: 'forum',
        title: 'forumLabel',
        route: 'https://forum-fanfiction-fr.azurewebsites.net',
        navigation: false,
        isLoggedIn: null,
    },
    {
        name: 'Help',
        icon: 'help',
        title: 'helpLabel',
        route: '/help',
        navigation: true,
        isLoggedIn: null,
    },
];