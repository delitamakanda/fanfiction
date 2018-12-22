<template>
    <div class="border border-grey-light bg-white rounded p-4 flex flex-col justify-between leading-normal">
        <div class="mb-8">
            <p class="text-sm text-grey-dark flex items-center">
            {{ fanfic.category }} / {{ fanfic.subcategory }}
          </p>
            <div class="text-black font-bold text-xl mb-2">{{ fanfic.title }}</div>
            <p v-if="fanfic.synopsis" v-html="fanfic.synopsis" class="text-grey-darker text-base">rr</p>

            <p v-if="fanfic.description && displayDescription" class="text-grey-darker text-base">
                {{ fanfic.description | readMore(120, '...') }}
            </p>
        </div>
        <div class="flex items-center">
            <div class="text-sm">
                <p class="text-black leading-none" v-if="displayAuthorName">
                    Auteur: <router-link :to="{ name: 'ShowUserFanfic', params: { username: fanfic.author.username, slug: fanfic.slug, id: fanfic.id } }" class="block mt-4 lg:inline-block lg:mt-0 text-teal hover:text-teal-darker">{{ fanfic.author.username }}</router-link>
                </p>
                <p class="text-grey-dark">Publié le : {{ fanfic.publish | date }}</p>
                <p class="text-grey-dark">{{ fanfic.genres }} / {{ fanfic.classement }} / {{ fanfic.total_likes }} {{ 'like' | pluralize(fanfic.total_likes) }} / {{ fanfic.views }} {{ 'view' | pluralize(fanfic.views) }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        fanfic: { type: Object, required: true, default: {} },
        displayAuthorName: { type: Boolean, required: false, default: true },
        displayDescription: { type: Boolean, required: false, default: false }
    }
}
</script>

<style scoped>
</style>
