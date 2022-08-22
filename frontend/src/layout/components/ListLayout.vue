<template>
<div class="listLayout">
    <slot></slot>
</div>
</template>

<script lang="ts">
export default {
    
}
</script>

<style lang="scss">
.listLayout {
    > * {
        min-height: 150px;
    }
}
</style>