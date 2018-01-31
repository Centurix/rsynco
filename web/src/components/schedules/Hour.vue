<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">On the</label>
      </div>
      <div class="field-body">
        <div class="field has-addons">
          <div class="control is-expanded">
            <input type="number" class="input" minimum="0" maximum="59" value="0">
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
  name: 'hour'
}
</script>

<style>
</style>
