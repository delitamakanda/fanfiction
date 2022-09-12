import Announcement from './Announcement.vue';
import ViewAnnouncement from './viewAnnouncement/views/ViewAnnouncement.vue';
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
        path: '/announcement/view/:slug',
        name: 'ViewAnnouncement',
        component: ViewAnnouncement,
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
