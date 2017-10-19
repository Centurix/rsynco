<template>
  <div>
    <div class="modal" v-bind:class="{ 'is-active': shown, 'modal': true }">
      <div class="modal-background" v-on:click="hide"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p v-show="editing" class="modal-card-title">Edit Job Detail</p>
          <p v-show="!editing" class="modal-card-title">Add Job Detail</p>
          <button class="delete" aria-label="close" v-on:click="hide"></button>
        </header>
        <section class="modal-card-body">
          <div class="columns">
            <div class="column">
              <div class="field is-horizontal">
                <div class="field-label is-normal">
                  <label class="label">Name</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="control has-icons-right">
                      <input v-bind:class="{'input': true, 'is-danger': isValid('name')}" type="text" placeholder="Name" v-model="job.name" :disabled="editing">
                      <span v-show="isValid('name')" class="icon is-small is-right">
                        <i class="fa fa-warning"></i>
                      </span>
                    </div>
                    <p v-show="!isValid('name') && !editing" class="help">A name for this job is required</p>
                    <p v-show="isValid('name') && !editing" class="help is-danger">Invalid job name</p>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal">
                <div class="field-label is-normal">
                  <label class="label">From Host</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="field has-addons">
                      <div class="control is-expanded">
                        <div class="select" v-bind:class="{'select': true, 'is-fullwidth': true, 'is-danger': isValid('from_host')}" >
                          <select v-model="job.from_host">
                            <option disabled value="">Select a host</option>
                            <option value="localhost">localhost</option>
                            <option v-for="host in hosts">{{ host.attributes.host }}</option>
                          </select>
                        </div>
                      </div>
                      <div class="control">
                        <button class="button is-primary" v-on:click="newHost('from')">New</button>
                      </div>
                    </div>
                    <p v-show="!isValid('from_host')" class="help">A host for this job is required</p>
                    <p v-show="isValid('from_host')" class="help is-danger">Invalid host</p>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal">
                <div class="field-label is-normal">
                  <label class="label">From Path</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="field has-addons">
                      <div class="control has-icons-right is-expanded">
                        <input v-bind:class="{'input': true, 'is-danger': isValid('from_path')}" type="text" placeholder="From Path" v-model="job.from_path">
                        <span v-show="isValid('from_path')" class="icon is-small is-right">
                          <i class="fa fa-warning"></i>
                        </span>
                      </div>
                      <div class="control">
                        <button class="button is-primary" v-on:click="browsePath('from_path')"><i class="fa fa-folder-open" aria-hidden="true"></i></button>
                      </div>
                    </div>
                    <p v-show="!isValid('from_path')" class="help">A path for this job is required</p>
                    <p v-show="isValid('from_path')" class="help is-danger">Invalid path</p>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal">
                <div class="field-label is-normal">
                  <label class="label">To Host</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="field has-addons">
                      <div class="control is-expanded">
                        <div class="select" v-bind:class="{'select': true, 'is-fullwidth': true, 'is-danger': isValid('to_host')}" >
                          <select v-model="job.to_host">
                            <option disabled value="">Select a host</option>
                            <option value="localhost">localhost</option>
                            <option v-for="host in hosts">{{ host.attributes.host }}</option>
                          </select>
                        </div>
                      </div>
                      <div class="control">
                        <button class="button is-primary" v-on:click="newHost('to')">New</button>
                      </div>
                    </div>
                    <p v-show="!isValid('to_host')" class="help">A host for this job is required</p>
                    <p v-show="isValid('to_host')" class="help is-danger">Invalid host</p>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal">
                <div class="field-label is-normal">
                  <label class="label">To Path</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="field has-addons">
                      <div class="control has-icons-right is-expanded">
                        <input v-bind:class="{'input': true, 'is-danger': isValid('to_path')}" type="text" placeholder="To Path" v-model="job.to_path">
                        <span v-show="isValid('to_path')" class="icon is-small is-right">
                          <i class="fa fa-warning"></i>
                        </span>
                      </div>
                      <div class="control">
                        <button class="button is-primary" v-on:click="browsePath('to_path')"><i class="fa fa-folder-open" aria-hidden="true"></i></button>
                      </div>
                    </div>
                    <p v-show="!isValid('to_path')" class="help">A path for this job is required</p>
                    <p v-show="isValid('to_path')" class="help is-danger">Invalid path</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="column">
              <div class="field is-horizontal">
                <div class="field-label is-normal">
                  <label class="label">Repeat</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="control">
                      <div class="select is-fullwidth">
                        <select v-model="job.repeat">
                          <option value="">Not scheduled</option>
                          <option value="seconds">Second</option>
                          <option value="minutes">Minute</option>
                          <option value="hours">Hour</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal" v-show="job.repeat != ''">
                <div class="field-label is-normal">
                  <label class="label">Every</label>
                </div>
                <div class="field-body">
                  <div class="field has-addons">
                    <div class="control">
                      <input type="number" class="input" v-model.number="job.repeat_every">
                    </div>
                    <div class="control">
                      <span class="button is-primary">{{ job.repeat }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal" v-show="job.repeat == 'days'">
                <!-- Daily -->
                <div class="field-label is-normal">
                  <label class="label">Starts</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="control">
                      <input type="text" class="input">
                    </div>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal" v-show="job.repeat != 'weeks'">
                <!-- Weekly -->
                <div class="field-label is-normal">
                  <label class="label">Every</label>
                </div>
                <div class="field-body">
                  <ul>
                    <li class="field" v-for="weekday in 7">
                      <div class="control">
                        <div class="b-checkbox is-primary">
                          <input type="checkbox" class="styled" v-bind:id="$moment.weekdays(weekday).toLowerCase()">
                          <label v-bind:for="$moment.weekdays(weekday).toLowerCase()">{{ $moment.weekdays(weekday) }}</label>
                        </div>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="field is-horizontal" v-show="job.repeat == 'months'">
                <!-- Monthly -->
                <div class="field-label is-normal">
                  <label class="label">Run</label>
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="control">
                      <div class="select is-fullwidth">
                        <select>
                          <option>Day of the Month</option>
                          <option>Day of the Week</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="field is-horizontal" v-show="job.repeat == 'years'">
                <!-- Yearly -->
                <div class="field-label is-normal">
                  <label class="label">Day of the year</label>&nbsp;
                </div>
                <div class="field-body">
                  <div class="field">
                    <div class="control">
                      <input type="text" class="input">
                    </div>
                  </div>
                </div>
              </div>
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
    <host ref="host"></host>
    <browser ref="browser"></browser>
  </div>
</template>

<script>
import axios from 'axios'
import Host from './Host'
import Browser from './Browser'
import EventBus from '../eventbus'
import Validation from '../mixins/validation'
import JobTransformers from '../mixins/transformers/job'

export default {
  name: 'job',
  data () {
    return {
      shown: false,
      editing: false,
      job: this.emptyJob(),
      hosts: []
    }
  },
  mixins: [
    Validation,
    JobTransformers
  ],
  mounted: function () {
    EventBus.$on('HOSTS_CHANGED', this.loadHosts)
    EventBus.$on('PATH_SELECTED', this.pathSelected)
    this.loadHosts()
  },
  components: {
    Host,
    Browser
  },
  methods: {
    pathSelected: function (tag, path) {
      if (tag === 'from_path') {
        this.job.from_path = path
      } else if (tag === 'to_path') {
        this.job.to_path = path
      }
    },
    browsePath: function (tag) {
      this.$refs.browser.browse(tag, this.job.from_host, this.job.from_path)
    },
    newHost: function (tag) {
      // Show the new host modal
      // Update the from and to host selects if a host was added
      this.$refs.host.newHost(tag)
    },
    loadHosts: function (tag, host) {
      axios.get(process.env.API_SERVER + '/hosts')
        .then((response) => {
          this.hosts = response.data.data
          if (tag === 'from') {
            this.job.from_host = host
          } else if (tag === 'to') {
            this.job.to_host = host
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },
    emptyJob: function () {
      return {
        name: '',
        from_host: '',
        from_path: '',
        to_host: '',
        to_path: '',
        repeat: '',
        repeat_every: 1
      }
    },
    newJob: function () {
      this.editing = false
      this.job = this.emptyJob()
      this.show()
    },
    editJob: function (name) {
      this.editing = true
      axios.get(process.env.API_SERVER + '/jobs/' + name)
        .then((response) => {
          this.job = response.data.data[0].attributes
        })
        .catch((error) => {
          console.log(error)
        })
      this.show()
    },
    add: function () {
      axios.post(process.env.API_SERVER + '/jobs', this.newJobTransformer(this.job))
        .then((response) => {
          this.hide()
          EventBus.$emit('JOBS_CHANGED')
        })
        .catch((error) => {
          this.processValidationErrors(error)
        })
    },
    update: function () {
      axios.put(process.env.API_SERVER + '/jobs/' + this.job.name, this.editJobTransformer(this.job))
        .then((response) => {
          this.hide()
          EventBus.$emit('JOBS_CHANGED')
        })
        .catch((error) => {
          this.processValidationErrors(error)
        })
    },
    show: function () {
      this.shown = true
      this.clearValidationErrors()
    },
    hide: function () {
      this.shown = false
    }
  }
}
</script>

<style>
</style>
