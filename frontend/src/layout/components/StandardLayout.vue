<template>
<div class="container mx-auto standardLayout">
    <header class="header"><slot name="header"></slot></header>
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

<style lang="scss" scoped>
.standardLayout {
    display: grid;
    grid-template-rows: 4rem 1fr 4rem;
    grid-template-columns: 1fr 4fr;
    height: 100vh;
}

.header,
.aside,
.content,
.footer {
    /* display: grid; */
    place-items: center;
}

.header {
    grid-column: span 2;
    @apply bg-green-200;
}
.footer {
    grid-column: span 2;
    @apply bg-gray-400;
}
.aside {
    @apply bg-indigo-200;
}
.content {
    @apply bg-purple-200;
}
</style>