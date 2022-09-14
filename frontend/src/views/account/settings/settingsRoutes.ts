import StaticPage from './StaticPage.vue';
import sns from './sns.vue';
import EmailChange from './EmailChange.vue';
import PasswordChange from './PasswordChange.vue';
import ProfileChange from './ProfileChange.vue';


const settingsRoutes = [
    {
        path: '/settings/email-change',
        name: 'EmailChange',
        component: EmailChange,
        meta: {
            layout: 'standard',
            requireAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' },
                { name: 'Changement email', link: '/settings/email-change' }
            ]
        }
    },
    {
        path: '/settings/password-change',
        name: 'PasswordChange',
        component: PasswordChange,
        meta: {
            layout: 'standard',
            requireAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' },
                { name: 'Changement password', link: '/settings/password-change' }
            ]
        }
    },
    {
        path: '/settings/profile-change',
        name: 'ProfileChange',
        component: ProfileChange,
        meta: {
            layout: 'standard',
            requireAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' },
                { name: 'Modification du profil', link: '/settings/profile-change' }
            ]
        }
    },
    {
        path: '/settings/sns-change',
        name: 'Sns',
        component: sns,
        meta: {
            layout: 'standard',
            requireAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' },
                { name: 'Social network', link: '/settings/sns-change' }
            ]
        }
    },
    {
        path: '/settings/static-page/:legal',
        name: 'StaticPage',
        component: StaticPage,
        meta: {
            layout: 'standard',
            requireAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' },
                { name: 'Informations légales', link: '/settings/static-page/:legal' }
            ]
        }
    },
];

export default settingsRoutes;
