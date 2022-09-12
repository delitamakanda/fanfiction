import StaticPage from './StaticPage.vue';


const settingsRoutes = [
    {
        path: '/settings/static-page/:legal',
        name: 'StaticPage',
        component: StaticPage,
        meta: {
            layout: 'standard',
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Settings', link: '/settings' },
                { name: 'Informations', link: '/settings/static-page/:legal' }
            ]
        }
    },
];

export default settingsRoutes;
