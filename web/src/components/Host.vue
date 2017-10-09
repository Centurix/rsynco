<template>
  <div>
    <div v-show="shown" class="modal" v-bind:class="{ 'is-active': shown, 'modal': true }">
      <div class="modal-background" v-on:click="hide"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Edit Host Detail</p>
          <button class="delete" aria-label="close" v-on:click="hide"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Name</label>
            <div class="control">
              <input class="input" type="text" placeholder="Name" v-model="host.host">
            </div>
          </div>
          <div class="field">
            <label class="label">Hostname</label>
            <div class="control">
              <input class="input" type="text" placeholder="Hostname" v-model="host.hostname">
            </div>
          </div>
          <div class="field">
            <label class="label">Port</label>
            <div class="control">
              <input class="input" type="text" placeholder="Port" v-model="host.port">
            </div>
          </div>
          <div class="field">
            <label class="label">User name</label>
            <div class="control">
              <input class="input" type="text" placeholder="User name" v-model="host.username">
            </div>
          </div>
          <div class="field">
            <label class="label">Password</label>
            <div class="control">
              <input class="input" type="text" placeholder="Password" v-model="host.password">
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button v-if="!editing" class="button is-primary" v-on:click="add">Add</button>
          <button v-if="editing" class="button is-primary" v-on:click="update">Update</button>
          <button class="button is-danger" v-on:click="hide">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import EventBus from '../eventbus'

export default {
  name: 'host',
  data () {
    return {
      shown: false,
      editing: false,
      host: {
        host: '',
        hostname: '',
        port: '',
        username: '',
        password: ''
      }
    }
  },
  methods: {
    newHost: function () {
      // Add a new host
      this.editing = false
      this.host = {
        host: '',
        hostname: '',
        port: '',
        username: '',
        password: ''
      }
      this.show()
    },
    editHost: function (name) {
      // Edit the host by name
      this.editing = true
      axios.get(process.env.API_SERVER + '/hosts/' + name)
        .then((response) => {
          this.host = response.data.data
        }, (error) => {
          console.log(error)
        })
      this.show()
    },
    add: function () {
      // Add a new host
      axios.post(process.env.API_SERVER + '/hosts', this.host)
        .then((response) => {
          console.log('Added!')
          this.hide()
          EventBus.$emit('HOSTS_CHANGED')
        }, (error) => {
          // Failed validation etc.
          console.log(error)
        })
    },
    update: function () {
      // Save the host
      axios.put(process.env.API_SERVER + '/hosts/' + this.host.host, this.host)
        .then((response) => {
          console.log('Updated!')
          this.hide()
          EventBus.$emit('HOSTS_CHANGED')
        }, (error) => {
          // Failed validation etc.
          console.log(error)
        })
    },
    cancel: function () {
      this.hide()
    },
    show: function () {
      this.shown = true
    },
    hide: function () {
      this.shown = false
    }
  }
}
</script>

<style>
</style>
