<template>
  <div class="article-list">
    <ul class="divide-y divide-gray-200">
      <li class="py-12" v-for="article in articles" :key="article.title">
        <article>
          <div
            class="space-y-2 xl:grid xl:grid-cols-4 xl:items-baseline xl:space-y-0"
          >
            <dl>
              <dt class="sr-only">Published on</dt>
              <dd class="text-base font-medium leading-6">
                <time>{{ formatDate(article.createdAt) }}</time>
              </dd>
            </dl>
            <div class="space-y-5 xl:col-span-3">
              <div class="space-y-6">
                <div>
                  <h2 class="text-2xl font-bold leading-8 tracking-tight">
                    <router-link :to="`/article/${article.slug}`">{{
                      article.title
                    }}</router-link>
                  </h2>
                  <router-link
                    v-if="article.category"
                    class="text-sm font-medium uppercase text-teal-500 hover:underline hover:text-teal-700"
                    :to="`/category/${article.category.slug}`"
                    >{{ article.category.name }}</router-link
                  >
                </div>
                <div class="prose max-w-none">
                  {{ trimString(stripHTML(article.content)) }}
                </div>
              </div>
              <div class="text-base font-medium leading-6">
                <router-link
                  class="text-teal-500 hover:underline hover:text-teal-700"
                  :to="`/article/${article.slug}`"
                  >Read more →</router-link
                >
              </div>
            </div>
          </div>
        </article>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Article } from "@/interfaces/types";

export default defineComponent({
  name: "ArticleListComponent",
  props: {
    articles: {
      type: Array as () => Array<Article>,
      required: true,
    },
  },
  methods: {
    stripHTML(string: string): string {
      return string.replace(/<\/?[^>]+>/gi, " ");
    },
    trimString(string: string): string {
      return string.length > 350 ? `${string.substring(0, 350)}...` : string;
    },
    formatDate(x: string | number | Date): string {
      let date = new Date(x);
      const months = [
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
      ];
      return `${
        months[date.getMonth()]
      } ${date.getDate()}, ${date.getFullYear()}`;
    },
  },
});
</script>
