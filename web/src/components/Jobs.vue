<template>
  <section class="section">
    <div>
      <h1 class="title">Jobs</h1>
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
              <button class="button is-primary">Pause</button>
              <button class="button is-danger">Stop</button>
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
  name: 'jobs',
  data () {
    return {
      items: []
    }
  },
  mounted: function () {
    axios.get('http://localhost:8888/api/activity')
      .then((response) => {
        this.items = response.data.data
        console.log(response)
      }, (error) => {
        console.log(error)
      })
  }
}
</script>

<style>
</style>
