import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'

// PrimeVue CSS
import 'primevue/resources/themes/lara-dark-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

// PrimeVue Components
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import Checkbox from 'primevue/checkbox'
import Image from 'primevue/image'
import ProgressSpinner from 'primevue/progressspinner'
import Toast from 'primevue/toast'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'

// Global styles
import './assets/styles/main.scss'

const app = createApp(App)

app.use(PrimeVue, { ripple: true })
app.use(ToastService)

// Register PrimeVue components
app.component('p-button', Button)
app.component('p-inputNumber', InputNumber)
app.component('p-inputText', InputText)
app.component('p-dropdown', Dropdown)
app.component('p-slider', Slider)
app.component('p-checkbox', Checkbox)
app.component('p-image', Image)
app.component('p-progressSpinner', ProgressSpinner)
app.component('p-toast', Toast)
app.component('p-tabView', TabView)
app.component('p-tabPanel', TabPanel)

app.mount('#app')

