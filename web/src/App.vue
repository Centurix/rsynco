<template>
  <div id="app">
    <navbar></navbar>
    <router-view></router-view>
  </div>
</template>

<script>
import Navbar from './components/Navbar'
import Activity from './components/Activity'

export default {
  name: 'app',
  components: {
    Navbar,
    Activity
  }
}
</script>

<style lang="sass">
@import "~bulma"
@import "~bulma-badge/badge.sass"
@import "~font-awesome/css/font-awesome.css"
</style>
