<template>
    <div class="w-full max-w-md">

        <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        title="Nouveau commentaire"
        :operation="operation"
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
                <Input
                    type="textarea"
                    name="text"
                    v-model="text"
                    placeholder="Ecrire le chapitre"
                    rows="20" />
            </div>
            <template slot="actions">
                <router-link
                    tag="button"
                    :to="{name: 'fanfic', params: { id: fanfic.id }}"
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
export default {
    name: 'NewComment',
    mixins: [
        PersistantData('NewComment', [
            'title',
            'description',
            'text',
        ]),
        RemoteData({
            fanfic () {
                return `fanfics/${this.$route.params.id}`
            },
        }),
    ],
    data(){
        return{
            error: null,
            title: '',
            description: '',
            text: '',
        }
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    computed: {
        valid () {
            return !!this.title && !!this.description && !!this.text
        }
    },
    methods: {
        async operation () {
            const result = await this.$fetch('comments', {
                method: 'POST',
                body: JSON.stringify({
                    title: this.title,
                    description: this.description,
                    text: this.text,
                    fanfic: this.$route.params.id,
                }),
            })
            this.title = this.description = this.text = ''
        }
    },
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
