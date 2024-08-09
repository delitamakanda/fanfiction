<template>
    <div class="fanficListCard">
        <div class="fanficImageContainer">
            <img v-if="fanfic.picture" class="fanficImage" :src="fanfic.picture" :alt="fanfic.title" />
        </div>
        <div class="px-4">
            <div class="flex flex-col h-full">
                <p class="font-semibold text-lg mb-2">{{ fanfic.title }}</p>
                <div class="flex flex-col justify-between h-full">
                    <p class="text-xl">{{ fanfic.author }}</p>
                    <p class="text-gray-500">{{ fanfic.category }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        fanfic: {
            type: Object,
        }
    }
}
</script>

<style lang="scss">
.fanficListCard {
    @apply bg-white p-4 rounded-md shadow-md flex justify-start;

    &:hover {
        @apply shadow-lg cursor-pointer;
    }
}

.fanficImageContainer {
    @apply w-20 mr-4 flex items-center justify-center flex-shrink-0;
}

.fanficImage {
    @apply max-w-full max-h-full block h-auto mx-4;
}
</style>