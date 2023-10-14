import gql from "graphql-tag";

export const SITE_INFO = gql`
  query {
    site {
      name
    }
  }
`;

export const ALL_CATEGORIES = gql`
  query {
    allCategories {
      id
      name
      slug
    }
  }
`;
