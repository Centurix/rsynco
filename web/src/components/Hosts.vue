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
            <th class="has-text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="host in hosts">
            <td>{{ host.host }}</td>
            <td>{{ host.hostname }}</td>
            <td>{{ host.port }}</td>
            <td>{{ host.username }}</td>
            <td>{{ host.password }}</td>
            <td class="has-text-right">
              <button class="button is-primary is-small" v-on:click="editHost(host.host)"><i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit</button>
              <button class="button is-danger is-small" v-on:click="deleteHost(host.host)"><i class="fa fa-trash" aria-hidden="true"></i>&nbsp;Delete</button>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="7" class="has-text-right">
              <button class="button is-primary is-small" v-on:click="newHost()"">Add a New Host</button>
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
import EventBus from '../eventbus'

export default {
  name: 'hosts',
  data () {
    return {
      hosts: []
    }
  },
  methods: {
    editHost: function (name) {
      // Trigger hosts modal popup
      this.$refs.host.editHost(name)
    },
    newHost: function () {
      this.$refs.host.newHost()
    },
    deleteHost: function (name) {
      axios.delete(process.env.API_SERVER + '/hosts/' + name)
        .then((response) => {
          this.loadHosts()
          console.log(response)
        }, (error) => {
          console.log(error)
        })
    },
    loadHosts: function () {
      axios.get(process.env.API_SERVER + '/hosts')
        .then((response) => {
          this.hosts = response.data.data
          console.log(response)
        }, (error) => {
          console.log(error)
        })
    }
  },
  components: {
    Host
  },
  mounted: function () {
    EventBus.$on('HOSTS_CHANGED', this.loadHosts)
    this.loadHosts()
  }
}
</script>

<style>
</style>
