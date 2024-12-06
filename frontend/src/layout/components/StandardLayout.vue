<template>
    <div class="standardLayout">
        <header class="header">
            <slot name="header"></slot>
        </header>
        <aside class="aside">
            <slot name="aside"></slot>
        </aside>
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

<style scoped>
.standardLayout {
    display: grid;
    grid-template-rows: 4rem 1fr 4rem;
    grid-template-columns: 1fr 4fr;
}

.header,
.aside,
.content,
.footer {
    display: grid;
}

.header {
    grid-column: span 2;
}

.footer {
    grid-column: span 2;
}

.content {
    @apply p-4;
}
</style>