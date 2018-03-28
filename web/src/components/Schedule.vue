<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Schedule</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="currentSchedule.type">
                <option v-for="option in options" v-bind:value="option.value" v-on:change="updated()">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <once v-if="currentSchedule.type === 'once'"
      v-on:changedOnce="changedOnce"
      v-bind:date="this.currentSchedule.date"
      v-bind:hour="this.currentSchedule.hour"
      v-bind:minute="this.currentSchedule.minute"
      v-bind:meridiem="this.currentSchedule.meridiem"></once>
    <day v-if="currentSchedule.type === 'day'"
      v-on:changedDay="changedDay"
      v-bind:hour="this.currentSchedule.hour"
      v-bind:minute="this.currentSchedule.minute"
      v-bind:meridiem="this.currentSchedule.meridiem"></day>
    <week v-if="currentSchedule.type === 'week'"
      v-on:changedWeek="changedWeek"
      v-bind:week="this.currentSchedule.week"
      v-bind:frequency="this.currentSchedule.weekFrequency"
      v-bind:days="this.currentSchedule.days"
      v-bind:hour="this.currentSchedule.hour"
      v-bind:minute="this.currentSchedule.minute"
      v-bind:meridiem="this.currentSchedule.meridiem"></week>
    <month v-if="currentSchedule.type === 'month'"
      v-on:changedMonth="changedMonth"
      v-bind:month="this.currentSchedule.month"
      v-bind:frequency="this.currentSchedule.monthFrequency"
      v-bind:day="this.currentSchedule.day"
      v-bind:hour="this.currentSchedule.hour"
      v-bind:minute="this.currentSchedule.minute"
      v-bind:meridiem="this.currentSchedule.meridiem"></month>
    <hour v-if="currentSchedule.type === 'hour'"
      v-on:changedMinute="changedMinute"
      v-bind:minute="this.currentSchedule.minute"></hour>
    <second v-if="currentSchedule.type === 'second'"
      v-on:changedSecond="changedSecond"
      v-bind:frequency="this.currentSchedule.secondFrequency"></second>
  </div>
</template>

<script>
import Day from './schedules/Day'
import Hour from './schedules/Hour'
import Month from './schedules/Month'
import Once from './schedules/Once'
import Second from './schedules/Second'
import Week from './schedules/Week'

export default {
  name: 'schedule',
  props: [
    'schedule'
  ],
  watch: {
    schedule: function (newVal, oldVal) {
      console.log('Schedule UPDATED')
      this.currentSchedule = newVal
    }
  },
  mounted () {
    this.currentSchedule = this.schedule
  },
  components: {
    Day,
    Hour,
    Month,
    Once,
    Second,
    Week
  },
  methods: {
    updated () {
      this.$emit('changedSchedule', this.currentSchedule)
    },
    changedDay (hour, minute, meridiem) {
      this.currentSchedule.hour = hour
      this.currentSchedule.minute = minute
      this.currentSchedule.meridiem = meridiem
      this.updated()
    },
    changedMinute (minute) {
      this.currentSchedule.minute = minute
      this.updated()
    },
    changedMonth (month, frequency, day, hour, minute, meridiem) {
      this.currentSchedule.month = month
      this.currentSchedule.monthFrequency = frequency
      this.currentSchedule.day = day
      this.currentSchedule.hour = hour
      this.currentSchedule.minute = minute
      this.currentSchedule.meridiem = meridiem
      this.updated()
    },
    changedOnce (date, hour, minute, meridiem) {
      this.currentSchedule.date = date
      this.currentSchedule.hour = hour
      this.currentSchedule.minute = minute
      this.currentSchedule.meridiem = meridiem
      this.updated()
    },
    changedSecond (secondFrequency) {
      this.currentSchedule.secondFrequency = secondFrequency
      this.updated()
    },
    changedWeek (week, frequency, days, hour, minute, meridiem) {
      this.currentSchedule.week = week
      this.currentSchedule.weekFrequency = frequency
      this.currentSchedule.days = days
      this.currentSchedule.hour = hour
      this.currentSchedule.minute = minute
      this.currentSchedule.meridiem = meridiem
      this.updated()
    }
  },
  data () {
    return {
      currentSchedule: {
        type: 'none',
        day: 1,
        days: [],
        date: this.$moment().format('YYYY-MM-DD'),
        hour: 12,
        minute: 0,
        second: 0,
        secondFrequency: 10,
        meridiem: 'AM',
        week: this.$moment().week(),
        weekFrequency: 1,
        month: 1,
        monthFrequency: 1
      },
      options: [
        { text: 'Not Scheduled', value: 'none' },
        { text: 'Once-off', value: 'once' },
        { text: 'Daily', value: 'day' },
        { text: 'Weekly', value: 'week' },
        { text: 'Monthly', value: 'month' },
        { text: 'Hourly', value: 'hour' },
        { text: 'Seconds', value: 'second' }
      ]
    }
  }
}
</script>

<style>
</style>
