import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import entropy

with open('corpus.txt', 'r') as file:
    corpus = file.read()

tokens = corpus.lower().split()

# Build bigrams (n-grams with n=2)
bigrams = {}
for i in range(len(tokens) - 1):
    gram = (tokens[i], tokens[i+1])
    bigrams[gram] = bigrams.get(gram, 0) + 1

def generate_text(seed, temperature, length=15):
    output = [seed]
    for _ in range(length):  
        possible_follows = [w for w in bigrams if w[0] == output[-1]]

        if possible_follows: 
            next_words = [x[1] for x in possible_follows] 
            probabilities = [bigrams[x] for x in possible_follows]

            if temperature == 0:
                print("You can't divid by zero, friend!")
                exit(1)
            else:
                adjusted_probs = [p ** (1 / temperature) for p in probabilities] 
                prob_sum = sum(adjusted_probs)
                normalized_probs = [p / prob_sum for p in adjusted_probs]
                next_word = random.choices(next_words, weights=normalized_probs)[0]  
            
            output.append(next_word)
        else:
            break  

    return " ".join(output)

def calculate_entropy(texts):
    all_words = " ".join(texts).split()
    word_counts = Counter(all_words)
    word_probs = np.array(list(word_counts.values())) / sum(word_counts.values())
    return entropy(word_probs)

# Generate text and calculate entropy for all words in the corpus
seed_words = set(tokens)
temperature_values = np.arange(0.1, 3.1, 0.1)
entropies = []

for temp in temperature_values:
    runs = []
    for seed in seed_words:
        for _ in range(5):  # Generate multiple runs per seed
            runs.append(generate_text(seed, temp))
    entropies.append(calculate_entropy(runs))

# Plotting Entropy vs. Temperature
plt.figure(figsize=(10, 6))
plt.plot(temperature_values, entropies, marker='o')
plt.xlabel('Temperature')
plt.ylabel('Entropy')
plt.title('Entropy vs. Temperature')
plt.grid(True)
plt.show()

# Function to get adjusted probabilities for different temperatures
def get_adjusted_probabilities(seed, temperatures):
    prob_distributions = {}
    possible_follows = [w for w in bigrams if w[0] == seed]
    next_words = [x[1] for x in possible_follows] 
    probabilities = [bigrams[x] for x in possible_follows]

    for temp in temperatures:
        if temp == 0:
            adjusted_probs = [1.0] * len(probabilities)
        else:
            adjusted_probs = [p ** (1 / temp) for p in probabilities] 
            
        prob_sum = sum(adjusted_probs)
        normalized_probs = [p / prob_sum for p in adjusted_probs]
        prob_distributions[temp] = normalized_probs

    return next_words, prob_distributions

# Get adjusted probabilities for selected temperatures
selected_temperatures = [0.5, 1, 1.5, 2, 3]
seed = "we"
next_words, prob_distributions = get_adjusted_probabilities(seed, selected_temperatures)

# Plotting the probability distributions
plt.figure(figsize=(10, 6))

for temp in selected_temperatures:
    plt.plot(next_words, prob_distributions[temp], marker='o', label=f'T={temp}')

plt.xlabel('Next Words')
plt.ylabel('Probability')
plt.title(f'Probability Distribution for Seed "{seed}" at Different Temperatures')
plt.legend()
plt.grid(True)
plt.show()

# Generate runs and create markdown tables for different temperature values
temperature_values = [0.5, 1, 1.5, 2, 3]
all_tables = ""

for temp in temperature_values:
    runs = [generate_text("we", temp) for _ in range(5)]
    
    markdown_table = f"### Temperature = {temp}\n\n"
    markdown_table += "| Run | Output |\n|-----|--------|\n"
    for i, run in enumerate(runs, 1):
        markdown_table += f"| Run {i} | {run} |\n"
    markdown_table += "\n"
    all_tables += markdown_table

print(all_tables)