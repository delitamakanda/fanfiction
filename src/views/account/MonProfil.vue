<template>
    <div>
        <edit-profile></edit-profile>
        <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        :title="$t('message.changeUserInfos')"
        :operation="operation"
        :valid="valid">
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.email') }}
                </label>
                <Input
                    type="text"
                    name="email"
                    v-model="email"
                    :placeholder="$t('message.email')"/>
            </div>
            <template slot="actions">
                <div class="flex items-center justify-between">
                    <button
                    class="bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                    type="submit"
                    :disabled="!valid">
                        {{ $t('message.changeUserInfos')}}
                    </button>
                </div>
            </template>
    </Form>
    <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="$t('message.changePassword')"
            :operation="changePassword"
            :valid="validPasswordForm">
                <div class="mb-4">
                    <label class="block text-grey-800 text-sm font-bold mb-2" for="old_password">
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
                    <label class="block text-grey-800 text-sm font-bold mb-2" for="new_password">
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
                        class="bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!validPasswordForm">
                            Changer le mot de passe
                        </button>
                    </div>
                </template>
        </Form>
    </div>
</template>

<script>
import Profile from "@/components/account/Profile.vue";

import confirm from '@/mixins/confirm'
import { mapGetters, mapActions } from "vuex";

export default {
    name:'MonProfil',
    data() {
        return {
            errorFetch: this.$t('message.errorFetch'),
            old_password: '',
            new_password: '',
            newEmail: '',
        };
    },
    methods: {
        ...mapActions('user', ['changeUserMail', 'updatePassword']),
        operation ($event) {
            const message = this.$t('message.infosUpdated');

            this.confirm(message, () => {
                this.changeUserMail({email: this.newEmail, userId: this.user.id})
            });
        },
        changePassword () {
          const message = this.$t('message.passwordChangedNotification');

          this.confirm(message, () => {
              //this.updatePassword(value);
              //this.$emit('old_password', this.oldPassword)
              //this.$emit('new_password', this.newPassword)
              /*$.ajax({
                  url: '/api/change-password',
                  type: 'PUT',
                  headers: {
                      "X-CSRFToken": get_cookie("csrftoken"),
                  },
                  data: {
                      old_password: this.old_password,
                      new_password: this.new_password
                  },
                  success: function() {
                      this.old_password = this.new_password = ''
                      this.logout()
                      if (this.$route.matched.some(m => m.meta.private)) {
                          this.$router.push({ name: 'Login' })
                      }
                  }.bind(this),
                  error: function (error) {
                      console.log(error);
                  }.bind(this)
              })*/
          });
      },
    },
    mixins: [
        confirm
    ],
    computed: {
        ...mapGetters("user", ["user"]),
        valid() {
            return true
        },
        validPasswordForm() {
            return !!this.old_password && !!this.new_password
        },
        email: {
            get() {
                return this.user.email
            },
            set(val) {
                this.newEmail = val
            }
        }
    },
    components: {
        "edit-profile": Profile,
    }
}
</script>

<style scoped>

</style>