import random

def generate_username(base_name):
    banglish_words = ['X', 'Boy', 'Mojar', 'Bhai', 'Shuvo', 'Dada', 'King', 'Queen', 'Pro', 'Hero', 'Guru', 'Master']
    rand_word = random.choice(banglish_words)
    base_name = base_name.capitalize()
    username = f"{base_name}{rand_word}{random.randint(1, 999)}"
    
    return username
