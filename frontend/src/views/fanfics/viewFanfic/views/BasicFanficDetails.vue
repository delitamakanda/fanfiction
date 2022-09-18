<template>
<div v-if="fanfic">
    basic detail fanfic {{route.params.slug}}
    {{ fanfic.title }}

    {{ fanfic }}
</div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { fetchFanficDetail } from '../../../../api/fanficApi';
import { withAsync } from '../../../../api/helpers/withAsync';
import { formatDate, options_FR } from '../../../../helpers/utils';
import Avatar from '../../../../components/common/Avatar.vue';
import { ref, onMounted } from 'vue';

export default {
    components: {
        Avatar,
    },
    setup() {
        const route = useRoute();
        const fanfic = ref<any>(null);
        
        const format = (date: string) => {
            return formatDate(date, options_FR);
        };

        onMounted(async () => {
            const { response, error } = await withAsync(fetchFanficDetail, route.params.slug);
            if (error) {
                return;
            }
            fanfic.value = response.data;
        });

        return {
            route,
            format,
            fanfic,
        }
    }
}
</script>