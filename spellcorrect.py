import csv

# helper function to calculate substitution scores and add them to candidates dictionary
def substitution_score(candidates: dict, original: str, word_counts: dict, total_word_count: int, unigram_counts: dict):
    sub_counts = {}
    with open('substitutions.csv', 'r') as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            orig_char, sub_char, count = row
            sub_counts[(orig_char, sub_char)] = int(count)
    
    for i in range(len(original)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != original[i]:
                # substitute character at position i with c
                candidate = original[:i] + c + original[i+1:]
                if candidate in word_counts:
                    # calculate P(w)
                    p_w = word_counts[candidate] / total_word_count
                    # calculate P(x | w)
                    p_x_given_w = sub_counts.get((candidate[i], original[i]), 0) / unigram_counts[candidate[i]]
                    # calculate score
                    score =  p_w * p_x_given_w
                    # adding to existing score if candidate already exists
                    if candidate in candidates:
                        candidates[candidate] += score
                    else:
                        candidates[candidate] = score

# helper function to calculate deletion scores and add them to candidates dictionary
def deletion_score(candidates: dict, original: str, word_counts: dict, total_word_count: int, bigram_counts: dict):
    del_counts = {}
    with open('deletions.csv', 'r') as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            prefix, deleted_char, count = row
            del_counts[(prefix, deleted_char)] = int(count)

    # iterate through each position in the original word, including one position after the last character
    for i in range(len(original) + 1):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            # add character c at position i to undo deletion
            candidate = original[:i] + c + original[i:]
            if candidate in word_counts:
                # calculate P(w)
                p_w = word_counts[candidate] / total_word_count
                # calculate P(x | w)
                prefix = candidate[i-1] if i > 0 else ""
                p_x_given_w = del_counts.get((prefix, c), 0) / bigram_counts.get(prefix + c, 1)
                # calculate score
                score =  p_w * p_x_given_w
                # adding to existing score if candidate already exists
                if candidate in candidates:
                    candidates[candidate] += score
                else:
                    candidates[candidate] = score

# helper function to calculate addition scores and add them to candidates dictionary
def addition_score(candidates: dict, original: str, word_counts: dict, total_word_count: int, unigram_counts: dict):
    add_counts = {}
    with open('additions.csv', 'r') as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            prefix, added_char, count = row
            add_counts[(prefix, added_char)] = int(count)

    # iterate through each position in the original word
    for i in range(len(original)):
        # remove character at position i to undo addition
        candidate = original[:i] + original[i+1:]
        if candidate in word_counts:
            # calculate P(w)
            p_w = word_counts[candidate] / total_word_count
            # calculate P(x | w)
            prefix = candidate[i-1] if i > 0 else ""
            p_x_given_w = add_counts.get((prefix, original[i]), 0) / unigram_counts[original[i]]
            # calculate score
            score =  p_w * p_x_given_w
            # adding to existing score if candidate already exists
            if candidate in candidates:
                candidates[candidate] += score
            else:
                candidates[candidate] = score

# takes in a word that has been misspelled and returns the corrected word according to a
# noisy channel model composed of a unigram model and weighted-Levenshtein-distance error model

# can assume each word is corrupted by at most one edit

# we are given the following:
# a file called count_1w.txt that contains a list of words and their counts from a large corpus
# a file called additions.csv that contains a list of prefixs, what was added after that prefix, and the count of how many times that addition was made
# a file called deletions.csv that contains a list of prefixes, what was deleted after that prefix, and the count of how many times that deletion was made
# a file called substitutions.csv that contains a list of original characters, what they were substituted with, and the count of how many times that substitution was made
# a file called bigrams.txt that contains a list of bigrams and their counts from a large corpus
# a file called unigrams.txt that contains a list of unigrams (single letters) and their counts from a large corpus
def correct(original : str) -> str:
    total_word_count = 0

    # store all words and their counts in a dictionary
    word_counts = {}
    with open('count_1w.txt', 'r') as f:
        for line in f:
            word, count = line.split()
            word_counts[word] = int(count)
            total_word_count += int(count)

    # store all unigram counts in a dictionary
    unigram_counts = {}
    with open('unigrams.csv', 'r') as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            unigram, count = row
            unigram_counts[unigram] = int(count)
    
    # store all bigram counts in a dictionary
    bigram_counts = {}
    with open('bigrams.csv', 'r') as f:
        reader = csv.reader(f)
        # skip the header
        next(reader)
        for row in reader:
            bigram, count = row
            bigram_counts[bigram] = int(count)

    # stores all possible candidates for the corrected word and their probabilities (P(w) x P(x | w))
    candidates = {}
    # add original word to candidates in case it is correct
    if original in word_counts:
        candidates[original] = word_counts[original] / total_word_count

    # generate all possible substitutions of one character
    substitution_score(candidates, original, word_counts, total_word_count, unigram_counts)
    # generate all possible deletions of one character
    deletion_score(candidates, original, word_counts, total_word_count, bigram_counts)
    # generate all possible additions of one character
    addition_score(candidates, original, word_counts, total_word_count, unigram_counts)
    # generate all possible transpositions of adjacent characters
    # transposition_score(candidates, original, word_counts, total_word_count, bigram_counts, unigram_counts)

    # returns the candidate with the highest probability
    if candidates:
        return max(candidates, key=candidates.get)
    else:
        print("No candidates found, returning the original word:")
        return original
    

if __name__ == "__main__":

    # substitution tests
    print(correct("awedome")) # returns "awesome"
    print(correct("nigjt")) # returns "night"
    print(correct("playbul")) # returns "playful"
    print(correct("tantrom")) # returns "tantrum"

    # deletion tests
    print(correct("aweome")) # returns "awesome"
    print(correct("pupy")) # returns "puppy"
    print(correct("stpid")) # returns "stupid"
    print(correct("umb")) # returns "umb"

    # addition tests
    print(correct("awesoome")) # returns "awesome"
    print(correct("pupppy")) # returns "puppy"
    print(correct("sillly")) # returns "silly"
    print(correct("justifieed")) # returns "justified"


    











        






    
