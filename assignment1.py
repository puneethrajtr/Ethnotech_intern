vowels=['a','e','i','o','u']
string=input('Enter a word:')
word=string.lower()
new_word=''
count:int=0
index_count:int=0
for letter in word:
    count+=1
    if letter in vowels:
        print(new_word)
        if len(word)==count and letter==word[-2]:
            new_word+=letter

        elif letter is word[0] and letter==word[count] and index_count<1:
            new_word+=letter
            index_count=1

        elif letter==word[-1] and letter==word[-2] and word[count] in vowels:
            new_word+=letter


        elif letter==word[-1]:
            last_letter=True

        elif (letter==word[count] or letter==word[count-2]):
            print('hello')
            new_word+=letter

    else:
        new_word+=letter
print(f'The sorted string is "{new_word}"')