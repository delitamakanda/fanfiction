<template>
    <div class="p-8 bg-red-300 h-screen flex items-center justify-center">
        <div class="flex items-center flex-col">
            <p class="text-read-800 font-bold text-center mb-4">
                oops text bla 
            </p>
            <base-button @click.prevent="$emit('close-panel')">Close panel</base-button>
            <base-button @click.prevent="$emit('retry')">Try again</base-button>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    emits: ['close-panel', 'retry'],
}
</script>