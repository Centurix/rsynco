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
            <td>{{ item.pid }}</td>
            <td>{{ item.started }}</td>
            <td>{{ duration(item.started) }} Seconds</td>
            <td>{{ item.from }}</td>
            <td>{{ item.to }}</td>
            <td>
              <span v-if="item.progress == -1"><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp;Not monitored</span>
              <progress v-if="item.progress > -1" class="progress is-primary is-large" v-bind:value="item.progress" max="100">{{ item.progress }}%</progress>
            </td>
            <td>
              <button v-if="paused(item.status)" class="button is-primary is-small" v-on:click="pause(item.pid)"><i class="fa fa-pause" aria-hidden="true"></i>&nbsp;Pause</button>
              <button v-if="!paused(item.status)" class="button is-primary is-small" v-on:click="resume(item.pid)"><i class="fa fa-play" aria-hidden="true"></i>&nbsp;Resume</button>
              <button class="button is-danger is-small" v-on:click="stop(item.pid)"><i class="fa fa-stop" aria-hidden="true"></i>&nbsp;Stop</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'activity',
  data () {
    return {
      items: [],
      timer: null
    }
  },
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
    pause: function (pid) {
      axios.post(process.env.API_SERVER + '/activity/' + pid + '/pause', {})
    },
    resume: function (pid) {
      axios.post(process.env.API_SERVER + '/activity/' + pid + '/resume', {})
    },
    stop: function (pid) {
      axios.post(process.env.API_SERVER + '/activity/' + pid + '/stop', {})
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
