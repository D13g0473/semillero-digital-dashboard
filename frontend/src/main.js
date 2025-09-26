import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Importar estilos de Quasar
import 'quasar/src/css/index.sass'

const myApp = createApp(App)

myApp.use(Quasar, {
  plugins: {},
})

myApp.use(createPinia())
myApp.use(router)

myApp.mount('#app')
