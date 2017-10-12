export default {
  methods: {
    changeStatusTransformer: function (pid, status) {
      return {
        data: [{
          type: 'activity',
          id: pid.toString(),
          attributes: {
            status: status
          }
        }]
      }
    }
  }
}
