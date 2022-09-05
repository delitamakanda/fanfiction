<template>
    <div class="flex">
        <img src="./../../assets/images/logo.png" class="mr-3 h-6 sm:h-9" :alt="title" />
        <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">{{title}}</span>
    </div>
    {{ baseline }}
</template>

<script lang="ts">
export default {
    props: {
        title: {
            type: String,
            required: true
        },
        baseline: {
            type: String,
            required: false
        }
    }
}
</script>