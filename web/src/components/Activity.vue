<template>
  <section class="section">
    <div>
      <h1 class="title">Current Activity</h1>
      <table class="table is-striped is-fullwidth">
        <thead>
          <tr>
            <th>Process ID</th>
            <th>Started</th>
            <th>Duration</th>
            <th>From</th>
            <th>To</th>
            <th>Progress</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td>{{ item.attributes.pid }}</td>
            <td>{{ item.attributes.started }}</td>
            <td>{{ duration(item.attributes.started) }} Seconds</td>
            <td>{{ item.attributes.from }}</td>
            <td>{{ item.attributes.to }}</td>
            <td>
              <span v-if="item.attributes.progress == -1">
                <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp;Not monitored
              </span>
              <progress v-if="item.attributes.progress > -1" class="progress is-primary is-large" v-bind:value="item.attributes.progress" max="100">{{ item.attributes.progress }}%</progress>
            </td>
            <td>
              <button v-if="paused(item.attributes.status)" class="button is-primary is-small" v-on:click="stateChange(item.attributes.pid, 'pause')"><i class="fa fa-pause" aria-hidden="true"></i>&nbsp;Pause</button>
              <button v-if="!paused(item.attributes.status)" class="button is-primary is-small" v-on:click="stateChange(item.attributes.pid, 'resume')"><i class="fa fa-play" aria-hidden="true"></i>&nbsp;Resume</button>
              <button v-if="paused(item.attributes.status)" class="button is-danger is-small" v-on:click="stateChange(item.attributes.pid, 'stop')"><i class="fa fa-stop" aria-hidden="true"></i>&nbsp;Stop</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import ActivityTransformers from '../mixins/transformers/activity'

export default {
  name: 'activity',
  data () {
    return {
      items: [],
      timer: null
    }
  },
  mixins: [ActivityTransformers],
  methods: {
    loadActivity: function () {
      axios.get(process.env.API_SERVER + '/activity')
        .then((response) => {
          this.items = response.data.data
          if (this.items.length > 0) {
            this.setRefresh(1000)
            return
          }
          this.setRefresh(5000)
        }, (error) => {
          console.log(error)
        })
    },
    stateChange: function (pid, state) {
      axios.patch(process.env.API_SERVER + '/activity/' + pid, this.changeStatusTransformer(pid, state))
    },
    paused: function (status) {
      return status === 'sleeping' || status === 'running'
    },
    duration: function (started) {
      return this.$moment().diff(this.$moment(started), 'seconds')
    },
    setRefresh: function (milliseconds) {
      if (this.timer) {
        clearTimeout(this.timer)
      }
      this.timer = setTimeout(function () {
        this.loadActivity()
      }.bind(this), milliseconds)
    }
  },
  mounted: function () {
    this.loadActivity()
  },
  created: function () {
    this.setRefresh(5000)
  },
  destroyed: function () {
    clearInterval(this.timer)
  }
}
</script>

<style>
</style>
