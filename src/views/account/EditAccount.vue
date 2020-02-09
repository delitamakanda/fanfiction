<template>
    <div>
        <!-- <div class="px-2 mb-4">
            <div class="flex -mx-2">
                <div class="w-full md:w-1/2 px-2">
                    <edit-user :user="user" @editEmail="emailChanged"></edit-user>
                    <edit-password :old_password="old_password" :new_password="new_password"></edit-password>
                </div>
                <div class="w-full md:w-1/2 px-2">
                    <edit-profile></edit-profile>
                    <edit-social></edit-social>
                </div>
            </div>
        </div> -->
    </div>
</template>

<script>
import Profile from '@/components/account/Profile.vue'
import Edit from '@/components/account/Edit.vue'
import Social from '@/components/account/Social.vue'
import Password from '@/components/account/Password.vue'

import { mapGetters, mapActions } from 'vuex'

export default {
    computed: {
        ...mapGetters('user', ['user'])
    },
    data() {
        return {
            old_password: '',
            new_password: ''
        };
    },
    methods: {
        ...mapActions('user', ['changeUserMail', 'updatePassword']),
        emailChanged (value) {
            this.changeUserMail(value)
        },
        passwordChange(a,b) {
            console.log(a)
            console.log(b)
            //this.updatePassword(value)
        }
    },
    components: {
        'edit-profile': Profile,
        'edit-user': Edit,
        'edit-social': Social,
        'edit-password': Password,
    }
}
</script>

<style scoped>
</style>
