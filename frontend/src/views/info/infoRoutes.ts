import Announcement from './Announcement.vue';
import StaticPage from './StaticPage.vue';
import Contact from './Contact.vue';


const infoRoutes = [
    {
        path: '/announcement',
        name: 'Announcement',
        component: Announcement,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/static-page/:legal',
        name: 'StaticPage',
        component: StaticPage,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/contact',
        name: 'Contact',
        component: Contact,
        meta: {
            layout: 'standard'
        }
    }
];

export default infoRoutes;
