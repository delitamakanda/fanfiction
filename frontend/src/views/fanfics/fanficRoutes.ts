import AddFanfic from './AddFanfic.vue';
import EditFanfic from './EditFanfic.vue';
import DeleteFanfic from './DeleteFanfic.vue';
import AdvancedFanficDetails from './viewFanfic/views/AdvancedFanficDetails.vue';
import BasicFanficDetails from './viewFanfic/views/BasicFanficDetails.vue';
import ListFanfic from './ListFanfic.vue';
import BrowseFanfic from './BrowseFanfic.vue';


const fanficRoutes = [
    {
        path: '/add-fanfic',
        name: 'AddFanfic',
        component: AddFanfic,
        meta: {
            layout: 'standard'
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
        path: '/edit-fanfic',
        name: 'EditFanfic',
        component: EditFanfic,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/delete-fanfic',
        name: 'DeleteFanfic',
        component: DeleteFanfic,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/advanced-fanfic-details',
        name: 'AdvancedFanficDetails',
        component: AdvancedFanficDetails,
        meta: {
            layout: 'standard'
        }
    },
    {
        path: '/basic-fanfic-details',
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
