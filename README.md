# ec_project

## Summary
This python script helps users find lines from the poem "Lepanto" by G.K. Chesterton based on words or phrases they remember.

After executing the script, the user inputs what they recall from the poem in the command line and up to three of the best matching lines of the poem (along with the line number) are returned.

## Installation
###_Requirements_
<li>Python3 - 3.7 Should be included in Debian Buster; to check:</li>

> $ python3 --version

<li> Python virtual environments (for convenience)

> $ sudo apt-get install python3-venv 

<li>Git</li>

>$ sudo apt install git-all

###_To Run_

After making sure requirements are met use the following commands: 

1) Clone the git repo
>$ git clone https://github.com/ddnev/ec_project.git _ProjectDirectory_

2) Create a virtual environment 
>$ python3 -m venv _VenvDirectory_

3) Activate the newly created virtual environment
>$ source _VenvDirectory_/bin/activate

4) With the virtual environment activated, install necessary packages
>$ python3 -m pip install numpy
>
>$ python3 -m pip install scikit-learn
>
>$ python3 -m pip install pandas

## Operation
First, make sure you've activated the correct virtual environment:
>$ source _VenvDirectory_/bin/activate

Next, navigate to the project folder. 

To execute the script use the following command:
>$ python3 LineFinder.py


## Solution Design
The objective of this program is to help a user find a line from the poem that they don't remember in full, but may recall some part of. 
In general, the task is to map the user input to the line of the poem it most likely comes from.
To accomplish this the program attempts to determine which line is most similar to the user input.

The program does this by transforming each line of the poem and the user input into a vector space defined by the vocabulary of the poem using the TF-IDF approach.
This approach consists of two parts: calculating the term frequency (TF) for each term in _each line_ and the inverse document frequency (IDF) of each term within the _whole document_ (here the poem).
> TF = (# times term is present in the line) / (# of unique terms in the line)
> 
> IDF = (# unique terms in the poem) / (# times the term is present in the poem)

So, if a term is used frequently in a particular line it will have a large TF value. 
If it doesn't occur in that line it the TF value will be 0.
Likewise, if a term is used many times throughout the poem it will have a small IDF value (remember it's inverse frequency). If it's used rarely then it will have a large IDF value.
Thus, each line of the poem can be represented as a vector where each element in that vector corresponds to one of the unique terms in the poem and the element value is the product of the TF and IDF values for that term.
The same process can be used to transform user input into the same vector space as the poem lines.

Now that the poem lines and user input are in the same space the similarity between each line and the user input can be estimated using the dot product. 
The output of this computation essentially tells us how aligned the poem-line vector and user-input vectors are, which we use as a proxy for similarity.
This computation conveniently returns a scalar value for each line of the poem, with the better matching lines having a higher similarity value.
The lines can be ordered by similarity value and any number returned.
Because the user may confuse content from multiple lines, up to the top three results with non-zero similarity are returned. 

So what do we get for all this effort? The TF-IDF approach implicitly decreases the weight of terms which appear frequently in the poem.
This is convenient because common words like "a", "the", etc. will not be very helpful in discriminating between lines and should not be given the same weight as more uncommon terms when looking for a match.
This saves us the trouble of defining a set of stop words to remove, though doing so may still increase accuracy.
Encoding the poem and user input into a vector space also gives us other advantages. The dot product computation is very efficient compared to iterating over lists of strings.

One practical consideration is the how to define "term", which may be a single word or sequence of words. 
Intuitively, there is additional information in the ordering of words within a line beyond just the words themselves.
To take advantage of this information we can treat each unique sequence of _n_ words as a term.
A high value for _n_ would lead to higher accuracy, but could significantly expand the vocabulary space and decrease efficiency. 
To balance these concerns, this programs uses terms of one or two words in length.

There are several limitations to this design that might be addressed if the higher accuracy is required or constraints on time/resources are eased:
<li>Spelling/Tense: The program does not do any stemming or lematization, so if a user inputs a verb from the poem but doesn't use the same tense as the one in the poem the transformation will ignore this word completely.</li>
<li>Synonyms: A user might input a synonym for a word in the poem, rather than the word itself. A more sophisticated algorithm is required to address this case.</li>


