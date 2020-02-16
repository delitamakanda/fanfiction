<template>
  <div>
    <div
      class="error bg-red-lightest border border-red-300 text-red-800 px-4 py-3 rounded relative"
      v-if="hasRemoteErrors"
      role="alert"
    >{{ errorFetch }}</div>
    <Loading v-if="remoteDataBusy" />

    <Form
      class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
      :title="$t('message.addNewSocialNetwork')"
      :operation="operation"
      :valid="valid"
    >
      <div class="mb-4 mt-4" v-if="profile && profile.social && profile.social.length > 0">
        <ul class="list-reset" v-for="(s, i) in profile.social" :key="i">
          <li>
            <a
              :title="s.network"
              class="hover:text-teal-dark text-teal font-bold mr-4"
              :href="'https://' + s.network + '.com/' + s.nichandle"
              target="_blank"
            >{{ s.nichandle }}</a>(<em>{{ s.network }}</em>) <button @click.prevent="deleteAccount(s.id)">x</button>
          </li>
        </ul>
      </div>
      <div class="mb-4">
        <label
          class="block text-grey-darker text-sm font-bold mb-2"
          for="network"
        >{{ $t('message.network') }}</label>
        <div class="inline-block relative w-64">
          <select
            class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
            id="network"
            v-model="network"
          >
            <option value>Sélectionner</option>
            <option v-for="(network, i) in networks" :value="network" :key="i">{{ network }}</option>
          </select>
          <div
            class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
          >
            <svg
              class="fill-current h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
            >
              <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
            </svg>
          </div>
        </div>
      </div>
      <div class="mb-6">
        <label
          class="block text-grey-800 text-sm font-bold mb-2"
          for="nichandle"
        >{{ $t('message.nichandle') }}</label>
        <Input
          name="nichandle"
          type="text"
          v-model="nichandle"
          :placeholder="$t('message.nichandle')"
        />
      </div>
      <template slot="actions">
        <div class="flex items-center justify-between">
          <button
            class="bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
            type="submit"
          >{{ $t('message.addNewSocialNetwork') }}</button>
        </div>
      </template>
    </Form>
  </div>
</template>

<script>
import confirm from "@/mixins/confirm";
import get_cookie from "@/cookie";
import RemoteData from "@/mixins/RemoteData";
import { mapGetters, mapState, mapActions } from "vuex";

export default {
  name: "Social",
  data() {
    return {
      errorFetch: this.$t("message.errorFetch"),
      account: {},
      network: "",
      networks: ["twitter", "facebook", "pinterest", "instagram"],
      nichandle: "",
      socialaccount: {}
    };
  },
  mixins: [
    confirm,
    RemoteData({})
  ],
  computed: {
    ...mapGetters('user', ['user']),
    ...mapState('user', ['profile']),
    valid() {
      return !!this.network && !!this.nichandle;
    }
  },
  async created() {
    this.fetchProfileUser({ username: this.user.username })
  },
  methods: {
    ...mapActions('user', ['fetchProfileUser', 'deleteSocialAccount', 'createSocialAccount']),
    deleteAccount(accountId) {
      this.deleteSocialAccount({ id: accountId })
    },
    operation() {
      const message = this.$t("message.socialNetworkAdded");

      this.confirm(message, () => {
        this.createSocialAccount({
          account: this.profile.id,
          network: this.network,
          nichandle: this.nichandle,
          user: this.user.id
        });
      });
    }
  }
};
</script>

<style scoped>
</style>