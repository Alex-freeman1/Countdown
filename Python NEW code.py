import random
import time
 
f = open('countdownwords.txt')
cd_words = f.read()
f.close()


possible_vowels = 'aeiou'
possible_consanents = 'bcdfghjklmnpqrstvwxyz'

score_list = []
name_list = []
Lopt = 0
game_number = 1

while True:
    try:
        playern = int(input("How many people are playing?"))
    except ValueError:
        print("oops, didn't get that")
    else:
        break

for i in range(playern):
    name = input("What is player {}'s name?".format(i+1))
    name_list.append(name)
player_turn = name_list[0]
name_listV = list(name_list)

for i in range(playern):
    score_list.append(0)


    
def wordCheck(name, word, length_word):
    if word in final_words:
        if len(word) == length_word:
            print("Fantastic word {}".format(name))
            legit_words[x] = word
        else:
            print("Your word was legit, but you declared the incorrect length of the word")
            legit_words[x] = 'a'
    else:
        print("Unfortunately {}, that is not a word or you cannot make this word with these letters".format(name))
        legit_words[x] = 'a'

while game_number > 0:
    Number_letters = 9
    cd_list = []
    cd_set = {}
    final_words = []
    bad_words = []
    length_list = []
    word_list = []
    legit_words = []
    for r in range(playern):
        legit_words.append(0)
        
    print("And its {}'s letters game".format(player_turn))
    print("{}, please choose 9 letters either vowels(v) or consonants(c)".format(player_turn))

    while Number_letters > 0:
        letters = input("What would you like")
        if letters == "v":
            final_vowel = random.choice(possible_vowels)
            cd_list.append(final_vowel)
            print(final_vowel)
            Number_letters = Number_letters - 1
        elif letters == "c":
            final_consanent = random.choice(possible_consanents)
            cd_list.append(final_consanent)
            print(final_consanent)
            Number_letters = Number_letters - 1
            
        else:
            print("Please enter either 'v' for vowel or 'c' for consonants ")
        
        if Number_letters == 0:
            cd_set = set(cd_list)
            print("The final letters are:")
            print(", ".join(cd_list))
            print("You now have 30 seconds to write down the longest word you can find with these letters")
            
            for word in cd_words.splitlines():
                word_letters = set(word)
                if word_letters <= cd_set:
                    final_words.append(word)
                else:
                    pass

            for word in final_words:
                for i in range(9):
                    if cd_list[i] in word:
                        count = word.count(cd_list[i])
                        if count > cd_list.count(cd_list[i]) and word not in bad_words:
                            bad_words.append(word)
                        else:
                            pass
                    else:
                        pass   
            for word in bad_words:
                final_words.remove(word)
                
            time.sleep(30)
            print("Aaaand times up")

            name_list = list(name_listV)
            for d in range(playern):
                while True:
                    try:
                        length_word = int(input("{}, How long was your word".format(name_list[d])))
                    except ValueError:
                        print("oops, didn't get that")
                    else:
                        length_list.append(length_word)
                        break

            
            length_listV = list(length_list)
            for i in range(playern):
                x = length_list.index(min(length_list))
                player_word = input("What was your word {}".format(name_list[x]))
                word_list.append(player_word)
                wordCheck(name_list[x], player_word, length_list[x])
                length_list[x] = length_list[x] + 9

            name_list = list(name_listV)
            length_list = list(length_listV)
            legit_wordsV = list(legit_words)
            sortedwords = sorted(legit_wordsV, key=len)
            m = len(sortedwords[-1])
        

            for s in range(playern):
                if len(legit_words[s]) == len(sortedwords[-1]):
                    score_list[s] = score_list[s] + m
            
            print('The scores at the moment is that...')
            for i in range(playern):
                print('{} has {} points'.format(name_list[i], score_list[i]))
                               
            time.sleep(1)       
            longestWord = ""
            for posword in final_words:
                if len(posword) > len(longestWord):
                    longestWord = posword
            print("And we move to dictionery corner..")
            time.sleep(1)
            print("Yeah the longest possible word we found was {}".format(longestWord))
            time.sleep(1)
            gameN = input("Would you like another game")
            if gameN == 'yes':
                game_number = game_number + 1
                Lopt = Lopt + 1
                if Lopt == playern:
                    Lopt = 0
                player_turn = name_list[Lopt]
                  
            else:
                WPI = score_list.index(max(score_list))
                WP = max(score_list)
                if len(set(score_list)) == playern:
                       print("The winner of Countdown and the person is taking of the 'Countdown Teapot' is {}".format(name_list[WPI]))
                       
                else:
                    Tie_count = score_list.count(WP)
                    print("It was a tie between.....")
                    for y in range(Tie_count):
                        Tie_x = score_list.index(WP)
                        print(name_list[Tie_x])
                        score_list[Tie_x] = 0
                    
    game_number = game_number - 1
