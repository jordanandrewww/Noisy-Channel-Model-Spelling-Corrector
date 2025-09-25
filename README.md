# Noisy-Channel-Model-Spelling-Corrector
A unigram + weighted-Levenshtein spelling corrector based on a noisy-channel model. Assumes ≤1 edit per word. Provides correct(original: str) -> str. Includes examples of strengths, weaknesses, and improvement ideas, using provided word frequency data.

# Here are some modeling assumptions that I made during this assignment:

1. At most 1 edit per word
Our algorithm assumes that the input word "original" differs from its intended/correct 
word by only one edit operation. This means that our model can't really be accurately
applied to words where more than one typo has been made.

2. Word edits are independent of context
Since I am modeling P(x | w) with only unigram or bigram statistics, plus
confusion matrices, we aren't using any sentence context. We are only using word-level
probability, which isn't as accurate as if we took into account what word would
"make most sense" within the context of a group of words.

3. Alphabet restrictions
We are only able to correct words that use the characters a-z. If words have any apostraphes,
accents, hypens, or capitalization, they won't be corrected.

4. No smoothing for unseen events
If an edit is made that produces a candidate that doesn't appear in our word list, it will
be treated as impossible, making its probability 0.

5. No transpositions
Since we were not provided with a csv file giving us information on transpositions,
we would only be able to model this as a combination of insertion/deletions, which would be
more than a single edit. Thus, our model does not cover transpositions.

6. When a candidate word is created multiple times (using multiple error models), my program adds
the probabilities together for that word.

# Here are some specific sceneratios in which my spelling corrector works well:

1. Simple substitution: Input: "nigjt" → Corrects to "night"
This works because "night" is very frequent in the unigram counts, and the "j" → "h" 
substitution is common in my substitution table.

2. Simple deletion: Input: "aweome" → Corrects to "awesome"
Thus works because "awesome" is common, and "s" deletion after "e" is in the 
deletion table with decent probability.

# Here are some specific sceneratios in which my spelling corrector does not work well:

1. Ambiguity between real words: Input: "from" (intended "form")
This word is kept as "from" because the word "from" is very common and therefore
has a high probability. So, when intended words are misspelled as real-words that are
more common than the intended word, it is not likely to be corrected with my current model.

Improvement: 

Use bigram or trigram probabilities over words (not just characters).

Example:

"came from London" → "from" is more likely in this context

"fill out the from" → "form" is correct and has a higher likelyhood here

This resolves ambiguity because the model looks at surrounding words, not just 
single-word frequency.

2. Out-of-vocabulary words: Input: "chatgptt" (not in count_1w.txt).
This prints out "No candidates found, returning the original word: chatgptt." The
issue here is that proper nouns or newer words won't be corrected unless they exist
in my word list.

Improvement:

We could add a larger lexicon or allow backoff to character-level models for 
unseen words. Both of these would increase the possibility of being able to correct
these words to their intended spelling.
