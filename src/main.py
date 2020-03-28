'''
Once you have run first_step.py, run this file everyday to get 
one translation of 'I love you' which you have not used before.

Author: Sahra Ghalebikesabi
'''

import pickle 


with open('data/a_loveu_everyday.pkl', 'rb') as file:
    a_loveu_everyday = pickle.load(file)

loveU_of_today = a_loveu_everyday.pop(0)
print(loveU_of_today)

with open('data/langs_time.txt', 'a') as file:
    file.write(loveU_of_today[0])

with open('data/a_loveu_everyday.pkl', 'wb') as file:
    pickle.dump(a_loveu_everyday, file, protocol=pickle.HIGHEST_PROTOCOL)