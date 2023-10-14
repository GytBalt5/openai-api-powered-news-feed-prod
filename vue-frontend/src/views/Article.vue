<template>
  <div v-if="articleBySlug" class="home">
    <div class="flex flex-col place-items-center border-b-2">
      <h1 class="text-center text-5xl font-extrabold mb-5">
        {{ articleBySlug.title }}
      </h1>
      <p class="text-gray-500 text-lg mb-2">
        {{ formatDate(articleBySlug.createdAt) }}
      </p>
    </div>
    <!-- Main content -->
    <div class="py-5 font-serif space-y-4">
      <div v-html="articleBySlug.content"></div>
    </div>
    <!-- Share -->
    <div
      class="flex flex-wrap py-4 space-x-8 justify-center items-center text-xl"
    >
      <div id="socialShareIcon" @click="toggleSocialSharePopover">
        <i class="fa-solid fa-share-nodes"></i>
      </div>
      <div id="socialShare">
        <div
          v-if="showSocialShare"
          class="flex space-x-2 drop-shadow-lg border-2 p-2"
        >
          <i
            class="fa-brands fa-linkedin text-3xl text-gray-700 hover:text-teal-700"
          ></i>
          <i
            class="fa-brands fa-facebook-square text-3xl text-gray-700 hover:text-teal-700"
          ></i>
          <i
            class="fa-brands fa-twitter-square text-3xl text-gray-700 hover:text-teal-700"
          ></i>
          <i
            class="fa-brands fa-google-plus-square text-3xl text-gray-700 hover:text-teal-700"
          ></i>
          <i
            class="fa-brands fa-github-square text-3xl text-gray-700 hover:text-teal-700"
          ></i>
          <i
            class="fa-brands fa-dev text-3xl text-gray-700 hover:text-teal-700"
          ></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ARTICLE_BY_SLUG } from "@/graphql/articles/queries";
import { Article } from "@/interfaces/types";

export default defineComponent({
  name: "ArticleView",
  data() {
    return {
      articleBySlug: null as Article | null,
      showSocialShare: false as boolean,
    };
  },
  async created() {
    try {
      const article = await this.$apollo.query({
        query: ARTICLE_BY_SLUG,
        variables: {
          slug: this.$route.params.slug,
        },
      });
      this.articleBySlug = article.data.articleBySlug;
    } catch (error) {
      console.error("An error occurred while fetching the article:", error);
    }
  },
  methods: {
    toggleSocialSharePopover() {
      this.showSocialShare = !this.showSocialShare;
    },
    formatDate(x: number | string | Date) {
      let date = new Date(x);
      var month = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ][date.getMonth()];
      return month + " " + date.getDate() + ", " + date.getFullYear();
    },
  },
});
</script>
