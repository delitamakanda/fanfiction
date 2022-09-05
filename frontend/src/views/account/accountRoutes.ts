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
            requiresAuth: true
        }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: {
            layout: 'standard',
            requiresAuth: true
        }
    },
    {
        path: '/inbox',
        name: 'Inbox',
        component: Inbox,
        meta: {
            layout: 'standard',
            requiresAuth: true
        }
    },
    {
        path: '/settings',
        name: 'Settings',
        component: Settings,
        meta: {
            layout: 'standard',
            requiresAuth: true
        }
    }
];

export default accountRoutes;
