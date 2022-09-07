import AddFanfic from './AddFanfic.vue';
import EditFanfic from './EditFanfic.vue';
import DeleteFanfic from './DeleteFanfic.vue';
import AdvancedFanficDetails from './viewFanfic/views/AdvancedFanficDetails.vue';
import BasicFanficDetails from './viewFanfic/views/BasicFanficDetails.vue';
import ListFanfic from './ListFanfic.vue';
import BrowseFanfic from './BrowseFanfic.vue';
import YourFanfic from './YourFanfic.vue';


const fanficRoutes = [
    {
        path: '/add-fanfic',
        name: 'AddFanfic',
        component: AddFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true
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
            requiresAuth: true
        }
    },
    {
        path: '/edit-fanfic/:slug',
        name: 'EditFanfic',
        component: EditFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true
        }
    },
    {
        path: '/delete-fanfic/:id',
        name: 'DeleteFanfic',
        component: DeleteFanfic,
        meta: {
            layout: 'standard',
            requiresAuth: true
        }
    },
    {
        path: '/advanced-fanfic-details/:slug',
        name: 'AdvancedFanficDetails',
        component: AdvancedFanficDetails,
        meta: {
            layout: 'standard',
            requiresAuth: true
        }
    },
    {
        path: '/basic-fanfic-details/:slug',
        name: 'BasicFanficDetails',
        component: BasicFanficDetails,
        meta: {
            layout: 'standard'
        }
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
