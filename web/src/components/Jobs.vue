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
            <td>{{ job.attributes.name }}</td>
            <td>{{ job.attributes.from_host }}</td>
            <td>{{ job.attributes.from_path }}</td>
            <td>{{ job.attributes.to_host }}</td>
            <td>{{ job.attributes.to_path }}</td>
            <td class="has-text-right">
              <button class="button is-primary is-small" v-on:click="editJob(job.attributes.name)">
                <i class="fa fa-pencil" aria-hidden="true"></i>&nbsp;Edit
              </button>
              <button class="button is-danger is-small" v-on:click="deleteJob(job.attributes.name)">
                <i class="fa fa-trash" aria-hidden="true"></i>&nbsp;Delete
              </button>
              <button class="button is-success is-small" v-on:click="stateChange(job.attributes.name, 'start')">
                <i class="fa fa-play" aria-hidden="true"></i>&nbsp;Start
              </button>
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
import JobTransformers from '../mixins/transformers/job'

export default {
  name: 'jobs',
  data () {
    return {
      jobs: []
    }
  },
  mixins: [
    JobTransformers
  ],
  methods: {
    editJob: function (name) {
      this.$refs.job.editJob(name)
    },
    newJob: function () {
      this.$refs.job.newJob()
    },
    stateChange: function (name, state) {
      axios.patch(process.env.API_SERVER + '/jobs/' + name, this.changeStatusTransformer(name, state))
        .then((response) => {
          console.log('Job started')
        })
        .catch((error) => {
          console.log(error)
        })
    },
    deleteJob: function (name) {
      axios.delete(process.env.API_SERVER + '/jobs/' + name)
        .then((response) => {
          this.loadJobs()
        })
        .catch((error) => {
          console.log(error)
        })
    },
    loadJobs: function () {
      axios.get(process.env.API_SERVER + '/jobs')
        .then((response) => {
          this.jobs = response.data.data
        })
        .catch((error) => {
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
