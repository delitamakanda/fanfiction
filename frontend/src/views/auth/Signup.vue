<template>
<div>
    <Logo title="Fanfiction" baseline="Sign in" />
    <Form @submit="handleRegister" :validation-schema="schema">
    <div class="mb-6">
        <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Your username</label>
        <Field type="text" name="username" id="username" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light" placeholder="" required="" />
        <ErrorMessage name="username" class="error" />
    </div>
    <div class="mb-6">
        <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Your email</label>
        <Field type="email" name="email" id="email" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light" placeholder="name@flowbite.com" required="" />
        <ErrorMessage name="email" class="error" />
    </div>
    <div class="mb-6">
        <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Your password</label>
        <Field type="password" id="password" name="password" class="block mbshadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light" required="" />
        <ErrorMessage name="password" class="error" />
    </div>
    <div class="mb-6">
        <label for="repeatPassword" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Repeat password</label>
        <Field type="password" id="repeatPassword" name="repeatPassword" class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light" required=" " />
        <ErrorMessage name="repeatPassword" class="error" />
    </div>
    <div class="flex items-start mb-6">
        <div class="flex items-center h-5">
        <input id="terms" type="checkbox" value="" class="w-4 h-4 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800" required="">
        </div>
        <label for="terms" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">I agree with the <span @click="openModal" class="text-blue-600 hover:underline dark:text-blue-500">terms and conditions</span></label>
    </div>
    <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            <span
              v-show="loading"
              class="spinner-border spinner-border-sm"
            ></span>
            <span>Signup</span>
        </button>
        <div v-if="messages">
            <template v-for="(message, idx) in messages" :key="idx">
                <div>
                    {{ message }}
                </div>
            </template>
        </div>
    </Form>

    <router-link to="/signin">Signin</router-link>
    <router-link to="/">Home</router-link>
    <Modal ref="modal">
        <template v-slot:header>header</template>
        <template v-slot:body>body</template>
    </Modal>
</div>
</template>

<script lang="ts">
import Logo from "./../../components/base/Logo.vue";
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import Modal from "../../components/common/Modal.vue";

export default {
    components: {
        Logo,
        Form,
        Field,
        ErrorMessage,
        Modal,
    },
    mounted() {
        (<any>this).$root.$modal = (<any>this).$refs.modal.open;
    },
    methods: {
        openModal() {
            (<any>this).$root.$modal()
        }
    },
    setup() {
        const store = useStore();
        const $router = useRouter();
        const loading = ref(false);
        const messages = ref([]) as any; 
        const schema = yup.object().shape({
            username: yup.string().required(),
            email: yup.string().email().required(),
            password: yup.string().required(),
            repeatPassword: yup.string().oneOf([yup.ref('password'), null], 'Passwords must match'),
        });

        const isLoggedIn = computed(() => store.state['auth'].status.loggedIn);

        if (isLoggedIn.value) {
            $router.push({ name: 'Dashboard' });
        }

        const handleRegister = (data) => {
            loading.value = true;
            store.dispatch('auth/signup', data)
                .then(() => {
                    $router.push({ name: 'Signin' });
                })
                .catch((error) => {
                    console.log(error);
                    messages.value.push(error.response.data);
                });
        };

        return {
            store,
            $router,
            loading,
            messages,
            schema,
            handleRegister,
        };
    }
}
</script>

<style lang="scss" scoped>

</style>