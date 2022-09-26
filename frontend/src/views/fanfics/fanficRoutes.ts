import AddFanfic from './AddFanfic.vue';
import EditFanfic from './EditFanfic.vue';
import DeleteFanfic from './DeleteFanfic.vue';
import AdvancedFanficDetails from './viewFanfic/views/AdvancedFanficDetails.vue';
import BasicFanficDetails from './viewFanfic/views/BasicFanficDetails.vue';
import ListFanfic from './ListFanfic.vue';
import BrowseFanfic from './BrowseFanfic.vue';
import YourFanfic from './YourFanfic.vue';
import EditChapter from './EditChapter.vue';
import BrowseChapter from './viewChapter/views/BrowseChapter.vue';


const fanficRoutes = [
    {
        path: '/add-fanfic',
        name: 'AddFanfic',
        component: AddFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Créer une fanfiction', link: '/add-fanfic' },
            ]
        }
    },
    {
        path: '/fanfics',
        name: 'ListFanfic',
        component: ListFanfic,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/your-fanfic',
        name: 'YourFanfic',
        component: YourFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Vos fanfictions', link: '/your-fanfic' },
            ]
        }
    },
    {
        path: '/edit-fanfic/:slug',
        name: 'EditFanfic',
        component: EditFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Vos fanfictions', link: '/your-fanfic' },
                { name: 'Modification d\'une fanfiction', link: '/your-edit-fanfic/:slug' },
            ]
        }
    },
    {
        path: '/delete-fanfic/:id',
        name: 'DeleteFanfic',
        component: DeleteFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true,
            breadcrumb: [
                { name: 'Dashboard', link: '/dashboard' },
                { name: 'Vos fanfictions', link: '/your-fanfic' },
                { name: 'Suppression d\'une fanfiction', link: '/delete-fanfic/:id' },
            ]
        }
    },
    {
        path: '/advanced-fanfic-details/:slug',
        name: 'AdvancedFanficDetails',
        component: AdvancedFanficDetails,
        meta: {
            layout: 'standard',
            breadcrumb: [
                { name: 'ListFanfic', link: '/fanfics' },
                { name: 'AdvancedFanficDetails', link: '/advanced-fanfic-details/:slug' },
            ]
        }
    },
    {
        path: '/basic-fanfic-details/:slug',
        name: 'BasicFanficDetails',
        component: BasicFanficDetails,
        meta: {
            layout: 'standard',
            breadcrumb: [
                { name: 'ListFanfic', link: '/fanfics' },
                { name: 'BasicFanficDetails', link: '/basic-fanfic-details/:slug' },
            ]
        },
        children: [
            { 
                path: '/fanfic/:fanficId/chapter/:chapterId', 
                name: 'BrowseChapter', 
                component: BrowseChapter
            },
            { 
                path: 'edit-chapter/:id',
                name: 'EditChapter',
                component: EditChapter
            },
        ]
    },
    {
        path: '/',
        name: 'BrowseFanfic',
        component: BrowseFanfic,
        meta: {
            layout: 'standard'
        }
    }
];

export default fanficRoutes;
