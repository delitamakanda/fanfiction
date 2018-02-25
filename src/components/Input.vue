<template>
    <div>
        <input
            class=""
            :class="inputClass"
            :name="name"
            :type="type"
            :value.prop="text"
            :placeholder="placeholder"
            @input="update"
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
