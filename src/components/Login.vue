<template>
  <div>
    <Form
        :title="title"
        :operation="operation"
        :valid="valid">
        <Input
            name="username"
            v-model="username"
            placeholder="Pseudo" />
        <Input
            name="password1"
            type="password"
            v-model="password1"
            placeholder="Mot de passe" />
        <template v-if="mode === 'signup'">
            <Input
                name="verify-password"
                type="password"
                v-model="password2"
                placeholder="Confirmer le mot de passe"
                :invalid="retypePasswordError" />
            <Input
                name="email"
                type="email"
                v-model="email"
                placeholder="E-mail" />
        </template>
        <template slot="actions">
            <template v-if="mode === 'login'">
                <button
                type="button"
                @click="mode = 'signup'">
                    S'enregister
                </button>
                <button
                type="button"
                :disabled="!valid">
                    Se connecter
                </button>
            </template>
            <template v-else-if="mode === 'signup'">
                <button
                type="button"
                @click="mode = 'login'">
                    Se connecter
                </button>
                <button
                type="button"
                :disabled="!valid">
                    S'enregister
                </button>
            </template>
        </template>
    </Form>

  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      mode: 'login',
      password1: '',
      password2: '',
      email: '',
    }
},
computed: {
    title () {
        switch (this.model) {
            case 'login': return 'Se connecter'
            case 'signup': return 'Création d\'un nouveau compte'
        }
    },
},
retypePasswordError() {
    return this.password2 && this.password1 !== this.password2
},
signupValid () {
    return this.password2 && this.email && !this.retypePasswordError
},
valid () {
    return this.username && this.password1 && (this.mode !== 'signup' || this.signupValid)
},
methods: {
    async operation () {
        await this[this.model]()
    },
    async login () {
        //
    },
    async signup () {
        //
    },

},

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
