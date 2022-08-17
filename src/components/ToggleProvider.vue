<template>
    <slot></slot>
</template>

<script lang="ts">

export default {
    props: {
        on: {
            type: Boolean,
            default: false
        },
        data() {
            return {
                isOn: this.on
            }
        },
        render() {
            const { toggle, isOn, turnOn, turnOff } = this;
            return this.$slots.default({
                toggle,
                isOn,
                turnOn,
                turnOff,
            })
        },
        methods: {
            turnOff () {
                this.isOn = false;
            },
            turnOn () {
                this.isOn = true;
            },
            toggle () {
                this.isOn = !this.isOn;
            }
        },
    }
}
</script>