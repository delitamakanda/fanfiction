<template>
    <div>
        <div class="px-2 mb-4">
            <div class="flex -mx-2">
                <div class="w-full sm:w-1/2 px-2">
                    <edit-user></edit-user>
                </div>
                <div class="w-full sm:w-1/2 px-2">
                    <edit-profile></edit-profile>
                </div>
            </div>
        </div>
        <div class="px-2">
            <div class="flex -mx-2">
                <div class="w-full sm:w-1/2 px-2">
                    <edit-password></edit-password>
                </div>
                <div class="w-full sm:w-1/2 px-2">
                    <edit-social></edit-social>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Profile from './account/Profile.vue'
import Edit from './account/Edit.vue'
import Social from './account/Social.vue'
import Password from './account/Password.vue'

export default {
    name: 'EditAccount',
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
