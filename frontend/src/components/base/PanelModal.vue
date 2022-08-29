<template>
    <div class="lazyModal" :class="{'open' : open}">
        <slot></slot>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        open: {
            type: Boolean,
            default: false,
        },
    }
}
</script>

<style lang="scss">
.lazyModal {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 2;
    width: 40vw;
    min-height: 100vh;
    @apply bg-gray-100 shadow-lg transition-transform transform translate-x-full duration-500;

    &.open {
        @apply translate-x-0;
    }
}
</style>