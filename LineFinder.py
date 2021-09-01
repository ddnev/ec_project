import sys
sys.path.append('C:/Users/Derek/anaconda3/envs/emsi_ec/Lib/site-packages/sklearn')
sys.path.append('C:/Users/Derek/anaconda3/envs/emsi_ec/Lib/site-packages/pandas/compat/numpy')

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

# Specify number of lines to return
num_return = 3

# Input
print('Words you remember from the line: ')
input = input()

# Read poem into memory
with open('lepanto.txt', encoding="utf8") as file:
    lines = file.readlines()

# Create vectorizer to compute TF, IDF and transform lines/input
#   TF: term frequency. This is (# times a term is used) / (# terms in the line); computed for each line.
#   IDF: inverse document frequency. This is (# lines) / (# times each unique term is used across all lines).
#   Transform: Encodes each line into a vector having length = # unique terms, where each element of the vector is the
#       TF*IDF for that line. If a term doesn't exist in a line then that element is 0.
vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)

# Because the resulting encoding is typically so sparse, the transformation result is returned as a CSR (sparse) matrix
# to facilitate matrix operations it is changed here to a full matrix.
encoded_lines = vectorizer.fit_transform(lines).toarray()

# Transform input - See comments above
encoded_input = vectorizer.transform([input]).toarray()

# Compute dot product
#   Now that the lines of the poem and the input are all encoded into the same vector space (as unit vectors!)
#   similarity between the input and each line is estimated using the dot product.
similarities = np.dot(encoded_lines, encoded_input.T)

# Select results to return
# Concatenate data to facilitate processing
lines_and_similarites = pd.concat([
    pd.DataFrame(similarities, dtype='float64', columns=['similarity']),
    pd.DataFrame(np.arange(0, 150).reshape(150, 1), dtype='int32', columns=['line_num']),
    pd.DataFrame(np.array(lines).reshape(150, 1), dtype='str', columns=['line_txt'])], axis=1)

# Order by similarity (descending)
lines_and_similarites = lines_and_similarites.sort_values('similarity', ascending=False)

# Remove results with similarity == 0
lines_and_similarites = lines_and_similarites[lines_and_similarites['similarity'] > 0]

# If there are lines with similarity > 0 return up to some number
if lines_and_similarites.shape[0] > 0:
    print('\nHere are the best matches based on your search terms: \n\t\t' + input + '\n')
    for index, row in lines_and_similarites[:num_return].iterrows():
        print('\t'+'['+str(row['line_num'])+'] '+row['line_txt'].rstrip('\n'))
# Else, inform the user no matching lines could be found
else:
    print('No lines appear to match your input. Care to try again?\n')



