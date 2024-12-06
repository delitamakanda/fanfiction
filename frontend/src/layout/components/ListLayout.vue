<template>
    <div class="listLayout">
        <slot></slot>
    </div>
</template>

<script lang="ts">
export default {

}
</script>

<style>
.listLayout>* {
    min-height: 150px;
}
</style>