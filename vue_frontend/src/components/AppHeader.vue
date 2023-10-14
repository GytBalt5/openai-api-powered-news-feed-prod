<template>
  <header class="flex flex-row items-center justify-between py-10">
    <div class="nav-logo text-2xl font-bold">
      <router-link to="/" v-if="mySite">{{ mySite.name }}</router-link>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Site } from "@/interfaces/types";

export default defineComponent({
  name: "AppHeaderComponent",
  props: {
    mySite: {
      type: Object as PropType<Site | null>,
      required: true,
    },
  },
});
</script>
