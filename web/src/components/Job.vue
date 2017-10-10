<template>
  <div>
    <div v-show="shown" class="modal" v-bind:class="{ 'is-active': shown, 'modal': true }">
      <div class="modal-background" v-on:click="hide"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Edit Job Detail</p>
          <button class="delete" aria-label="close" v-on:click="hide"></button>
        </header>
        <section class="modal-card-body">
          <div class="field">
            <label class="label">Name</label>
            <div class="control">
              <input class="input" type="text" placeholder="Name" v-model="job.name">
            </div>
          </div>
          <div class="field">
            <label class="label">From Host</label>
            <div class="control">
              <input class="input" type="text" placeholder="From Host" v-model="job.from_host">
            </div>
          </div>
          <div class="field">
            <label class="label">From Path</label>
            <div class="control">
              <input class="input" type="text" placeholder="From Path" v-model="job.from_path">
            </div>
          </div>
          <div class="field">
            <label class="label">To Host</label>
            <div class="control">
              <input class="input" type="text" placeholder="To Host" v-model="job.to_host">
            </div>
          </div>
          <div class="field">
            <label class="label">To Path</label>
            <div class="control">
              <input class="input" type="text" placeholder="To Path" v-model="job.to_path">
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
  name: 'job',
  data () {
    return {
      shown: false,
      editing: false,
      job: {
        name: '',
        from_host: '',
        from_path: '',
        to_host: '',
        to_path: ''
      }
    }
  },
  methods: {
    newJob: function () {
      // Add a new job
      this.editing = false
      this.job = {
        name: '',
        from_host: '',
        from_path: '',
        to_host: '',
        to_path: ''
      }
      this.show()
    },
    editJob: function (name) {
      // Edit the job by name
      this.editing = true
      axios.get(process.env.API_SERVER + '/jobs/' + name)
        .then((response) => {
          this.job = response.data.data
        }, (error) => {
          console.log(error)
        })
      this.show()
    },
    add: function () {
      // Add a new job
      axios.post(process.env.API_SERVER + '/jobs', {
        data: {
          type: 'jobs',
          attributes: this.job
        }
      })
        .then((response) => {
          console.log('Added!')
          this.hide()
          EventBus.$emit('JOBS_CHANGED')
        }, (error) => {
          // Failed validation etc.
          console.log(error)
        })
    },
    update: function () {
      // Save the host
      axios.put(process.env.API_SERVER + '/jobs/' + this.job.name, {
        data: {
          type: 'jobs',
          attributes: this.job
        }
      })
        .then((response) => {
          console.log('Updated!')
          this.hide()
          EventBus.$emit('JOBS_CHANGED')
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
