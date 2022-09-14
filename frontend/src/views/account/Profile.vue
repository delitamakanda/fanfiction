<template>
<div>
    {{ route.params.username}}
    {{ route.params.email}}
    {{ profile }}
    {{ currentUser }}
</div>
</template>

<script lang="ts">
import Breadcrumb from '../../components/base/Breadcrumb.vue';
import { useRoute } from 'vue-router';
import { getCurrentProfile } from '../../api/accountApi';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { withAsync } from '../../api/helpers/withAsync';

export default {
    components: {
        Breadcrumb,
    },

    setup() {
        const route = useRoute();
        const store = useStore();
        const profile = ref<any>();

        onMounted( async() => {
            const { response, error } = await withAsync(getCurrentProfile, route.params.username);
            if (response) {
                profile.value = response.data;
            }
        });

        return {
            route,
            store,
            profile,
        };
    }
}
</script>