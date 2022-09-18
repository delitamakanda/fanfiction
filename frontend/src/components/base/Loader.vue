<template>
<div class="loading" :class="{'visible': isVisible }">
    <div class="spinner spinner1"></div>
</div>
 </template>

 <script lang="ts">
export default {
    props: ['isVisible'],
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.loading {
    display: none;


    &.visible {
        display: block;
        pointer-events: all;
    }
}

.spinner {
    position: relative;
    width: 125px;
    height: 125px;
}

.spinner::before, .spinner::after {
    position: absolute;
    display: block;
    content: "";
    border-style: solid;
    border-width: 4px;
    border-radius: 50%;
}

@keyframes rotate-animation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
@keyframes anti-rotate-animation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(-360deg);
    }
}
.spinner.spinner1::before {
    top: 0;
    left: 0;
    width: 117px;
    height: 117px;
    border-top-color: #21212100;
    border-right-color: #212121;
    border-bottom-color: #212121;
    border-left-color: #21212100;
    animation: rotate-animation 1s linear 0s infinite;
}
.spinner.spinner1::after {
    top: 17.55px;
    left: 17.55px;
    width: 81.9px;
    height: 81.9px;
    border-right-color: #212121;
    border-top-color: rgba(33, 33, 33, 0);
    border-left-color: rgba(33, 33, 33, 0);
    border-bottom-color: #212121;
    animation: anti-rotate-animation 0.85s linear 0s infinite;
}

.loading {
    position: fixed;
    top: 50%;
    left: 50%;
    z-index: 88;
    width: auto;
    transform: translate(-50%, -50%);
}
    
</style>
    