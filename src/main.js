import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import 'bootstrap'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// import AudioVisual from 'vue-audio-visual'


// import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

Vue.config.productionTip = false
// Vue.use(AudioVisual)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
