<template>
    <div class="p-8 items-center h-screen justify-content flex-col">
        <h2 class="text-2xl font-semibold mb-4"> title </h2>
        <p class="mb-4">text</p>
        <base-button @click.prevent="$emit('close-panel')">Close button</base-button>
    </div>
</template>

<script lang="ts">
export default {
    emits: ['close-panel'],
}
</script>
