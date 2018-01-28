<template>
  <div>
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
  </div>
</template>

<script>
export default {
  name: 'week'
}
</script>

<style>
</style>
