<template>
    <router-link class="no-underline" :key="fanfic.id" :to="{
        name: 'Detail',
        params: {
            slug: fanfic.slug,
            id: fanfic.id
        },
    }">
    <div class="border border-grey-light bg-white rounded p-4 flex flex-col justify-between leading-normal">
        <div class="mb-8">
            <p class="text-sm text-grey-dark italic flex items-center float-right">
            {{ fanfic.status }}
            </p>
            <p class="text-sm text-grey-dark flex items-center">
            {{ fanfic.category }} / {{ fanfic.subcategory }}
          </p>
            <div class="text-black font-bold text-xl mb-2">{{ fanfic.title }}</div>
            <p v-if="fanfic.synopsis" v-html="fanfic.synopsis" class="text-grey-darker text-base"></p>

            <p v-if="fanfic.description" class="text-grey-darker text-base">
                {{ fanfic.description | readMore(120, '...') }}
            </p>
        </div>
        <div class="flex items-center">
            <div class="text-sm">
                <p class="text-black leading-none">
                    {{ $t('message.authorLabel') }} : {{ fanfic.author.username }}
                </p>
                <p class="text-grey-dark">{{ $t('message.publishedAtLabel' )}} : {{ fanfic.publish | date }}</p>
                <p class="text-grey-dark">{{ fanfic.genres }} / {{ fanfic.classement }} / {{ fanfic.total_likes }} {{ 'like' | pluralize(fanfic.total_likes) }} / {{ fanfic.views }} {{ 'view' | pluralize(fanfic.views) }}</p>
            </div>
        </div>
    </div>
    </router-link>
</template>

<script>
export default {
    props: {
        fanfic: { type: Object, required: true, default: {} }
    }
}
</script>

<style scoped>
</style>
