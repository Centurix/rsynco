import Vue from 'vue'
import Router from 'vue-router'
import Activity from '@/components/Activity'
import Hosts from '@/components/Hosts'
import Jobs from '@/components/Jobs'

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
    }
  ]
})
