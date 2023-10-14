import gql from "graphql-tag";

export const CREATE_ARTICLE = gql`
  mutation (
    $userID: ID!
    $categoryID: ID!
    $title: String!
    $content: String!
    $isPublished: Boolean!
    $isFeatured: Boolean!
  ) {
    createArticle(
      userID: $userID
      categoryID: $categoryID
      title: $title
      content: $content
      isPublished: $isPublished
      isFeatured: $isFeatured
    ) {
      article {
        title
      }
    }
  }
`;
