<template>
  <footer class="flex flex-col place-items-center mt-5 py-5 border-t-2">
    <div class="mb-3 flex space-x-4">
      <i
        class="fa-brands fa-linkedin text-3xl text-gray-400 hover:text-teal-300"
      ></i>
      <i
        class="fa-brands fa-facebook-square text-3xl text-gray-400 hover:text-teal-300"
      ></i>
      <i
        class="fa-brands fa-twitter-square text-3xl text-gray-400 hover:text-teal-300"
      ></i>
      <i
        class="fa-brands fa-google-plus-square text-3xl text-gray-400 hover:text-teal-300"
      ></i>
      <i
        class="fa-brands fa-github-square text-3xl text-gray-400 hover:text-teal-300"
      ></i>
      <i
        class="fa-brands fa-dev text-3xl text-gray-400 hover:text-teal-300"
      ></i>
    </div>
    <div class="mb-3 flex space-x-1 text-sm text-gray-400">
      <div>•</div>
      <div>© 2023</div>
      <div>•</div>
      <a href="/" class="hover:underline hover:text-teal-300"
        >Vue.js Starter OpenAI Generated News Feed</a
      >
    </div>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "AppFooterComponent",
});
</script>
