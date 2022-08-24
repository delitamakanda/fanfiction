import FAQ from './FAQ.vue';
import Help from './Help.vue';


const miscRoutes = [
    {
        path: '/help',
        name: 'Help',
        component: Help,
        meta: {
            layout: 'standard',
        }
    },
    {
        path: '/faq',
        name: 'FAQ',
        component: FAQ,
        meta: {
            layout: 'standard'
        }
    },
];

export default miscRoutes;
