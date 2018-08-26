<template>
    <div>
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="title"
            :operation="operation"
            :valid="valid">
                <div class="mb-4">
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="old_password">
                        Ancien mot de passe
                    </label>
                    <Input
                        name="old_password"
                        type="password"
                        v-model="old_password"
                        placeholder="Ancien mot de passe"
                        required />
                    </div>
                <div class="mb-6">
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="new_password">
                        Mot de passe
                    </label>
                    <Input
                        name="new_password"
                        type="password"
                        v-model="new_password"
                        placeholder="Nouveau mot de passe" />
                </div>
                <template slot="actions">
                    <div class="flex items-center justify-between">
                        <button
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!valid">
                            Changer le mot de passe
                        </button>
                    </div>
                </template>

        </Form>
    </div>
</template>

<script>
export default {
    name: 'ChangePassword',
    data(){
        return{
            old_password: '',
            new_password: ''
        }
    },
    computed: {
      title () {
        return "Changer le mot de passe"
      },
      valid () {
        return !!this.old_password && !!this.new_password
      },
    },
    methods: {
      async operation () {
        const result = await this.$fetch('change-password', {
                method: 'PUT',
                body: JSON.stringify({
                    old_password: this.old_password,
                    new_password: this.new_password
                }),
            })
            this.old_password = this.new_password = ''
      }
    }
}
</script>

<style scoped>
</style>
