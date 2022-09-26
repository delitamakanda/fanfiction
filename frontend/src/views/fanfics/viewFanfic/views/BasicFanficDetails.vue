<template>
<div v-if="fanfic">
    {{ fanfic.title }}

    {{ fanfic }}
    <router-view></router-view>
    <ul v-for="(chapter, idx) in chapters" :key="idx">
        <li>
            <router-link :to="`/fanfic/${fanfic.id}/chapter/${chapter.id}`">
                {{ chapter.title }}
            </router-link>
        </li>
    </ul>
</div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { fetchFanficDetail, fetchChaptersList } from '../../../../api/fanficApi';
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
        const chapters = ref<any>(null);
        
        const format = (date: string) => {
            return formatDate(date, options_FR);
        };

        const getFanficDetail = async () => {
            // fetch fanfic details
            const { response, error } = await withAsync(fetchFanficDetail, route.params.slug);
            if (error) {
                return;
            }
            fanfic.value = response.data;
            if (response) {
                // fetch chapters list
                getChaptersListByFanfic();
            }
        }

        const getChaptersListByFanfic = async () => {
            const { response, error } = await withAsync(fetchChaptersList, fanfic.value.id);
            if (error) {
                return;
            }
            chapters.value = response.data.results;
        }

        onMounted(() => {
            getFanficDetail();
        });

        return {
            route,
            format,
            fanfic,
            chapters,
        }
    }
}
</script>