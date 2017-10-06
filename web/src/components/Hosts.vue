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
            <th class="has-text-right">Action</th>
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
            <td class="has-text-right">
              <button class="button is-primary" v-on:click="editHost(item.host)"><i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit</button>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="7" class="has-text-right">
              <button class="button is-primary" v-on:click="newHost()"">Add a New Host</button>
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
    <host ref="host"></host>
  </section>
</template>

<script>
import axios from 'axios'
import Host from './Host'

export default {
  name: 'hosts',
  data () {
    return {
      items: []
    }
  },
  methods: {
    editHost: function (name) {
      // Trigger hosts modal popup
      this.$refs.host.editHost(name)
    },
    newHost: function () {
      this.$refs.host.newHost()
    }
  },
  components: {
    Host
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
