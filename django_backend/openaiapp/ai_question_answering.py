import openai
from openai.embeddings_utils import distances_from_embeddings

from openaiapp.embeddings import create_embedding
from openaiapp.text_preparation import generate_each_text_of_df_tokens_amount


CONTEXT_MAX_LEN = 1800


# NOTE. This functions copy pasted from OpenAI's documentation.
# TODO. Need refactoring.
def create_context(question, df, max_len=CONTEXT_MAX_LEN):
    """
    Create a context for a question by finding the most similar context from the data frame.
    """

    df = generate_each_text_of_df_tokens_amount(df=df)

    # Get the embeddings for the question.
    q_embeddings = create_embedding(input=question)

    # Get the distances from the embeddings.
    df["distances"] = distances_from_embeddings(
        q_embeddings, df["embeddings"].values, distance_metric="cosine"
    )

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long.
    for _, row in df.sort_values("distances", ascending=True).iterrows():
        # Add the length of the text to the current length.
        cur_len += row["n_tokens"] + 4

        # If the context is too long, break.
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned.
        returns.append(row["text"])

    # Return the context.
    return "\n\n###\n\n".join(returns)


# NOTE. This functions copy pasted from OpenAI's documentation.
# TODO. Need refactoring.
def answer_question(
    df,
    model="gpt-3.5-turbo-instruct",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    debug=False,
    max_tokens=150,
    stop_sequence=None,
):
    """
    Answer a question based on the most similar context from the dataframe texts.
    """
    context = create_context(question, df, max_len=max_len)
    # If debug, print the raw model response.
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the question and context.
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""