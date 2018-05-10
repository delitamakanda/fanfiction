<template>
    <div class="w-full max-w-xs">
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="title"
            :operation="operation"
            :valid="valid">
                <div class="mb-4">
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="email">
                        E-mail
                    </label>
                    <Input
                        id="email"
                        name="email"
                        type="email"
                        v-model="email"
                        placeholder="E-mail"
                        required />
                </div>
                <template slot="actions">
                    <div class="flex items-center justify-between">
                        <button
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!valid">
                            Renvoyer le mot de passe
                        </button>
                    </div>
                </template>
        </Form>
    </div>
</template>

<script>
export default {
    name: 'ForgotPassword',
    data(){
        return{
            email: '',
        }
    },
    computed: {
        title () {
            return 'Vous avez oublié votre mot de passe ?'
        },
        valid () {
            return !!this.email
        },
    },
    async created () {
    },
    methods: {
        async operation () {
            const result = await this.$fetch('forgot-password', {
                method: 'POST',
                body: JSON.stringify({
                    email: this.email
                }),
            })
            this.email = ''
        },
    },
}
</script>

<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
