import './assets/main.css'

import { createApp } from 'vue'
import { createStore} from "vuex";
import App from './App.vue'
import "@material/web/progress/linear-progress.js"
import "@material/web/list/list.js"
import "@material/web/list/list-item.js"
import "@material/web/divider/divider.js"


const app = createApp(App)
export const store = createStore({
    state () {
        return {
            index: 1
        }
    },
    mutations: {
        setindex(state, indexvalue) {
            state.index = indexvalue
        },
    }
})
app.use(store)
app.mount('#app')