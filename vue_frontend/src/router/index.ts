import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "news-feed",
    component: () =>
      import(/* webpackChunkName: "NewsFeed" */ "@/views/NewsFeed.vue"),
  },
  {
    path: "/article/:slug",
    name: "article",
    component: () =>
      import(/* webpackChunkName: "Article" */ "@/views/Article.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
