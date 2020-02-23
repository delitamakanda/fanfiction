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
        if (this.newsSlug && this.newsSlug.length) {
            this.getNews({ slug: this.newsSlug})
        }
    },
    components: {
        'input-tag': InputTag
    },
    props: {
        newsSlug: {
            type: String,
            required: false
        }
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
            return true
        },
        header: {
            get() {
                return this.news.header ? this.news.header : this.newHeader
            },
            set(val) {
                this.newHeader = val
            }
        },
        title: {
            get() {
                return this.news.title ? this.news.title : this.newTitle
            },
            set(val) {
                this.newTitle = val
            }
        },
        content: {
            get() {
                return this.news.content ? this.news.content : this.newContent
            },
            set(val) {
                this.newContent = val
            }
        },
        tags: {
            get() {
                return this.news.tags ? this.news.tags : this.newTags
            },
            set(val) {
                this.newTags = val
            }
        }
    },
    methods: {
        ...mapActions('post', ['addNews', 'updateNews', 'getNews']),
        operation () {
            const message = this.$t('message.infosUpdated');
            
            const data = {
                user: this.user.id,
                header: this.header ? this.header : this.newHeader,
                title: this.title ? this.title : this.newTitle,
                content: this.content ? this.content : this.newContent,
                tags: this.tags ? this.tags : this.newTags,
                id: this.news.id ? this.news.id : null
            }

            if (this.newsSlug && this.newsSlug.length) {
                data.tags = this.newTags
                this.confirm(message, () => {
                    this.updateNews(data)
                });
            } else {
                this.confirm(message, () => {
                    this.addNews(data)
                });
            }

            this.header = this.title = this.content = ''
        }
    }
}
</script>

<style scoped>

</style>