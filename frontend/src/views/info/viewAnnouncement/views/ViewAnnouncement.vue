<template>
    <div v-if="post">
        <span class="bg-primary-100 text-primary-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded dark:bg-primary-200 dark:text-primary-800">
            <svg class="mr-1 w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clip-rule="evenodd"></path><path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V7z"></path></svg>
            {{post.category}}
        </span>
        <h3>{{ post.title }}</h3>
        <markdown :source="post.content" :html="true" :linkify="true"></markdown>
        <div>{{ formatDateTime(post.created) }}</div>
        <avatar ref="avatar" class="w-7 h-7 rounded-full" :email="post.email_author" />
        <span class="font-medium dark:text-white">
            {{ post.username_author }}
        </span>
    </div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { formatRelativeDate } from '../../../../helpers/utils';
import Avatar from '../../../../components/common/Avatar.vue';
import Markdown from 'vue3-markdown-it';
import { fetchPost } from '../../../../api/infoApi';
import { ref, onMounted } from 'vue';
import { withAsync } from '../../../../api/helpers/withAsync';

export default {
    components: {
        'avatar': Avatar,
        'markdown': Markdown,
    },
    setup() {
        const $route = useRoute();
        const post = ref<any>();

        const formatDateTime = (date: string) => {
            return formatRelativeDate(date);
        }
        
        const getPost = async () => {
            const { response, error } = await withAsync(fetchPost, $route.params.slug, {});

            post.value = response.data;
        }

        onMounted(() => {
            getPost();
        });

        return {
            $route,
            formatDateTime,
            getPost,
            post,
        };
    },
}
</script>