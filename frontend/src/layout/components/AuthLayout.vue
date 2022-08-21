<template>
<div class="container mx-auto authLayout">
    <main class="content">
        <slot name="content"></slot>
    </main>
    <footer class="footer">
        <slot name="footer"></slot>
    </footer>
</div>
</template>

<script lang="ts">
export default {}
</script>

<style lang="scss" scoped>
.authLayout {
    display: grid;
    grid-template-rows: 1fr 4rem;
    grid-template-columns: 1fr;
    height: 100vh;
    @apply bg-purple-300;
}

.content,
.footer {
    display: grid;
    place-items: center;
}

.content {
    grid-area: 1 / 1 / 2 / 2;
    @apply bg-purple-200;
}

.footer {
    grid-area: 2 / 1 / 3 / 2;
    @apply bg-gray-400;
}

</style>