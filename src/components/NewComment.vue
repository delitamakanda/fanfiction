<template>
    <div class="w-full max-w-md">

        <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        title="Nouveau commentaire"
        :operation="operation"
        :valid="valid">
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="name">
                  Nom ou Pseudo
                </label>
                <Input
                    name="name"
                    v-model="name"
                    placeholder=""
                    maxlength="255"
                    required />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="email">
                  E-mail
                </label>
                <Input
                    name="email"
                    v-model="email"
                    placeholder="Votre e-mail (seul l'auteur le verra)"
                    maxlength="255" />
            </div>
            <div class="mb-4">
                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="body">
                  Commentaire
                </label>
                <Input
                    type="textarea"
                    name="body"
                    v-model="body"
                    placeholder=""
                    rows="6"
                    required />
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
                    Ajouter un commentaire
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
            'name',
            'email',
            'body',
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
            name: '',
            email: '',
            body: '',
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
            return !!this.name && !!this.body
        }
    },
    methods: {
        async operation () {
            const result = await this.$fetch('comments', {
                method: 'POST',
                body: JSON.stringify({
                    name: this.name,
                    email: this.email,
                    body: this.body,
                    fanfic: this.$route.params.id,
                }),
            })
            this.name = this.email = this.body = ''
        }
    },
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
