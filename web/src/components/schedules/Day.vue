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
              <select v-model.number="startHour" v-on:change="updated()">
                <option v-for="hourIndex in 12" v-bind:value="hourIndex">{{ hourIndex | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model.number="startMinute" v-on:change="updated()">
                <option value="0">00</option>
                <option v-for="minuteIndex in 59" v-bind:value="minuteIndex">{{ minuteIndex | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model="startMeridiem" v-on:change="updated()">
                <option>AM</option>
                <option>PM</option>
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
  props: [
    'hour',
    'minute',
    'meridiem'
  ],
  watch: {
    hour: function (newVal, oldVal) {
      this.startHour = newVal
    },
    minute: function (newVal, oldVal) {
      this.startMinute = newVal
    },
    meridiem: function (newVal, oldVal) {
      this.startMeridiem = newVal
    }
  },
  created () {
    this.startHour = this.hour
    this.startMinute = this.minute
    this.startMeridiem = this.meridiem
  },
  methods: {
    updated () {
      this.$emit('changedDay', this.startHour, this.startMinute, this.startMeridiem)
    }
  },
  data () {
    return {
      startHour: 12,
      startMinute: 0,
      startMeridiem: 'AM'
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
