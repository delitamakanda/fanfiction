<template>
<div>
    {{ route.params.username}}
    {{ route.params.email}}
</div>
</template>

<script lang="ts">
import Breadcrumb from '../../components/base/Breadcrumb.vue';
import { useRoute } from 'vue-router';

export default {
    components: {
        Breadcrumb,
    },

    setup() {
        const route = useRoute();

        return {
            route,
        };
    }
}
</script>