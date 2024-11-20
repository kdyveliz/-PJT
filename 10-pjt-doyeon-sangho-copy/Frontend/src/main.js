import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

createApp(App).use(router).mount('#app')


fetch("http://127.0.0.1:8000/api/kakao-map-key/")
  .then((response) => response.json())
  .then((data) => {
    const script = document.createElement("script");
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${data.api_key}&libraries=services`;
    script.async = true;
    document.head.appendChild(script);
  });

