<template>
<div class="authLayout">
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
}

.content,
.footer {
    display: grid;
}

.content {
    grid-area: 1 / 1 / 2 / 2;
}

.footer {
    grid-area: 2 / 1 / 3 / 2;
}

</style>