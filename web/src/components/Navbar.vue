<template>
  <nav class="navbar is-warning" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a href="/" class="navbar-item">
        <img src="/static/rsynco_brand.png">
      </a>
      <button class="button navbar-burger" v-bind:class="{ 'is-active': isActive }" v-on:click="isActive = !isActive">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
    <div class="navbar-menu" ref="burgerMenu" v-bind:class="{ 'is-active': isActive }">
      <div class="navbar-start">
        <router-link :to="{name: 'Activity'}" class="navbar-item">Activity</router-link>
        <router-link :to="{name: 'Hosts'}" class="navbar-item">Hosts</router-link>
        <router-link :to="{name: 'Jobs'}" class="navbar-item">Jobs</router-link>
        <router-link :to="{name: 'About'}" class="navbar-item">About</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'navbar',
  data () {
    return {
      isActive: false
    }
  }
}
</script>

<style lang="sass">
.is-badge-bottom::after
      top: calc(50% - ( 1.75rem / 2 )) !important
      left: calc(100% - (1.75rem / 2)) !important
</style>
