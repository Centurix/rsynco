<template>
  <section class="section">
    <div>
      <h1 class="title">Current Activity</h1>
      <table class="table is-striped is-fullwidth">
        <thead>
          <tr>
            <th>Process ID</th>
            <th>Started</th>
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
            <td>{{ item.from }}</td>
            <td>{{ item.to }}</td>
            <td>
              <progress class="progress is-primary is-large" v-bind:value="item.progress" max="100">{{ item.progress }}%</progress>
            </td>
            <td>
              <button v-if="paused(item.status)" class="button is-primary" v-on:click="pause(item.pid)"><i class="fa fa-pause" aria-hidden="true"></i>&nbsp;Pause</button>
              <button v-if="!paused(item.status)" class="button is-primary" v-on:click="resume(item.pid)"><i class="fa fa-play" aria-hidden="true"></i>&nbsp;Resume</button>
              <button class="button is-danger" v-on:click="stop(item.pid)"><i class="fa fa-stop" aria-hidden="true"></i>&nbsp;Stop</button>
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
      items: []
    }
  },
  methods: {
    loadActivity: function () {
      axios.get(process.env.API_SERVER + '/activity')
        .then((response) => {
          this.items = response.data.data
          if (this.items.length > 0) {
            clearInterval(this.timer)
            this.timer = setInterval(function () {
              this.loadActivity()
            }.bind(this), 1000)
          } else {
            clearInterval(this.timer)
            this.timer = setInterval(function () {
              this.loadActivity()
            }.bind(this), 5000)
          }
          console.log(response)
        }, (error) => {
          console.log(error)
        })
    },
    pause: function (pid) {
      axios.post(process.env.API_SERVER + '/activity/' + pid + '/pause')
      console.log('Pausing a process: ' + pid)
    },
    resume: function (pid) {
      axios.post(process.env.API_SERVER + '/activity/' + pid + '/resume')
      console.log('Resume a process: ' + pid)
    },
    stop: function (pid) {
      axios.post(process.env.API_SERVER + '/activity/' + pid + '/stop')
      console.log('Stop a process: ' + pid)
    },
    paused: function (status) {
      return status === 'sleeping' || status === 'running'
    }
  },
  mounted: function () {
    this.loadActivity()
  },
  created: function () {
    this.timer = setInterval(function () {
      this.loadActivity()
    }.bind(this), 5000)
  },
  destroyed: function () {
    clearInterval(this.timer)
  }
}
</script>

<style>
</style>
