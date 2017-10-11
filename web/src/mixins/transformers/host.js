export default {
  methods: {
    hostAttributes: function (host) {
      return {
        host: host.host,
        hostname: host.hostname,
        port: host.port,
        username: host.username,
        password: host.password
      }
    },
    newHostTransformer: function (host) {
      return {
        data: [{
          type: 'hosts',
          attributes: this.hostAttributes(host)
        }]
      }
    },
    editHostTransformer: function (host) {
      return {
        data: [{
          type: 'hosts',
          id: host.host,
          attributes: this.hostAttributes(host)
        }]
      }
    }
  }
}
