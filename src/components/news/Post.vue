<template>
    <div class="w-full rounded overflow-hidden shadow-md mt-6">
        <div v-if="post.header" class="h-400 overflow-hidden">
            <img class="w-full" :src="post.header" :alt="post.title">
        </div>
      <div class="px-6 py-4">
        <div class="font-bold text-xl mb-2">{{ post.title }}</div>
        <vue-markdown :source="toggled ? post.content : truncatedText" :class="'text-gray-900 text-base'"></vue-markdown>
        <p class="text-grey-900 text-base"><a href="javascript:void(0)" class="text-teal-600 hover:text-teal-900" @click="toggle">{{ toggled ? $t('message.showLess') : $t('message.showMore') }}</a></p>
      </div>
      <div class="px-6 py-4">
        <span v-for="tag in post.tags" :key="tag.id" class="inline-block bg-gray-400 rounded-full px-3 py-1 text-sm font-semibold text-gray-900 mr-2">#{{ tag.word }}</span>
      </div>
      <div class="px-6 py-4" v-if="user && user.is_staff">
          <router-link :to="{name: 'EditNews', params: {newsSlug: post.slug, newsId: post.id }}">
              Edit
          </router-link>
          <button @click="deleteNew(post.id)">
              Delete
          </button>
      </div>
    </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'
import { mapGetters, mapActions } from 'vuex';

export default {
    props: {
        post: Object
    },
    data () {
        return {
            limit: 25,
            toggled: false
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        truncatedText () {
            if (this.post.content.length < this.limit ) {
                return this.post.content;
            } else {
                for (let i = this.limit; i > 0; i--) {
                      return `${this.post.content.substring(0, i)}...`;
                }
            }
        }
    },
    methods: {
        ...mapActions('post',['deletePost']),
        deleteNew(id) {
            this.deletePost(id)
        },
        toggle () {
            this.toggled = !this.toggled
        }
    },
    components: {
     VueMarkdown,
   },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.h-400 {
    height: 400px;
}
</style>
