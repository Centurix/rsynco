<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Start</label>
      </div>
      <div class="field-body">
        <div class="field">
          <datetime input-class="input"></datetime>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Time</label>
      </div>
      <div class="field-body">
        <div class="field">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Datetime } from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'

export default {
  name: 'once',
  components: {
    datetime: Datetime
  }
}
</script>

<style>
.vdatetime-popup__header {
  background: #ffdd57;
  color: rgba(0, 0, 0, 0.7);
}
.vdatetime-calendar__month__day--selected > span > span,
.vdatetime-calendar__month__day--selected:hover > span > span{
  background: #ffdd57;
  color: rgba(0, 0, 0, 0.7);
}
.vdatetime-popup__actions__button {
  color: rgba(0, 0, 0, 0.7);
}
</style>
