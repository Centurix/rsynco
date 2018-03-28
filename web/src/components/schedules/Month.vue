<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Start</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model.number="startMonth" v-on:change="updated()">
                <option v-for="(monthName, monthIndex) in $moment.months()" v-bind:class="{current: (monthName.toLowerCase() === currentMonth)}" v-bind:value="monthIndex">{{ monthName }} <span v-if="monthName.toLowerCase() === currentMonth"> (current)</span></option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Every</label>
      </div>
      <div class="field-body">
        <div class="field has-addons">
          <div class="control is-expanded">
            <input type="number" class="input" min="1" max="31" v-model.number="monthFrequency" v-on:change="updated()">
          </div>
            <div class="control">
              <label class="button is-primary">Month(s)</label>
            </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">On</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model.number="startDay" v-on:change="updated()">
                <option v-for="dayIndex in 31" v-bind:value="$moment().month(0).date(dayIndex).format('D')">{{ $moment().month(0).date(dayIndex).format('Do') }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
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
export default {
  name: 'month',
  props: [
    'month',
    'frequency',
    'day',
    'hour',
    'minute',
    'meridiem'
  ],
  watch: {
    month: function (newVal, oldVal) {
      this.startMonth = newVal
    },
    frequency: function (newVal, oldVal) {
      this.monthFrequency = newVal
    },
    day: function (newVal, oldVal) {
      this.startDay = newVal
    },
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
    this.startMonth = this.month
    this.monthFrequency = this.frequency
    this.startDay = this.day
    this.startHour = this.hour
    this.startMinute = this.minute
    this.startMeridiem = this.meridiem
  },
  data () {
    return {
      startMonth: this.$moment().format('MMMM').toLowerCase(),
      monthFrequency: 1,
      startDay: 1,
      startHour: 1,
      startMinute: 0,
      startMeridiem: 'AM',
      currentMonth: this.$moment().format('MMMM').toLowerCase()
    }
  },
  methods: {
    updated () {
      this.$emit('changedMonth', this.startMonth, this.monthFrequency, this.startDay, this.startHour, this.startMinute, this.startMeridiem)
    }
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
option.current {
  font-weight: bold;
}
</style>
