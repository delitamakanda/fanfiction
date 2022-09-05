<template>
<div>
    <Logo title="Fanfiction" baseline="Sign in" />
    <Form @submit="handleLogin" :validation-schema="schema">
        <div class="mb-6">
            <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Your email</label>
            <Field name="username" type="email" id="username" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="name@flowbite.com" required="" />
            <ErrorMessage name="username" class="error" />
        </div>
        <div class="mb-6">
            <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Your password</label>
            <Field name="password" type="password" id="password" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
            <ErrorMessage name="username" class="error" />
        </div>
        <div class="flex items-start mb-6">
            <div class="flex items-center h-5">
            <Field id="remember" name="remember" type="checkbox" value="" class="w-4 h-4 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800" />
            </div>
            <label for="remember" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Remember me</label>
        </div>
        <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <span
              v-show="loading"
              class="spinner-border spinner-border-sm"
            ></span>
            <span>Login</span>
        </button>
        <div v-if="message">
            {{ message }}
        </div>
    </Form>

    <router-link to="/signup">Signup</router-link>
    <router-link to="/">Home</router-link>
</div>
</template>

<script lang="ts">
import Logo from "./../../components/base/Logo.vue";
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
    components: {
        Logo,
        Form,
        Field,
        ErrorMessage,
    },
    setup() {
        const store = useStore();
        const $router = useRouter();
        const loading = ref(false);
        const message = ref('');
        const schema = yup.object().shape({
            username: yup.string().required(),
            password: yup.string().required(),
            remember: yup.boolean(),
        });

        const isLoggedIn = computed(() => store.state['auth'].status.loggedIn);

        if (isLoggedIn.value) {
            $router.push({ name: 'Dashboard' });
        }

        const handleLogin = (data) =>{
            loading.value = true;
            store.dispatch('auth/login', { username: data.username, password: data.password })
                .then((response) => {
                    console.log(response);
                    $router.push({ name: 'Dashboard' });
                })
                .catch((error) => {
                    console.log(error)
                    message.value = error.response.data.detail.toString();
                });
            loading.value = false;
        };

        return {
            store,
            isLoggedIn,
            loading,
            message,
            schema,
            $router,
            handleLogin
        }
    }
}
</script>

<style lang="scss" scoped>

</style>