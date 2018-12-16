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
                    <avatar v-if="!account.photo" ref="avatar" :email="this.user.email" />
                    <img v-else :src="account.photo" class="inline-block h-30 w-24 mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" />
                    <img :src="photo" v-if="displayPhoto" class="inline-block h-30 w-24 mx-auto mb-4 sm:mb-0 sm:mr-4 sm:ml-0" />
                    <label class="block text-grey-darker text-sm font-bold mb-2" for="photo">
                        {{ $t('message.Photo') }}
                    </label>
                    <a class="text-teal hover:text-teal-darker cursor-pointer" @click="removePhoto">{{ $t('message.removePhotoText' )}}</a>
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
import { mapGetters } from 'vuex'

export default {
    name: 'Profile',
    data(){
        return {
            errorFetch: this.$t('message.errorFetch'),
            account: {},
            date_of_birth: '',
            photo: '',
            bio: '',
            displayPhoto: false,
        }
    },
    mixins: [
        confirm,
        RemoteData({
            account () {
                return `users/${this.user.id}/edit/profile`;
            }
        })
    ],
    computed: {
        ...mapGetters('user', ['user']),
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
                  url: `/api/users/${this.user.id}/edit/profile`,
                  type: 'PUT',
                  headers: {
                      "X-CSRFToken": get_cookie("csrftoken")
                  },
                  data: {
                      date_of_birth: this.account.date_of_birth,
                      bio: this.account.bio,
                      photo: this.photo,
                      user: this.user.id
                  },
                  success: function(response) {
                      this.account.photo = response.photo
                      this.displayPhoto = false
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
          this.displayPhoto = true;
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
      removePhoto () {
          const message = this.$t('message.warningRemovePhoto');

          this.confirm(message, () => {
              $.ajax({
                  url: `/api/remove-photo/${this.account.id}`,
                  type: 'PUT',
                  headers: {
                      "X-CSRFToken": get_cookie("csrftoken")
                  },
                  success: function(response) {
                      this.photo = ''
                      this.account.photo = ''
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
