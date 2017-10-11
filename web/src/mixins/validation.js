export default {
  data () {
    return {
      validationErrors: []
    }
  },
  methods: {
    clearValidationErrors: function () {
      this.validationErrors = []
    },
    isValid: function (field) {
      let validationError = this.validationErrors.find(function (obj) { return obj.path === 'data/attributes/' + field })
      return (typeof validationError === 'object')
    },
    processValidationErrors: function (error) {
      if (error.response.status === 400) {
        this.validationErrors = error.response.data.errors
      }
    }
  }
}
