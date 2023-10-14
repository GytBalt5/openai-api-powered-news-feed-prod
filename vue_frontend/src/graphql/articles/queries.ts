import gql from "graphql-tag";

const ARTICLE_FIELDS = `
    title
    slug
    content
    isPublished
    isFeatured
    createdAt
    categoryId
    userId
`;

export const ALL_ARTICLES = gql`
  query {
    allArticles {
        ${ARTICLE_FIELDS}
    }
}
`;

export const ARTICLES_BY_CATEGORY = gql`
  query ($category: String!) {
    articlesByCategory(category: $category) {
       ${ARTICLE_FIELDS}
    }
  }
`;

export const ARTICLE_BY_SLUG = gql`
  query ($slug: String!) {
    articleBySlug(slug: $slug) {
       ${ARTICLE_FIELDS}
    }
  }
`;
