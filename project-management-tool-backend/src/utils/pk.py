import time
import random

def generate_unique_key():
    curr_code = ''.join(str(time.time()).split('.'))
    random_suffix = ''.join(chr(ord(char) + 20) for char in str(random.randint(10000, 99999)))
    
    pk = ''
    for i, char in enumerate(curr_code):
        if i < 5:
            temp = chr(ord(char) + 20) + random_suffix[i]
        elif i< 10:
            temp =chr(ord(char) + 20)
        else:
            temp =char
        pk+=temp
    
    if len(pk) < 22:
        pk = pk + ('0' * (22 - len(pk)))
        
    return pk

