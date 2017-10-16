<template>
  <section class="section">
    <div>
      <h1 class="title"><i class="fa fa-server" aria-hidden="true"></i>&nbsp;Hosts</h1>
      <p class="has-text-right">
        <label class="checkbox">
          <input type="checkbox" v-model="showSystemHosts">
          List System defined SSH hosts
        </label>
      </p>
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
          <tr v-for="host in hosts" v-show="host.attributes.type == 'rsynco' || showSystemHosts">
            <td>{{ host.attributes.host }}</td>
            <td>{{ host.attributes.hostname }}</td>
            <td>{{ host.attributes.port }}</td>
            <td>{{ host.attributes.username }}</td>
            <td>{{ host.attributes.password }}</td>
            <td class="has-text-right">
              <span v-show="host.attributes.type == 'system'">SSH Config Host (Non-edit)</span>
              <button v-show="host.attributes.type == 'rsynco'" class="button is-primary is-small" v-on:click="editHost(host.attributes.host)">
                <i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit
              </button>
              <button v-show="host.attributes.type == 'rsynco'" class="button is-danger is-small" v-on:click="deleteHost(host.attributes.host)">
                <i class="fa fa-trash" aria-hidden="true"></i>&nbsp;Delete
              </button>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="7" class="has-text-right">
              <button class="button is-primary is-small" v-on:click="newHost()""><i class="fa fa-plus" aria-hidden="true"></i>&nbsp;Add a New Host</button>
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
      hosts: [],
      showSystemHosts: false
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
        })
        .catch((error) => {
          console.log(error)
        })
    },
    loadHosts: function () {
      axios.get(process.env.API_SERVER + '/hosts')
        .then((response) => {
          this.hosts = response.data.data
        })
        .catch((error) => {
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
