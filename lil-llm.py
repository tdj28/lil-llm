corpus = """
Hello friend! I said to them. They were not sure whom I meant.
Hello friend! I said again, and still no one replied. Ok I said.
I will say Hello Alice and Hello Bob, but I don't know who the
rest of you are so I won't say Hello All or Hello everybody but I will
say Hello Alice and Hello Bob because Alice and Bob are people I would
say Hello too. Except I didn't say Hello Bob last time because Bob 
didn't say Hello to me. So, Hello Bob too, but if you aren't nice to
me I will not say Hello Bob anymore.
"""
tokens = corpus.lower().split()  # Simple tokenization

# Build bigrams (n-grams with n=2)
bigrams = {}
for i in range(len(tokens) - 1):
    gram = (tokens[i], tokens[i+1])
    bigrams[gram] = bigrams.get(gram, 0) + 1

# "Generation"
seed = "hello"
output = [seed]
for _ in range(7):  # Generate 7 words 
    possible_follows = [w for w in bigrams if w[0] == output[-1]]
    next_word = max(possible_follows, key=lambda x: bigrams[x])  # Greedy choice
    output.append(next_word[1])

print(" ".join(output))

