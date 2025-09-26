import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Importar estilos de Quasar
import 'quasar/src/css/index.sass'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
import materialIcons from '@quasar/extras/material-icons/index.js'

const myApp = createApp(App)

myApp.use(Quasar, {
  plugins: {},
  iconSet: materialIcons // Quasar icon set
})

myApp.use(createPinia())
myApp.use(router)

myApp.mount('#app')
