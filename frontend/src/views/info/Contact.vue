<template>
   <div>
      <h2 class="mb-4 text-3xl font-extrabold tracking-tight leading-none text-gray-900 md:text-4xl dark:text-white">{{
         $t('message.contact.title') }}</h2>
      <p class="my-4 text-lg text-gray-500">{{ $t('message.contact.baseline') }}</p>

      <Form @submit="sendMail" :validation-schema="schema" class="mb-6">
         <div v-if="!currentUser" class="mb-6">
            <label for="from_email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{
               $t('message.contact.fromEmailLabel') }}</label>
            <Field type="email" id="from_email" name="from_email"
               class="block mb-2 text-sm font-medium textbg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-teal-500 focus:border-teal-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-teal-500 dark:focus:border-teal-500"
               :placeholder="$t('message.contact.placeholderEmail')" />
            <ErrorMessage name="from_email" class="error" />
         </div>
         <div class="mb-6">
            <label for="subject" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{
               $t('message.contact.subjectLabel') }}</label>
            <Field type="text" name="subject" id="subject"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-teal-500 focus:border-teal-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-teal-500 dark:focus:border-teal-500"
               :placeholder="$t('message.contact.subjectPlaceholder')" />
            <ErrorMessage name="subject" class="error" />
         </div>
         <div class="mb-6">
            <label for="message" class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400">{{
               $t('message.contact.messageLabel') }}</label>
            <Field name="message" as="textarea" id="message" rows="4"
               class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-teal-500 dark:focus:border-teal-500"
               :placeholder="$t('message.contact.messagePlaceholder')" />
            <ErrorMessage name="message" class="error" />
         </div>
         <button type="submit"
            class="text-white bg-teal-700 hover:bg-teal-800 w-full focus:ring-4 focus:ring-teal-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-teal-600 dark:hover:bg-teal-700 focus:outline-none dark:focus:ring-teal-800 block">
            <span v-show="loading" class="spinner-border spinner-border-sm"></span>
            <span>{{ $t('message.contact.sendButton') }}</span>
         </button>
      </Form>
   </div>
</template>

<script lang="ts">
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import { ref, computed } from 'vue';
import { withAsync } from '../../api/helpers/withAsync';
import { contactMail } from '../../api/infoApi';
import { useStore } from 'vuex';

export default {
   components: {
      Form,
      Field,
      ErrorMessage,
   },
   setup() {
      const store = useStore();

      const currentUser = computed(() => store.state['user'].user);

      const loading = ref(false);
      const message = ref('');
      const schema = yup.object().shape({
         from_email: currentUser.value ? yup.string().email() : yup.string().email().required(),
         subject: yup.string().required(),
         message: yup.string().required(),
      });


      const sendMail = async (data) => {
         if (currentUser.value) {
            data.from_email = currentUser.value.email;
         }
         loading.value = true;
         const { response, error } = await withAsync(contactMail, data);
         if (error) {
            loading.value = false;
            return;
         }
         loading.value = false;
         store.dispatch('snackbar/showSnackbar', {
            message: 'Your message has been sent',
            type: 'success',
         });
      }


      return {
         schema,
         loading,
         message,
         sendMail,
         store,
         currentUser,
      }
   }
}
</script>
