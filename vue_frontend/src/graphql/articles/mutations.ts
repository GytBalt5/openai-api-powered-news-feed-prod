import gql from "graphql-tag";

export const CREATE_ARTICLE = gql`
  mutation (
    $userID: ID!
    $topicID: ID!
    $title: String!
    $content: String!
    $isPublished: Boolean!
    $isFeatured: Boolean!
  ) {
    createArticle(
      userID: $userID
      topicID: $categoryID
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
