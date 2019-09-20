<template>
<div>
    <Form
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        :title="title"
        :operation="operation"
        :valid="valid">
            <div class="mb-4">
                <label class="block tracking-wide text-grey-800 text-xs font-bold mb-2" for="email">
                  {{ $t('message.email') }}
                </label>
                <Input
                    type="text"
                    name="email"
                    v-model="newEmail"
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
</div>
</template>

<script>
    import confirm from '../../mixins/confirm'
    import { mapMutations } from 'vuex'

    export default {
        data(){
            return {
                errorFetch: this.$t('message.errorFetch'),
            }
        },
        props: {
            user: {type: Object, required: true, default: {}}
        },
        mixins: [
        confirm
        ],
        computed: {
            title () {
                return this.$t('message.changeUserInfos')
            },
            valid () {
                return true;
            },
            newEmail: {
                get() {
                    return this.user.email;
                },
                set(val) {
                    return this.setUserEmail(val);
                }
            }
        },
        methods: {
            ...mapMutations('user', ['setUserEmail']),
            operation ($event) {
                const message = this.$t('message.infosUpdated');

                this.confirm(message, () => {
                    this.$emit('editEmail', { email: this.newEmail, userId: this.user.id })
                });
            }
        }
    }
</script>

<style scoped>
</style>
