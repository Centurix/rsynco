<template>
  <div>
    <div class="modal" v-bind:class="{ 'is-active': shown, 'modal': true }">
      <div class="modal-background" v-on:click="hide"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Browse For a Folder</p>
          <button class="delete" aria-label="close" v-on:click="hide"></button>
        </header>
        <section class="modal-card-body">
          <div class="columns" v-show="loading">
            <div class="column has-text-centered">
              <pulse-loader></pulse-loader>
            </div>
          </div>
          <div v-show="!loading">
            <nav class="breadcrumb" aria-label="breadcrumbs">
              <ul>
                <li v-for="(part, index) in pathParts">
                  <a v-on:click="navigateToAbsolute(index)">{{ part }}</a>
                </li>
              </ul>
            </nav>
            <ul>
              <li v-show="pathParts.length > 1"><a v-on:click="navigateToParent">..</a></li>
              <li v-for="item in contents">
                <a v-show="item.attributes.type=='dir' && canShow(item.attributes.name)" v-on:click="navigateTo(item.attributes.name)">
                  <i class="fa fa-folder" aria-hidden="true"></i>
                  {{ item.attributes.name }}
                </a>
                <span v-show="item.attributes.type=='file' && canShow(item.attributes.name)">
                  <i class="fa fa-file" aria-hidden="true"></i>
                  {{ item.attributes.name }}
                </span>
                <span v-show="item.attributes.type=='link' && canShow(item.attributes.name)">
                  <i class="fa fa-link" aria-hidden="true"></i>
                  {{ item.attributes.name }}
                </span>
              </li>
            </ul>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-primary" v-on:click="select">Select</button>
          <button class="button is-danger" v-on:click="hide">Cancel</button>
          <div class="control">
            <div class="b-checkbox is-primary">
              <input type="checkbox" class="styled" id="hidden" v-model="showHidden">
              <label for="hidden">Show hidden files and folders</label>
            </div>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import EventBus from '../eventbus'
import PulseLoader from 'vue-spinner/src/PulseLoader.vue'

export default {
  name: 'browser',
  data () {
    return {
      loading: false,
      showHidden: false,
      tag: '',
      shown: false,
      host: '',
      initialPath: '',
      currentPath: '',
      pathParts: [],
      contents: []
    }
  },
  components: {
    PulseLoader
  },
  methods: {
    canShow: function (name) {
      return this.showHidden || (name.substr(0, 1) !== '.')
    },
    navigateTo: function (dir) {
      this.pathParts.push(dir)
      this.getContents()
    },
    navigateToParent: function () {
      this.pathParts.pop()
      this.getContents()
    },
    navigateToAbsolute: function (index) {
      this.pathParts = this.pathParts.slice(0, index + 1)
      this.getContents()
    },
    parsePath: function (path) {
      let paths = path.split('/')
      paths[0] = 'root'
      return paths
    },
    joinPath: function (pathParts) {
      let parts = pathParts.slice()
      parts.shift()
      return '/' + parts.join('/')
    },
    browse: function (tag, host, initialPath) {
      this.tag = tag
      this.host = host
      this.initialPath = initialPath
      this.pathParts = this.parsePath(initialPath)
      this.getContents()
      this.show()
    },
    getContents: function () {
      this.loading = true
      axios.get(process.env.API_SERVER + '/paths/' + encodeURIComponent(this.host) + '/' + encodeURIComponent(this.joinPath(this.pathParts)))
        .then((response) => {
          this.loading = false
          this.contents = response.data.data
          console.log(response)
        })
        .catch((error) => {
          this.loading = false
          console.log(error)
        })
    },
    select: function () {
      // Emit the select event
      EventBus.$emit('PATH_SELECTED', this.tag, this.joinPath(this.pathParts))
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
