<template>
<div class="gridLayout">
    <slot></slot>
</div>
</template>

<script lang="ts">
export default {
    
}
</script>

<style lang="scss">
.gridLayout {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    @apply gap-8 grid;
}
</style>