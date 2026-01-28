Question 1 (1 point) 
 Saved
The process of converting raw text into a sequence of  units that a model can process.

Question 1 options:

Tokenization


Lemmatization


Stemming

Question 2 (1 point) 
 Saved
For which of the following tasks we shouldn’t do stemming/lemmatization?

Question 2 options:

Sentiment Analysis

Poetry Analysis

Text Classification
Question 3 (1 point) 
 Saved
SpaCy does not provide a built-in function for Stemming 

Question 3 options:
	True
	False
Question 4 (1 point) 
 Saved
The following rgx will match all the words ended with a hyphen(-)  :

rgx = r'\b\w+[-]\w+\b'

Question 4 options:
	True
	False
Question 5 (1 point) 
 Saved
Text cleaning removes noise (like special characters, irrelevant symbols, and unnecessary spaces) and standardizes the text (e.g., converting to lowercase),  is essential for improving the quality of the data and the performance of NLP models.

Question 5 options:
	True
	False
Question 6 (1 point) 
 Saved
Consider you have the following list that represents the USA's state names:

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado',

          'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho',

          'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',

          'Maine','Maryland','Massachusetts','Michigan','Minnesota',

          'Mississippi','Missouri','Montana','Nebraska','Nevada',

          'New Hampshire','New Jersey','New Mexico','New York',

          'North Carolina','North Dakota','Ohio','Oklahoma','Oregon',

          'Pennsylvania','Rhode Island','South Carolina','South Dakota',

          'Tennessee','Texas','Utah','Vermont','Virginia','Washington',

          'West Virginia','Wisconsin','Wyoming']


 which python expression that output Which state names start and end with a "vowel" character? 

Question 6 options:

[s for s in states if s[0].lower() in 'aeiou' and s[1] in 'aeiou']


[s for s in states if s[0].lower() in 'aeiou' and s[-1] in 'aeiou']


[s for s in states if s[1].lower() in 'aeiou' and s[-1] in 'aeiou']

Question 7 (1 point) 
 Saved
When might you use lemmatizing over stemming?

Question 7 options:

when accuracy is preferred more than speed


when non-dictionary words are allowed to appear in the output


when the data file contains a large number of simple words


when speed is preferred more than accuracy

Question 8 (1 point) 
 Saved
Pick the stemming action

Question 8 options:

was, am, is , are ----> be


helped, helps -----> help


troubled, troubling , trouble ------> trouble

Question 9 (1 point) 
 Saved
Consider the provided code snippet:

Text='I love NLP and I am read9y to study in 5 hours per Day'
regex='[a-zA-Z]\w*d+'

print(re.findall(regex,Text))

the output is : [and]

Question 9 options:
	True
	False
