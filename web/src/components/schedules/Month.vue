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
              <select>
                <option v-for="month in $moment.months()" v-bind:class="{current: (month === currentMonth)}"">{{ month }} <span v-if="month === currentMonth"> (current)</span></option>
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
              <select>
                <option v-for="day in 31">{{ $moment().month(0).date(day).format('Do') }}</option>
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
              <select>
                <option v-for="hour in 12">{{ hour | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select>
                <option>00</option>
                <option v-for="minute in 60">{{ minute | leftPad(2, '0') }}</option>
              </select>
            </div>
            <div class="select">
              <select>
                <option>AM</option>
                <option>PM</option>
              </select>
            </div>
          </div>
        </div>
        <div class="field">
          <div class="control">
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
      currentMonth: this.$moment().format('MMMM')
    }
  }
}
</script>

<style>
option.current {
  font-weight: bold;
}
</style>
