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
              <select class="input" v-model.number="startWeek" v-on:change="updated()">
                <option v-for="week in 104" v-bind:class="{current: (week === currentWeek)}" v-bind:value="week">{{ weekDescription(week) }}</option>
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
            <input type="number" class="input" min="1" max="52" value="1" v-model.number="weekFrequency" v-on:input="updated()">
          </div>
            <div class="control">
              <label class="button is-primary">Week(s)</label>
            </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <!-- Weekly -->
      <div class="field-label is-normal">
        <label class="label">On</label>
      </div>
      <div class="field-body">
        <ul>
          <li class="field" v-for="weekday in 7">
            <div class="control">
              <div class="b-checkbox is-primary">
                <input type="checkbox" class="styled"
                  v-bind:id="$moment.weekdays(weekday).toLowerCase()"
                  v-model="weekDays"
                  v-bind:value="$moment.weekdays(weekday).toLowerCase()"
                  v-on:click="updated()">
                <label v-bind:for="$moment.weekdays(weekday).toLowerCase()">{{ $moment.weekdays(weekday) }}</label>
              </div>
            </div>
          </li>
        </ul>
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
  name: 'week',
  props: [
    'week',
    'frequency',
    'days',
    'hour',
    'minute',
    'meridiem'
  ],
  watch: {
    week: function (newVal, oldVal) {
      this.startWeek = newVal
    },
    frequency: function (newVal, oldVal) {
      this.weekFrequency = newVal
    },
    days: function (newVal, oldVal) {
      this.weekDays = newVal
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
    this.startWeek = this.week
    this.weekFrequency = this.frequency
    this.weekDays = this.days
    this.startHour = this.hour
    this.startMinute = this.minute
    this.startMeridiem = this.meridiem
  },
  data () {
    return {
      currentWeek: this.$moment().week(),
      startWeek: this.$moment().week(),
      weekFrequency: 1,
      weekDays: [],
      startHour: 12,
      startMinute: 0,
      startMeridiem: 'AM'
    }
  },
  methods: {
    weekDescription: function (week) {
      let actualYearWeek = this.$moment().week(week)
      let start = actualYearWeek.startOf('week')
      return 'Week ' + actualYearWeek.week() + ' (' + start.format('MMMM Do, YYYY') + (this.currentWeek === week ? ', current' : '') + ')'
    },
    updated () {
      this.$emit('changedWeek', this.startWeek, this.weekFrequency, this.weekDays, this.startHour, this.startMinute, this.startMeridiem)
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
