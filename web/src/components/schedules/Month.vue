<template>
  <div>
    <div class="field is-horizontal">
      <!-- Monthly -->
      <div class="field-label is-normal">
        <label class="label">Run</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select>
                <option>Day of the Month</option>
                <option>Day of the Week</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'month'
}
</script>

<style>
</style>
