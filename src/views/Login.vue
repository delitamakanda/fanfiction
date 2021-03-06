<template>
  <div class="w-full max-w-xs">
    <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        :title="title"
        :operation="operation"
        :valid="valid">
            <div class="mb-4">
                <label class="block text-grey-darker text-sm font-bold mb-2" for="username">
                    {{ $t('message.username') }}
                </label>
                <Input
                    :text="username"
                    name="username"
                    v-model="username"
                    placeholder="Pseudo"
                    v-validate="'required'" />
                    <span>{{ err.first('username') }}</span>
                </div>
            <div class="mb-6">
                <label class="block text-grey-darker text-sm font-bold mb-2" for="password">
                    {{ $t('message.passwordLabel') }}
                </label>
                <Input
                    name="password"
                    :type="passwordFieldType"
                    v-model="password"
                    placeholder="Mot de passe"
                    v-validate="'required'" />
                <button type="button" @click="switchVisibility">
                    <svgicon icon="view-show" v-if="!iconVisibility" width="22" height="18" color="#000"></svgicon>
                    <svgicon icon="view-hide" v-if="iconVisibility" width="22" height="18" color="#000"></svgicon>
                </button>
                <span>{{ err.first('password') }}</span>
            </div>
            <template v-if="mode === 'signup'">
                <div class="mb-6">
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="verify-password">
                        {{ $t('message.confirmPasswordLabel') }}
                    </label>
                    <Input
                        name="verify-password"
                        type="password"
                        v-model="password2"
                        :placeholder="$t('message.confirmPasswordLabel')"
                        :invalid="retypePasswordError"
                        v-validate="'required'" />
                    <span>{{ err.first('verify-password') }}</span>
                </div>
                <div class="mb-4">
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="email">
                        {{ $t('message.formContactEmailLabel') }}
                    </label>
                    <Input
                        name="email"
                        type="email"
                        v-model="email"
                        :placeholder="$t('message.formContactEmailLabel')"
                        v-validate="'required|email'" />
                    <span>{{ err.first('email') }}</span>
                </div>
            </template>
            <template slot="actions">
                <template v-if="mode === 'login'">
                    <a href="accounts/password_reset/" class="inline-block align-baseline font-bold text-sm text-blue hover:text-blue-darker">{{ $t('message.forgotPasswordLabel') }}?</a>
                    <div class="flex items-center justify-between">
                        <button
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-darker"
                        type="button"
                        @click="mode = 'signup'">
                            {{ $t('message.registerLabel')}}
                        </button>
                        <button
                        class="bg-blue-500 hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!valid">
                            {{ $t('message.connectionLabel')}}
                        </button>
                    </div>
                    {{ error }}
                </template>
                <template v-else-if="mode === 'signup'">
                    <div class="flex items-center justify-between">
                        <button
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-darker"
                        type="button"
                        @click="mode = 'login'">
                            {{ $t('message.connectionLabel')}}
                        </button>
                        <button
                        class="bg-blue-500 hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!valid">
                            {{ $t('message.registerLabel')}}
                        </button>
                    </div>
                    {{ error }}
                </template>
            </template>

    </Form>

  </div>
</template>

<script>
import '../compiled-icons/view-show'
import '../compiled-icons/view-hide'
import { mapActions, mapState } from 'vuex'

export default {
    data () {
        return {
            username: '',
            mode: 'login',
            password: '',
            password2: '',
            passwordFieldType: 'password',
            email: '',
            iconVisibility: false
        }
    },
    computed: {
        ...mapState('user', ['user', 'error']),
        title () {
            this.clearError()
            switch (this.mode) {
                case 'login': return this.$t('message.connectionLabel')
                case 'signup': return this.$t('message.createNewAccountLabel')
            }
        },
        retypePasswordError () {
            return !!this.password2 && this.password !== this.password2
        },

        signupValid () {
            return !!this.password2 && !!this.email && !this.retypePasswordError
        },
        valid () {
            return !!this.username && !!this.password && (this.mode !== 'signup' || this.signupValid)
        },
    },

    methods: {
        ...mapActions('user', ['connect', 'authenticate', 'register', 'clearError']),
        async operation () {
            await this[this.mode]()
        },
        async login () {
            let username = this.username
            let password = this.password

            this.authenticate({ username, password })
            // let user = await this.$fetch('login', {
            //     method: 'POST',
            //     body: JSON.stringify({
            //         username: this.username,
            //         password: this.password,
            //     }),
            // })
            // this.$router.replace(this.$route.params.wantedRoute || { name: 'Dashboard'})
        },
        async signup () {
            let username = this.username
            let password = this.password
            let email = this.email

            this.register({ username, password, email })
            // await this.$fetch('signup', {
            //     method: 'POST',
            //     body: JSON.stringify({
            //         username: this.username,
            //         password: this.password,
            //         email: this.email,
            //     }),
            // })
            this.mode = 'login'
        },
        switchVisibility () {
            this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
            this.iconVisibility = this.iconVisibility === false ? true : false;
        }

    },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.w-full {
    margin: 0 auto;
}
</style>
