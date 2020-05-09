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
                    v-model="newTitle"
                    :placeholder="$t('message.newsPage.titleLabel')"/>
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.newsPage.headerLabel') }}
                </label>
                <Input
                    type="text"
                    name="header"
                    v-model="newHeader"
                    :placeholder="$t('message.newsPage.headerLabel')"/>
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                    {{ $t('message.newsPage.contentLabel') }}
                </label>
                <Input
                type="textarea"
                name="content"
                v-model="newContent"
                :placeholder="$t('message.newsPage.contentLabel')"
                rows="6"
                required />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.newsPage.tagsLabel') }}
                </label>
                <input-tag
                    v-model="newTags"
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
import { mapGetters, mapActions } from 'vuex';
import confirm from "@/mixins/confirm";
import InputTag from 'vue-input-tag'

export default {
    components: {
        'input-tag': InputTag
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
        valid() {
            return !!this.newTitle && !!this.newContent
        }
    },
    methods: {
        ...mapActions('post', ['addNews']),
        operation () {
            const message = this.$t('message.infosUpdated');
            
            const data = {
                user: this.user.id,
                header: this.newHeader,
                title: this.newTitle,
                content: this.newContent,
                tags: this.newTags
            }

            this.confirm(message, () => {
                this.addNews(data)
            });
        }
    }
}
</script>

<style scoped>

</style>