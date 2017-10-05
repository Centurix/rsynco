<template>
  <section class="section">
    <div>
      <h1 class="title">Hosts</h1>
      <table class="table is-striped is-fullwidth">
        <thead>
          <tr>
            <th>Name</th>
            <th>Hostname</th>
            <th>User</th>
            <th>Auth</th>
            <th>Progress</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items">
            <td>{{ item.name }}</td>
            <td>{{ item.host }}</td>
            <td>{{ item.user }}</td>
            <td>{{ item.auth }}</td>
            <td></td>
            <td>
              <button class="button is-primary">Stuff</button>
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
//        this.items = response.data.data
        this.items = [{
          'name': 'Host 1'
        }]
        console.log(response)
      }, (error) => {
        console.log(error)
      })
  }
}
</script>

<style>
</style>
