import "./index.css";
import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import { apolloProvider } from "@/apollo-config";

createApp(App).use(store).use(router).use(apolloProvider).mount("#app");
