<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <Loading v-if="remoteDataBusy" />
        {{ $t('message.dateJoined') }} {{ infos.date_joined | date }}
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="title"
            :operation="operation"
            :valid="valid">
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="email">
                      {{ $t('message.email') }}
                    </label>
                    <Input
                        type="text"
                        name="email"
                        v-model="infos.email"
                        :placeholder="$t('message.email')"/>
                </div>
                <template slot="actions">
                    <div class="flex items-center justify-between">
                        <button
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!valid">
                            {{ $t('message.changeUserInfos')}}
                        </button>
                    </div>
                </template>
        </Form>
    </div>
</template>

<script>
import confirm from '../../mixins/confirm'
import get_cookie from '../../cookie'
import RemoteData from '../../mixins/RemoteData'
import { mapGetters } from 'vuex'

export default {
    data(){
        return {
            errorFetch: this.$t('message.errorFetch'),
            infos: {},
            username: '',
            email: ''
        }
    },
    mixins: [
        confirm,
        RemoteData({
            infos () {
                return `users/${this.user.id}`;
            }
        })
    ],
    computed: {
        ...mapGetters('user', ['user']),
        title () {
            return this.$t('message.changeUserInfos')
        },
        valid () {
          return true;
        }
    },
    methods: {
     operation () {
          const message = this.$t('message.infosUpdated');

          this.confirm(message, () => {
              $.ajax({
                  url: `/api/users/${this.user.id}`,
                  type: 'PUT',
                  headers: {
                      "X-CSRFToken": get_cookie("csrftoken")
                  },
                  data: {
                      email: this.user.email
                  },
                  success: function(response) {
                      console.log(response);
                  }.bind(this),
                  error: function (error) {
                      console.log(error);
                  }.bind(this)
              })
          });
      }
    }
}
</script>

<style scoped>
</style>
