import Vue from 'vue'
import Router from 'vue-router'
import Activity from '@/components/Activity'
import Hosts from '@/components/Hosts'
import Jobs from '@/components/Jobs'
import About from '@/components/About'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Activity',
      component: Activity
    }, {
      path: '/hosts',
      name: 'Hosts',
      component: Hosts
    }, {
      path: '/jobs',
      name: 'Jobs',
      component: Jobs
    }, {
      path: '/about',
      name: 'About',
      component: About
    }
  ]
})
