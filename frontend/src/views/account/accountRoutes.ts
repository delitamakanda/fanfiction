import Dashboard from './Dashboard.vue';
import Profile from './Profile.vue';


const accountRoutes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: {
            layout: 'standard'
        }
    }
];

export default accountRoutes;
