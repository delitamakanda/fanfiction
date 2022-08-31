<template>
<div v-html="page">
</div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import { fetchPage } from '../../api/infoApi';

export default {
    setup() {
        const $route = useRoute();

        const page = ref<any>();

        const getPages = () => {
           fetchPage($route.params.legal)
            .then(response => {
                page.value = response.data;
            }, error => {
                console.log(error);
            });
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