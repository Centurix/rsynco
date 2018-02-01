<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Time</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select">
              <select v-model="hour">
                <option v-for="hour in 12" v-bind:value="hour">{{ hour | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model="minute">
                <option value="0">00</option>
                <option v-for="minute in 60" v-bind:value="minute">{{ minute | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model="meridiem">
                <option value="am">AM</option>
                <option value="pm">PM</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Datetime } from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'

export default {
  name: 'day',
  data () {
    return {
      hour: 1,
      minute: 0,
      meridiem: 'am'
    }
  },
  components: {
    Datetime
  },
  filters: {
    leftPad: function (value) {
      if (value >= 10) {
        return value
      }
      return '0' + value
    }
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
