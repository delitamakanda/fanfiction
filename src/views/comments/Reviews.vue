<template>
    <div>
        <div v-if="!isPrivate">
            <comment :comments="comments" :isPrivate="false"></comment>
        </div>
        <div v-else>
            <comment :comments="filteredComment" :isPrivate="true"></comment>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import Comment from '@/components/comment/Comment';

export default {
    name: 'Reviews',
    props: {
        fanficId: {
            type: Number,
            required: false
        },
        isPrivate: {
            type: Boolean,
            required: false,
            default: true
        }
    },
    data() {
        return {
            filteredComment: []
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        ...mapGetters('comment', ['commentsByAuthor']),
        ...mapState('comment', ['comments', 'allcomments'])
    },
    created () {
        if (this.isPrivate) {
            this.fetchComments()
            this.filteredComment = this.commentsByAuthor(this.user);
        } else {
            console.log(this.isPrivate)
            this.fetchAllComments({ id: this.fanficId, isActive: true})
        }
    },
    methods: {
        ...mapActions('comment', ['fetchAllComments', 'fetchComments', 'clearComments'])
    },
    watch: {
        comments(val, oldVal) {
        }
    },
    components: { Comment }
}
</script>

<style scoped>
</style>
