<template>
    <div>
        <div class="error bg-red-lightest border border-red-light text-red-dark px-4 py-3 rounded relative" v-if="hasRemoteErrors" role="alert">
            {{ errorFetch }}
        </div>
        <Loading v-if="remoteDataBusy" />
        <Form
            class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            :title="$t('message.addNewSocialNetwork')"
            :operation="operation"
            :valid="valid">
                <div class="mb-4 mt-4" v-if="socialaccount.length > 0">
                    <ul class="list-reset" v-for="social in socialaccount">
                        <li><a :title="social.network" class="hover:text-teal-dark text-teal font-bold mr-4" :href="'https://' + social.network + '.com/' + social.nichandle" target="_blank">{{ social.nichandle }}</a>(<em>{{ social.network }}</em>)</li>
                    </ul>
                </div>
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
</template>

<script>
import confirm from '../../mixins/confirm'
import get_cookie from '../../cookie'
import RemoteData from '../../mixins/RemoteData'

export default {
    name: 'Social',
    data(){
        return {
            errorFetch: this.$t('message.errorFetch'),
            account: {},
            network: '',
            networks: ['twitter', 'facebook', 'pinterest', 'instagram'],
            nichandle: '',
            socialaccount: {}
        }
    },
    mixins: [
        confirm,
        RemoteData({
            account () {
                return `users/${this.$state.user.id}/edit/profile`;
            },
        })
    ],
    computed: {
        title () {
            return this.$t('message.addNewSocialNetwork')
        },
        valid () {
            return !!this.network && !!this.nichandle
        },
    },
    async created () {
        this.getSocialAccount();
    },
    methods: {
        async getSocialAccount () {
            this.account = await this.$fetch(`users/${this.$state.user.id}/edit/profile`)
            this.socialaccount = await this.$fetch(`users/${this.account.id}/socialaccount`)
        },
        operation () {
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
                    success: function(response) {
                        this.network = this.nichandle = ''
                        this.socialaccount.push(response)
                    }.bind(this),
                    error: function (error) {
                        console.log(error);
                    }.bind(this)
                })
            });
        },
    }
}
</script>

<style scoped>
</style>
