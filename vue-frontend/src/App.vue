<template>
  <div class="container mx-auto max-w-3xl px-4 sm:px-6 xl:max-w-5xl xl:px-0">
    <div class="flex flex-col justify-between">
      <app-header :my-site="mySite" />
      <router-view />
      <app-footer />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { SITE_INFO } from "@/graphql/news-feed/queries";
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import { Site } from "@/interfaces/types";

export default defineComponent({
  components: {
    AppHeader,
    AppFooter,
  },
  data() {
    return {
      mySite: Object as Site | null,
      dataLoaded: false as boolean,
    };
  },
  async created() {
    try {
      const siteInfo = await this.$apollo.query({ query: SITE_INFO });
      this.mySite = siteInfo.data.site;
      this.dataLoaded = true;
    } catch (error) {
      console.error("An error occurred while fetching the site info:", error);
    }
  },
});
</script>
