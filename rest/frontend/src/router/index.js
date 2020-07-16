import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ListPuntajes from '@/components/puntajes/ListPuntajes'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/puntajes',
      name: 'ListPuntajes',
      component: ListPuntajes
    }
  ],
  mode: 'history'
})
