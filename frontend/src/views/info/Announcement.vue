<template>
<section class="bg-white dark:bg-gray-900">
  <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
      <div class="mx-auto max-w-screen-sm text-center lg:mb-16 mb-8">
          <h2 class="mb-4 text-3xl lg:text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white">{{ $t('message.blog.title') }}</h2>
          <p class="font-light text-gray-500 sm:text-xl dark:text-gray-400">{{ $t('message.blog.baseLine')}}.</p>
      </div> 
      <div class="grid gap-8 lg:grid-cols-2">
          <post-card v-for="post of posts" :post="post" :key="post.id" />
      </div>  
  </div>
</section>
</template>

<script lang="ts">
import { withAsync } from '../../api/helpers/withAsync';
import { fetchPosts } from '../../api/infoApi';
import { ref, onMounted } from 'vue';
import PostCard from './components/PostCard.vue';


export default {
    components: {
        'post-card': PostCard
    },
    setup() {
        const posts = ref<any>();
        
        const getPosts = async () => {
            const { response, error } = await withAsync(fetchPosts);
            if (error) {
                return;
            }
            posts.value = response.data.results;
        }

        onMounted(() => {
            getPosts();
        });

        return {
            posts,
            getPosts,
        }
    }
}
</script>