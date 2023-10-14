<template>
  <div class="home">
    <h1 class="text-5xl font-extrabold mb-2">Recent Articles</h1>
    <p class="text-gray-500 text-lg mb-5">
      A NewsFeed created with Django, Vue.js and TailwindCSS
    </p>
    <div class="py-8 border-b-2">
      <h1 class="text-5xl font-extrabold">All Categories</h1>
    </div>
    <div class="flex flex-wrap py-8">
      <router-link
        v-for="category in allCategories"
        :key="category.name"
        class="my-2 mr-5 text-sm font-medium uppercase text-teal-500 hover:underline hover:text-teal-700"
        to="#"
      >
        {{ category.name }}
      </router-link>
    </div>
    <article-list :articles="allArticles"></article-list>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Article, Category } from "@/interfaces/types";
import ArticleList from "@/components/ArticleList.vue";
import { ALL_ARTICLES } from "@/graphql/articles/queries";
import { ALL_CATEGORIES } from "@/graphql/news-feed/queries";

export default defineComponent({
  name: "NewsFeedView",
  components: { ArticleList },
  data() {
    return {
      allArticles: [] as Article[],
      allCategories: [] as Category[],
    };
  },
  async created() {
    const articles = await this.$apollo.query({ query: ALL_ARTICLES });
    this.allArticles = articles.data.allArticles;
    const categories = await this.$apollo.query({ query: ALL_CATEGORIES });
    this.allCategories = categories.data.allCategories;
  },
});
</script>
