<template>
<div class="container mx-auto px-4">
    <h2>{{ $tc('message.newsLabel', this.totalNews, { n: this.totalNews }) }}</h2>
    <Loading v-if="remoteDataBusy" />
    <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
        {{ $t('message.errorFetch') }}
    </div>
    <Post v-for="(post, i) in posts" track-by="post.slug" :key="i" :post="post"></Post>
</div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'
import Post from '@/components/Post'

export default {
    created() {},
    data () {
        return {
            errorFetch: this.$t('message.errorFetch'),
            maxCharacters: 15,
            posts: []
        };
    },
    computed: {
        totalNews () {
            return this.posts.length;
        }
    },
    methods: {

    },
    mixins: [
        RemoteData({
            posts: 'posts',
        }),
    ],
    components: {Post}
}
</script>

<style scoped>

</scoped>
