<template>
  <section class="section">
    <div>
      <h1 class="title">Hosts</h1>
      <table class="table is-striped is-fullwidth">
        <thead>
          <tr>
            <th>Name</th>
            <th>Hostname</th>
            <th>Port</th>
            <th>User</th>
            <th>Auth</th>
            <th>Progress</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td>{{ item.host }}</td>
            <td>{{ item.hostname }}</td>
            <td>{{ item.port }}</td>
            <td>{{ item.username }}</td>
            <td>{{ item.password }}</td>
            <td></td>
            <td>
              <button class="button is-primary"><i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit</button>
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
  name: 'hosts',
  data () {
    return {
      items: []
    }
  },
  mounted: function () {
    axios.get(process.env.API_SERVER + '/hosts')
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
