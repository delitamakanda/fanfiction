<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>

        <Loading v-if="remoteDataBusy" />

        <div>
            <h3>{{ chapter.title }}</h3>

            <div v-if="chapter.description !== ''" class="bg-blue-lightest border-t border-b border-blue text-blue-dark px-4 py-3" v-html="chapter.description" role="alert">{{ chapter.description }}</div>

            <div v-html="chapter.text"></div>

        </div>
    </div>
</template>

<script>
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'Chapter',
    props: {
        id: {
            type: Number,
            required: true
        },
        slug: {
            type: String,
            required: true
        }
    },
    mixins: [
        RemoteData({
            chapter () {
                return `chapters/${this.$route.params.id}`
            },
        }),
    ],
    data () {
        return {
            errorFetch: 'Il y a un problème avec la requète.',
            chapter: []
        };
    }
}
</script>

<style scoped>
</style>
