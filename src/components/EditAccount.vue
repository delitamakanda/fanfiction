<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <Loading v-if="remoteDataBusy" />
        {{ $t('message.dateJoined') }} {{ user.date_joined | date }}
        <div class="px-2 mb-4">
            <div class="flex -mx-2">
                <div class="w-full sm:w-1/2 px-2">
                    <Form
                        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                        :title="$t('message.changeUserInfos')"
                        :operation="editUser"
                        :valid="validAccount">
                            <div class="mb-4">
                                <label class="block tracking-wide text-grey-darker text-xs font-bold mb-2" for="email">
                                  {{ $t('message.email') }}
                                </label>
                                <Input
                                    type="text"
                                    name="email"
                                    v-model="user.email"
                                    :placeholder="$t('message.email')"/>
                            </div>
                            <template slot="actions">
                                <div class="flex items-center justify-between">
                                    <button
                                    class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                                    type="submit"
                                    :disabled="!validAccount">
                                        {{ $t('message.changeUserInfos')}}
                                    </button>
                                </div>
                            </template>
                    </Form>
                </div>
                <div class="w-full sm:w-1/2 px-2">
                    <Form
                        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                        :title="$t('message.changeProfileEdit')"
                        :operation="profile"
                        :valid="validAccount"
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
                                    :disabled="!validAccount">
                                        {{ $t('message.changeProfileEdit')}}
                                    </button>
                                </div>
                            </template>
                    </Form>
                </div>
            </div>
        </div>
        <div class="px-2">
            <div class="flex -mx-2">
                <div class="w-full sm:w-1/2 px-2">
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
                <div class="w-full sm:w-1/2 px-2">
                    <Form
                        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                        :title="$t('message.addNewSocialNetwork')"
                        :operation="social"
                        :valid="valid">
                            <div class="mb-4">
                                <label class="block text-grey-darker text-sm font-bold mb-2" for="network">
                                    {{ $t('message.network') }}
                                </label>
                                <div class="relative">
                                  <select class="block appearance-none w-full bg-white border border-grey-light hover:border-grey px-4 py-2 pr-8 rounded shadow" id="network" v-model="network">
                                      <option value="">Sélectionner</option>
                                      <option v-for="network in networks" :value="network ">{{ network }}</option>
                                  </select>
                                  <div class="pointer-events-none absolute pin-y pin-r flex items-center px-2 text-grey-darker">
                                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                                  </div>
                                </div>
                                </div>
                            <div class="mb-6">
                                <label class="block text-grey-darker text-sm font-bold mb-2" for="nichandle">
                                    {{ $t('message.nichandle') }}
                                </label>
                                <Input
                                    name="nichandle"
                                    type="text"
                                    v-model="nichandle"
                                    :placeholder="$t('message.nichandle')" />
                            </div>
                            <template slot="actions">
                                <div class="flex items-center justify-between">
                                    <button
                                    class="bg-blue hover:bg-blue-dark text-white font-bold py-2 px-4 rounded"
                                    type="submit">
                                        {{ $t('message.addNewSocialNetwork') }}
                                    </button>
                                </div>
                            </template>
                    </Form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import confirm from '../mixins/confirm'
import get_cookie from '../cookie'
import RemoteData from '../mixins/RemoteData'

export default {
    name: 'EditAccount',
    data(){
        return {
            errorFetch: this.$t('message.errorFetch'),
            account: {},
            user: {},
            old_password: '',
            new_password: '',
            network: '',
            networks: ['twitter', 'facebook', 'pinterest', 'instagram'],
            nichandle: '',
            date_of_birth: '',
            photo: '',
            bio: '',
            username: '',
            email: ''
        }
    },
    mixins: [
        confirm,
        RemoteData({
            account () {
                return `users/${this.$state.user.id}/edit/profile`;
            },
            user () {
                return `users/${this.$state.user.id}`;
            }
        })
    ],
    computed: {
      title () {
        return this.$t('message.changePassword')
      },
      valid () {
        return !!this.old_password && !!this.new_password || !!this.network && !!this.nichandle
      },
      validAccount () {
          return true;
      }
    },
    methods: {
      operation () {
          const message = this.$t('message.passwordChangedNotification');

          this.confirm(message, () => {
              $.ajax({
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
                      if (this.$route.matched.some(m => m.meta.private)) {
                          this.$router.push({ name: 'Login' })
                      }
                  }.bind(this),
                  error: function (error) {
                      console.log(error);
                  }.bind(this)
              })
          });
      },
      social () {
          const message = this.$t('message.socialNetworkAdded');

          this.confirm(message, () => {
              $.ajax({
                  url: '/api/users/social-account',
                  type: 'POST',
                  headers: {
                      "X-CSRFToken": get_cookie("csrftoken"),
                  },
                  data: {
                      account: this.account.id,
                      network: this.network,
                      nichandle: this.nichandle,
                      user: this.$state.user.id
                  },
                  success: function() {
                      this.network = this.nichandle = ''
                  }.bind(this),
                  error: function (error) {
                      console.log(error);
                  }.bind(this)
              })
          });
      },
      profile () {
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
     editUser() {
          const message = this.$t('message.infosUpdated');

          this.confirm(message, () => {
              $.ajax({
                  url: `/api/users/${this.$state.user.id}`,
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
