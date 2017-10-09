<template>
  <section class="section">
    <div>
      <h1 class="title">Jobs</h1>
      <table class="table is-striped is-fullwidth">
        <thead>
          <tr>
            <th>Name</th>
            <th>From Host</th>
            <th>From Path</th>
            <th>To Host</th>
            <th>To Path</th>
            <th class="has-text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs">
            <td>{{ job.name }}</td>
            <td>{{ job.from_host }}</td>
            <td>{{ job.from_path }}</td>
            <td>{{ job.to_host }}</td>
            <td>{{ job.to_path }}</td>
            <td class="has-text-right">
              <button class="button is-primary is-small" v-on:click="editJob(job.name)"><i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit</button>
              <button class="button is-danger is-small" v-on:click="deleteJob(job.name)"><i class="fa fa-trash" aria-hidden="true"></i>&nbsp;Delete</button>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="7" class="has-text-right">
              <button class="button is-primary is-small" v-on:click="newJob()"">Add a New Job</button>
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
    <job ref="job"></job>
  </section>
</template>

<script>
import axios from 'axios'
import Job from './Job'
import EventBus from '../eventbus'

export default {
  name: 'jobs',
  data () {
    return {
      jobs: []
    }
  },
  methods: {
    editJob: function (name) {
      // Trigger hosts modal popup
      this.$refs.job.editJob(name)
    },
    newJob: function () {
      this.$refs.job.newJob()
    },
    deleteJob: function (name) {
      axios.delete(process.env.API_SERVER + '/jobs/' + name)
        .then((response) => {
          this.loadJobs()
          console.log(response)
        }, (error) => {
          console.log(error)
        })
    },
    loadJobs: function () {
      axios.get(process.env.API_SERVER + '/jobs')
        .then((response) => {
          this.jobs = response.data.data
          console.log(response)
        }, (error) => {
          console.log(error)
        })
    }
  },
  components: {
    Job
  },
  mounted: function () {
    EventBus.$on('JOBS_CHANGED', this.loadJobs)
    this.loadJobs()
  }
}
</script>

<style>
</style>
