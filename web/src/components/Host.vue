<template>
  <div>
    <div class="modal" v-bind:class="{ 'is-active': shown, 'modal': true }">
      <div class="modal-background" v-on:click="hide"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p v-show="editing" class="modal-card-title">Edit Host Detail</p>
          <p v-show="!editing" class="modal-card-title">New Host Detail</p>
          <button class="delete" aria-label="close" v-on:click="hide"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Name</label>
            <div class="control has-icons-right">
              <input v-bind:class="{'is-danger': isValid('host'), 'input': true}" type="text" placeholder="Name" v-model="host.host" :disabled="editing">
              <span v-show="isValid('host')" class="icon is-small is-right">
                <i class="fa fa-warning"></i>
              </span>
            </div>
            <p v-show="!isValid('host') && !editing" class="help">A name for this host is required</p>
            <p v-show="isValid('host') && !editing" class="help is-danger">Invalid host name</p>
          </div>
          <div class="field">
            <label class="label">Hostname</label>
            <div class="control has-icons-right">
              <input v-bind:class="{'is-danger': isValid('hostname'), 'input': true}" type="text" placeholder="Hostname" v-model="host.hostname">
              <span v-show="isValid('hostname')" class="icon is-small is-right">
                <i class="fa fa-warning"></i>
              </span>
            </div>
            <p v-show="!isValid('hostname')" class="help">A host is required</p>
            <p v-show="isValid('hostname')" class="help is-danger">Invalid host</p>
          </div>
          <div class="field">
            <label class="label">Port</label>
            <div class="control">
              <input v-bind:class="{'input': true, 'is-danger': isValid('port')}" type="number" placeholder="Port" v-model.number="host.port">
            </div>
            <p v-show="!isValid('port')" class="help">A port number between 1 and 65535 must be selected</p>
            <p v-show="isValid('port')" class="help is-danger">Invalid port number</p>
          </div>
          <div class="field">
            <label class="label">User name</label>
            <div class="control has-icons-right">
              <input v-bind:class="{'input': true, 'is-danger': isValid('username')}" type="text" placeholder="User name" v-model="host.username">
              <span v-show="isValid('username')" class="icon is-small is-right">
                <i class="fa fa-warning"></i>
              </span>
            </div>
            <p v-show="!isValid('username')" class="help">A username is required</p>
            <p v-show="isValid('username')" class="help is-danger">Invalid username</p>
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
import Validation from '../mixins/validation'
import HostTransformers from '../mixins/transformers/host'

export default {
  name: 'host',
  data () {
    return {
      shown: false,
      editing: false,
      host: this.emptyHost()
    }
  },
  mixins: [
    Validation,
    HostTransformers
  ],
  methods: {
    emptyHost: function () {
      return {
        host: '',
        hostname: '',
        port: 22,
        username: '',
        password: ''
      }
    },
    newHost: function () {
      this.editing = false
      this.host = this.emptyHost()
      this.show()
    },
    editHost: function (name) {
      this.editing = true
      axios.get(process.env.API_SERVER + '/hosts/' + name)
        .then((response) => {
          this.host = response.data.data[0].attributes
          this.show()
        })
        .catch((error) => {
          console.log(error)
        })
    },
    add: function () {
      axios.post(process.env.API_SERVER + '/hosts', this.newHostTransformer(this.host))
        .then((response) => {
          this.hide()
          EventBus.$emit('HOSTS_CHANGED')
        })
        .catch((error) => {
          this.processValidationErrors(error)
        })
    },
    update: function () {
      axios.put(process.env.API_SERVER + '/hosts/' + this.host.host, this.editHostTransformer(this.host))
        .then((response) => {
          this.hide()
          EventBus.$emit('HOSTS_CHANGED')
        })
        .catch((error) => {
          this.processValidationErrors(error)
        })
    },
    show: function () {
      this.clearValidationErrors()
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
