<template>
<div v-html="page">
</div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import { fetchPage } from '../../api/infoApi';
import { withAsync } from '../../api/helpers/withAsync';

export default {
    setup() {
        const $route = useRoute();

        const page = ref<any>();

        const getPages = async () => {
           const { response, error } = await withAsync(fetchPage, $route.params.legal, {});
           page.value = response.data;
        }

        watch($route, (val, oldVal) => { 
            if ((val.params.legal && oldVal.params.legal) || (val.params.legal !== $route.params.legal)) {
                getPages();
            }
        });

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