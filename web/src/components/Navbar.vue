<template>
  <nav class="navbar is-warning" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a href="/" class="navbar-item">
        <img src="/static/rsynco_brand.png">
      </a>
      <button class="button navbar-burger">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start">
        <router-link :to="{name: 'Activity'}" class="navbar-item badge is-badge-small is-badge-warning is-badge-bottom" data-badge="1">Activity</router-link>
        <router-link :to="{name: 'Hosts'}" class="navbar-item badge is-badge-small is-badge-warning is-badge-bottom" data-badge="2">Hosts</router-link>
        <router-link :to="{name: 'Jobs'}" class="navbar-item badge is-badge-small is-badge-warning is-badge-bottom" data-badge="3">Jobs</router-link>
        <router-link :to="{name: 'About'}" class="navbar-item">About</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'navbar'
}
</script>

<style lang="sass">
.is-badge-bottom::after
      top: calc(50% - ( 1.75rem / 2 )) !important
      left: calc(100% - (1.75rem / 2)) !important
</style>
