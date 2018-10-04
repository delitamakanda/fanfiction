<template>
    <div class="w-full max-w-md">
        <template v-if="id && !chapter_id">
            <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            title="Nouveau chapitre"
            :operation="add"
            :valid="valid">
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="title">
                      Titre du chapitre
                    </label>
                    <Input
                        name="title"
                        v-model="title"
                        placeholder="Titre du chapitre"
                        maxlength="255"
                        required />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="description">
                      Description du chapitre
                    </label>
                    <Input
                        type="textarea"
                        name="description"
                        v-model="description"
                        placeholder="Description du chapitre"
                        maxlength="1000"
                        rows="4" />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="text">
                      Chapitre
                    </label>
                    <trumbowyg v-model="text"></trumbowyg>
                </div>
                <template slot="actions">
                    <router-link
                        tag="button"
                        :to="{name: 'Fanfic', params: { id: this.$route.params.id }}"
                        class="secondary inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">
                        Retour à l'histoire
                    </router-link>
                    <button
                        type="submit"
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        :disabled="!valid">
                        Ajouter un chapitre
                    </button>
                </template>
            </Form>
        </template>
        <template v-else-if="chapter_id">
            <Loading v-if="remoteDataBusy" />
            <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
                {{ errorFetch }}
            </div>
            <form
            @submit.prevent="edit"
            enctype="multipart/form-data"
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <h2>Editer le chapitre</h2>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="title">
                      Titre du chapitre
                    </label>
                    <Input
                        name="title"
                        v-model="chapter.title"
                        placeholder="Titre du chapitre"
                        maxlength="255"
                        required />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="description">
                      Description du chapitre
                    </label>
                    <Input
                        type="textarea"
                        name="description"
                        v-model="chapter.description"
                        placeholder="Description du chapitre"
                        maxlength="1000"
                        rows="4" />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="text">
                      Chapitre
                    </label>
                    <trumbowyg v-model="chapter.text"></trumbowyg>
                </div>
                <Input
                    type="hidden"
                    name="fanfic"
                    v-model="chapter.fanfic" />
                <router-link
                    tag="button"
                    :to="{name: 'Fanfic', params: { id: this.$route.params.id }}"
                    class="secondary inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">
                    Retour à la l'histoire
                </router-link>
                <button
                    type="submit"
                    class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded">
                    Editer le chapitre
                </button>
            </form>
        </template>
    </div>
</template>

<script>
import PersistantData from '../mixins/PersistantData'
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'NewChapter',
    mixins: [
        PersistantData('NewChapter', [
            'title',
            'description',
            'text',
        ]),
        RemoteData({
            fanfic () {
                return `fanfics/${this.$route.params.id}`
            },
            chapter () {
                return this.chapter_id ? `chapters/${this.$route.params.chapter_id}` : ``
            },
        }),
    ],
    data(){
        return{
            error: null,
            title: '',
            description: '',
            text: '',
            errorFetch: 'Il y a un problème avec la requète.',
            chapter: []
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
        chapter_id: {
            type: Number,
            required: false,
        },
    },
    computed: {
        valid () {
            return !!this.title && !!this.text
        }
    },
    methods: {
        async add () {
            const result = await this.$fetch('chapters/create', {
                method: 'POST',
                body: JSON.stringify({
                    title: this.title,
                    description: this.description,
                    text: this.text,
                    fanfic: this.$route.params.id,
                    author: this.$state.user.id
                }),
            })
            this.title = this.description = this.text = ''
        },
        async edit () {
            const result = await this.$fetch(`chapters/${this.$route.params.chapter_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    title: this.chapter.title,
                    description: this.chapter.description,
                    text: this.chapter.text,
                    fanfic: this.chapter.fanfic,
                    author: this.$state.user.id
                }),
            })
            this.$router.push({name: 'Fanfic', params: { id: this.chapter.fanfic }})
        }
    },
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
