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
              <select class="input">
                <option v-for="week in 104" v-bind:class="{current: (week === currentWeek)}">{{ weekDescription(week) }}</option>
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
            <input type="number" class="input" minimum="1" value="1">
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
                <input type="checkbox" class="styled" v-bind:id="$moment.weekdays(weekday).toLowerCase()">
                <label v-bind:for="$moment.weekdays(weekday).toLowerCase()">{{ $moment.weekdays(weekday) }}</label>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'week',
  data () {
    return {
      currentWeek: this.$moment().week()
    }
  },
  methods: {
    weekDescription: function (week) {
      let actualYearWeek = this.$moment().week(week)
      let start = actualYearWeek.startOf('week')
      return 'Week ' + actualYearWeek.week() + ' (' + start.format('MMMM Do, YYYY') + (this.currentWeek === week ? ', current' : '') + ')'
    }
  }
}
</script>

<style>
option.current {
  font-weight: bold;
}
</style>
