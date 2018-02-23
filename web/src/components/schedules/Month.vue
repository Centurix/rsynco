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
              <select v-model="month">
                <option v-for="month in $moment.months()" v-bind:class="{current: (month.toLowerCase() === currentMonth)}" v-bind:value="month.toLowerCase()">{{ month }} <span v-if="month.toLowerCase() === currentMonth"> (current)</span></option>
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
            <input type="number" class="input" min="1" v-model="monthFrequency">
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
              <select v-model="day">
                <option v-for="day in 31" v-bind:value="$moment().month(0).date(day).format('D')">{{ $moment().month(0).date(day).format('Do') }}</option>
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
              <select v-model="hour">
                <option v-for="hour in 12">{{ hour | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model="minute">
                <option>0</option>
                <option v-for="minute in 60">{{ minute | leftPad(2, '0') }}</option>
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
export default {
  name: 'month',
  data () {
    return {
      month: this.$moment().format('MMMM').toLowerCase(),
      monthFrequency: 1,
      day: 1,
      hour: 1,
      minute: 0,
      meridiem: 'am',
      currentMonth: this.$moment().format('MMMM').toLowerCase()
    }
  }
}
</script>

<style>
option.current {
  font-weight: bold;
}
</style>
