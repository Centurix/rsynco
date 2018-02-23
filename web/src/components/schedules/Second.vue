<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Every</label>
      </div>
      <div class="field-body">
        <div class="field has-addons">
          <div class="control is-expanded">
            <input type="number" class="input" min="10" value="10" v-model="seconds">
          </div>
          <div class="control">
            <label class="button is-primary">Second(s)</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'second',
  data () {
    return {
      seconds: 10
    }
  }
}
</script>

<style>
</style>
