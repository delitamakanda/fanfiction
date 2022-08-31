<template>
<div>
 <v-select v-bind="$attrs" v-on="$listeners" :clearSearchOnSelect="clearOnSelect">
    <slot v-for="slot in Object.keys($slots)" :name="slot" :slot="slot"></slot>
    <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
        <slot :name="slot" v-bind="scope" />
    </template>
 </v-select>
 <div>
    <slot name="caption">
        <span>{{ caption}}</span>
    </slot>
 </div>
</div>
</template>

<script lang="ts">
import vSelect from 'vue-select';

export default {
    inheritAttrs: false,
    props: {
        clearOnSelect: {
            type: Boolean,
            default: false
        },
        caption: {
            type: String,
            default: ''
        }
    },
    components: { 
        'v-select': vSelect
    },
}
</script>


<style lang="scss">
@import 'vue-select/dist/vue-select.css';
</style>