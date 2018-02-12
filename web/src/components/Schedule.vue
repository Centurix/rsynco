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
              <select v-model="type">
                <option v-for="option in options" v-bind:value="option.value">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <day v-if="type === 'day'"></day>
    <hour v-if="type === 'hour'"></hour>
    <month v-if="type === 'month'"></month>
    <once v-if="type === 'once'"></once>
    <second v-if="type === 'second'"></second>
    <week v-if="type === 'week'"></week>
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
  components: {
    Day,
    Hour,
    Month,
    Once,
    Second,
    Week
  },
  data () {
    return {
      type: 'none',
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
