<template>
<Breadcrumb />
<div v-html="page">
</div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import { fetchPage } from '../../../api/infoApi';
import { withAsync } from '../../../api/helpers/withAsync';
import Breadcrumb from '../../../components/base/Breadcrumb.vue';

export default {
    components: {
        Breadcrumb,
    },
    setup() {
        const $route = useRoute();

        const page = ref<any>();

        const getPages = async () => {
           const { response, error } = await withAsync(fetchPage, $route.params.legal, {});
           page.value = response.data;
        }

        onMounted(() => {
            getPages();
        });
        return {
            getPages,
            page,
            $route
        };
    },
}
</script>