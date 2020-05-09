<template>
<div class="container mx-auto px-4">
    <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        :title="$t('message.newsPage.title')"
        :operation="operation"
        :valid="valid">
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.newsPage.titleLabel') }}
                </label>
                <Input
                    type="text"
                    name="title"
                    v-model="title"
                    :placeholder="$t('message.newsPage.titleLabel')"/>
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.newsPage.headerLabel') }}
                </label>
                <Input
                    type="text"
                    name="header"
                    v-model="header"
                    :placeholder="$t('message.newsPage.headerLabel')"/>
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                    {{ $t('message.newsPage.contentLabel') }}
                </label>
                <Input
                type="textarea"
                name="content"
                v-model="content"
                :placeholder="$t('message.newsPage.contentLabel')"
                rows="6"
                required />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.newsPage.tagsLabel') }}
                </label>
                <input-tag
                    v-model="tags"
                    :placeholder="$t('message.newsPage.tagsLabel')">
                </input-tag>
            </div>
            <template slot="actions">
                <div class="flex items-center justify-between">
                    <button
                    class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                    type="submit"
                    :disabled="!valid">
                        Submit
                    </button>
                </div>
            </template>
    </Form>
</div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import confirm from "@/mixins/confirm";
import InputTag from 'vue-input-tag'

export default {
    created() {
        this.getNews({ slug: this.newsSlug})
    },
    destroyed() {
        this.clearNews()
    },
    components: {
        'input-tag': InputTag
    },
    props: {
        newsSlug: {
            type: String,
            required: true
        },
        newsId: {
            type: Number,
            required: true
        },
    },
    data () {
        return {
            newHeader: '',
            newTitle: '',
            newContent: '',
            newTags: []
        };
    },
    mixins: [ confirm ],
    computed: {
        ...mapGetters('user', ['user']),
        ...mapState('post', ['news']),
        valid() {
            return !!this.newsSlug
        },
        header: {
            get() {
                return this.news.header
            },
            set(val) {
                this.newHeader = val
            }
        },
        title: {
            get() {
                return this.news.title
            },
            set(val) {
                this.newTitle = val
            }
        },
        content: {
            get() {
                return this.news.content
            },
            set(val) {
                this.newContent = val
            }
        },
        tags: {
            get() {
                return this.news.tags
            },
            set(val) {
                this.newTags.push(val)
            }
        }
    },
    methods: {
        ...mapActions('post', ['updatePost', 'getNews', 'clearNews']),
        operation () {
            const message = this.$t('message.infosUpdated');
            
            const data = {
                user: this.user.id,
                header: this.newHeader ? this.newHeader : this.header,
                title: this.newTitle ? this.newTitle : this.title,
                content: this.newContent ? this.newContent : this.content,
                tags: this.newTags ? this.newTags : this.tags,
                id: this.news.id
            }

            this.confirm(message, () => {
                this.updatePost(data)
            });
        }
    }
}
</script>

<style scoped>

</style>