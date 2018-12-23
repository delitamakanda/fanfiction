<template>
    <div class="w-full max-w-md">
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
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="status">
                  Status
                </label>
                <div class="relative">
                  <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="status" v-model="status">
                      <option value="">Sélectionner</option>
                      <option v-for="(status, i) in statusOptions" :key="i" :value="status.key">{{ status.value }}</option>
                  </select>
                  <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                  </div>
                </div>
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
    </div>
</template>

<script>
import PersistantData from '../mixins/PersistantData'
import RemoteData from '../mixins/RemoteData'
import { mapGetters } from 'vuex'

export default {
    mixins: [
        PersistantData('DraftChapter', [
            'title',
            'description',
            'text',
        ]),
        RemoteData({
            fanfic () {
                return `fanfics/${this.$route.params.id}`
            }
        }),
    ],
    data(){
        return{
            error: null,
            title: '',
            description: '',
            text: '',
            status: '',
            errorFetch: this.$t('message.errorFetch'),
            statusOptions: [{key: 'brouillon', value: 'Brouillon'}, {key: 'publié', value: 'Publié'}]
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        }
    },
    computed: {
        ...mapGetters('user', ['user']),
        valid () {
            return !!this.title && !!this.text && !!this.status
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
                    author: this.user.id,
                    status: this.status
                }),
            })
            this.title = this.description = this.text = this.status = ''
            this.$router.replace(this.$route.params.wantedRoute || { name: 'Fanfic', params: { id: this.$route.params.id }})
        }
    }
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
