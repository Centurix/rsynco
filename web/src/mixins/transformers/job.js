export default {
  methods: {
    jobAttributes: function (job) {
      return {
        name: job.name,
        from_host: job.from_host,
        from_path: job.from_path,
        to_host: job.to_host,
        to_path: job.to_path
      }
    },
    newJobTransformer: function (job) {
      return {
        data: [{
          type: 'jobs',
          attributes: this.jobAttributes(job)
        }]
      }
    },
    editJobTransformer: function (job) {
      return {
        data: [{
          type: 'jobs',
          id: job.name,
          attributes: this.jobAttributes(job)
        }]
      }
    },
    changeStatusTransformer: function (job, status) {
      return {
        data: [{
          type: 'jobs',
          id: job,
          attributes: {
            'status': status
          }
        }]
      }
    }
  }
}
