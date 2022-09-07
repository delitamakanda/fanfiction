import Dashboard from './Dashboard.vue';
import Profile from './Profile.vue';
import Inbox from './Inbox.vue';
import Settings from './Settings.vue';


const accountRoutes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard'}
            ]
        }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Profile', link: '/profile' }
            ]
        }
    },
    {
        path: '/inbox',
        name: 'Inbox',
        component: Inbox,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Inbox', link: '/inbox' }
            ]
        }
    },
    {
        path: '/settings',
        name: 'Settings',
        component: Settings,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' }
            ]
        }
    }
];

export default accountRoutes;
