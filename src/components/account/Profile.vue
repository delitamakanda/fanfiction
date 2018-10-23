<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <Loading v-if="remoteDataBusy" />
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="title"
            :operation="operation"
            :valid="valid"
            enctype="multipart/form-data"
            method="post">
                <div class="mb-4">
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="date_of_birth">
                        {{ $t('message.dateOfBirth') }}
                    </label>
                    <Input
                        name="date_of_birth"
                        type="date"
                        v-model="account.date_of_birth"
                        :placeholder="$t('message.dateOfBirth')"/>
                    </div>
                <div class="mb-6">
                    <img v-if="!photo" :src="account.photo" class="block h-30 w-24 mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" />
                    <img v-else :src="photo" class="block h-30 w-24 mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" />
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="photo">
                        {{ $t('message.Photo') }}
                    </label>
                    <input
                        name="photo"
                        type="file"
                        :placeholder="$t('message.Photo')"
                        @change="onFileChanged"
                        accept="image/*"
                        ref="fileInput" />
                </div>
                <div class="mb-4">
                    <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="bio">
                      {{ $t('message.Biography') }}
                    </label>
                    <Input
                        type="textarea"
                        name="bio"
                        v-model="account.bio"
                        :placeholder="$t('message.Biography')"
                        maxlength="1000"
                        rows="8" />
                </div>
                <template slot="actions">
                    <div class="flex items-center justify-between">
                        <button
                        class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                        type="submit"
                        :disabled="!valid">
                            {{ $t('message.changeProfileEdit')}}
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


export default {
    name: 'Profile',
    data(){
        return {
            errorFetch: this.$t('message.errorFetch'),
            account: {},
            date_of_birth: '',
            photo: '',
            bio: ''
        }
    },
    mixins: [
        confirm,
        RemoteData({
            account () {
                return `users/${this.$state.user.id}/edit/profile`;
            }
        })
    ],
    computed: {
      title () {
        return this.$t('message.changeProfileEdit')
      },
      valid () {
          return true;
      }
    },
    methods: {
      operation () {
          const message = this.$t('message.profileUpdated');

          this.confirm(message, () => {
              $.ajax({
                  url: `/api/users/${this.$state.user.id}/edit/profile`,
                  type: 'PUT',
                  headers: {
                      "X-CSRFToken": get_cookie("csrftoken")
                  },
                  data: {
                      date_of_birth: this.account.date_of_birth,
                      bio: this.account.bio,
                      photo: this.photo,
                      user: this.$state.user.id
                  },
                  success: function(response) {
                      console.log(response);
                  }.bind(this),
                  error: function (error) {
                      console.log(error);
                  }.bind(this)
              })
          });
      },
      onFileChanged (e) {
          const files = e.target.files || e.dataTransfer.files;
          if (!files.length) {
              return;
          }
          this.createImage(files[0]);
      },
      createImage(file) {
          let photo = new Image();
          let reader = new FileReader();
          let vm = this;

          reader.onload = (e) => {
              vm.photo = e.target.result;
          };

          reader.readAsDataURL(file);
      },
    }
}
</script>

<style scoped>
</style>