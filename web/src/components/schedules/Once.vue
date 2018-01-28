<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Start</label>
      </div>
      <div class="field-body">
        <div class="field">
          <datepicker input-class="input" ></datepicker>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Time</label>
      </div>
      <div class="field-body">
        <div class="field">
          <vue-timepicker></vue-timepicker>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'

export default {
  name: 'once',
  components: {
    Datepicker
  }
}
</script>

<style>
</style>
