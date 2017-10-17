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
@import "~bulma/sass/utilities/initial-variables.sass"

$modal-content-width: 1000px

@import "~bulma/sass/utilities/functions.sass"
@import "~bulma/sass/utilities/derived-variables.sass"
@import "~bulma/sass/utilities/animations.sass"
@import "~bulma/sass/utilities/mixins.sass"
@import "~bulma/sass/utilities/controls.sass"

@import "~bulma/sass/base/_all"
@import "~bulma/sass/elements/_all"
@import "~bulma/sass/components/_all"
@import "~bulma/sass/grid/_all"
@import "~bulma/sass/layout/_all"

@import "~cool-checkboxes-for-bulma.io/dist/css/bulma-radio-checkbox.min.css"

@import "~bulma-badge/badge.sass"
@import "~font-awesome/css/font-awesome.css"
</style>
