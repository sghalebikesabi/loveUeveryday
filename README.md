# I love you everyday

This repository will give you a love statement in a different language every day and create a timely ordered list of the languages used so far.

The first time you run the program modify the data/langs_time.txt file such that it contains a list of languages you already know how to say 'I love you' in. After that run 
# python src/first_step.py 
This creates a pickle file with a list of tuples which contain respectively a random language and the corresponding translation. Now run 
# python main.py
which prints one of these tuples and updates the file 'langs_time.py'.
