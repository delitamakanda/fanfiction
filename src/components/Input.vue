<template>
    <div class="row">
        <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
            :class="inputClass"
            :id="name"
            :name="name"
            :type="type"
            :value.prop="text"
            :placeholder="placeholder"
            @input="update"
            v-bind="$attrs"
        />
    </div>
</template>

<script>
export default {
  name: 'Input',
  model: {
      prop: 'text',
      event: 'update',
  },
  props: {
      name: {
          type: String,
      },
      type: {
          type: String,
          default: 'text'
      },
      text: {
          required: true
      },
      placeholder: {
          type: String
      },
      invalid: {
          type: Boolean,
          default: false
      },
  },
  data () {
    return {
    }
},
computed: {
    inputClass () {
        return {
            'invalid': this.invalid,
        }
    },
},
methods: {
    update (event) {
        this.$emit('update', event.currentTarget.value)
    },
}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
