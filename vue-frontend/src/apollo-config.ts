import {
  ApolloClient,
  createHttpLink,
  InMemoryCache,
} from "@apollo/client/core";
import { createApolloProvider } from "@vue/apollo-option";

const httpLink = createHttpLink({
  uri: "http://127.0.0.1:8000/graphql",
});

const cache = new InMemoryCache();

const apolloClient = new ApolloClient({
  link: httpLink,
  cache,
});

export const apolloProvider = createApolloProvider({
  defaultClient: apolloClient,
});

export default apolloProvider;
