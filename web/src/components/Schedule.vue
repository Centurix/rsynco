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
              <select>
                <option value="">Not scheduled</option>
                <option value="once">One-off!</option>
                <option value="repeat">Repeat</option>
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
          <div class="control">
            <input type="number" class="input">
          </div>
          <div class="control">
            <span class="button is-primary">Test</span>
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <!-- Daily -->
      <div class="field-label is-normal">
        <label class="label">Starts</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <input type="text" class="input">
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <!-- Weekly -->
      <div class="field-label is-normal">
        <label class="label">Every</label>
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
    <div class="field is-horizontal">
      <!-- Monthly -->
      <div class="field-label is-normal">
        <label class="label">Run</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select>
                <option>Day of the Month</option>
                <option>Day of the Week</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <!-- Yearly -->
      <div class="field-label is-normal">
        <label class="label">Day of the year</label>&nbsp;
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <input type="text" class="input">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'schedule'
}
</script>

<style>
</style>
