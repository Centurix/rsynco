<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">On the</label>
      </div>
      <div class="field-body">
        <div class="field has-addons">
          <div class="control is-expanded">
            <input type="number" class="input" min="0" max="59" v-model.number="startMinute" v-on:change="updated()">
          </div>
          <div class="control">
            <label class="button is-primary">Minute</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'hour',
  props: [
    'minute'
  ],
  watch: {
    minute: function (newVal, oldVal) {
      this.startMinute = this.minute
    }
  },
  created () {
    this.startMinute = this.minute
  },
  data () {
    return {
      startMinute: 0
    }
  },
  methods: {
    updated () {
      this.$emit('changedMinute', this.startMinute)
    }
  }
}
</script>

<style>
</style>
