# Importing libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import time
import winsound
import sys

# Lists of different letters in the respective lists
possible_vowels = 'aeiou'
vowel_weights = [8.2, 12.7, 7.0, 7.5, 2.8]

possible_consanents = 'bcdfghjklmnpqrstvwxyz'
consonant_weights = [
    1.5, 2.8, 4.3, 2.2, 2.0, 6.1, 0.2, 0.8, 4.0, 2.4,
    6.7, 1.9, 0.1, 6.0, 6.3, 9.1, 1.0, 2.4, 0.2, 2.0, 0.1
]

# Opens the file of the all English words that this game uses and saves it as cd_words
cdWords_file = open('countdownwords.txt')
cd_words = cdWords_file.read()
cdWords_file.close()

# Sets the name of Tk() to root
root = Tk()

# Function that will run the normal part of the game
def Normalmain():

    # Used global here to define these lists, didn't use return because it won't be transferred to the other function of this level.
    # As in these variables are staying in this function 'Normalmain' and won't leave it
    global length_list
    global word_list
    global cd_list
    global final_words
    global bad_words
    global legit_words
    global score_list
    

    label_Game.grid_remove()
    player_list = []

    # Creates different label frames for each different subset
    # Some are currently hidden and then revealed when necessery to avoid clutter and overcomplication
    labelframe_choose = LabelFrame(root, text="Choose")

    labelframe_word = LabelFrame(labelframe_choose, text="Word")
    labelframe_word.grid_remove()

    labelframe_length = LabelFrame(labelframe_choose, text="Length")
    labelframe_length.grid(row=4, column=0) 

    labelframe_setup = LabelFrame(root, text="Setup")
    labelframe_setup.grid(row=0, column=0)

    labelframe_timer = LabelFrame(root, text="Timer")

    labelframe_score = LabelFrame(root, text="Score")
    labelframe_score.grid_remove()

    labelframe_letter = LabelFrame(root, text="Letter")
    labelframe_letter.grid(row=5, column=0)

    labelframe_finish = LabelFrame(root, text="End")

    # These var are defined in the scope of root itself, and therefore work as counters and do not need globals
    root.v_position = 0
    root.counti = 0
    root.countz = 0
    root.x_position = 0
    root.countd = 1

    # Declaring the rest of the variables
    x_position = 0
    i_position = 0 
    y_position = 0
    length_list = []
    word_list = []
    cd_list = []
    final_words = []
    bad_words = []
    legit_words = []
    score_list = []

    
    # 'waithere' is a function used as a timing system, where when it runs, the program pauses for 1 second
    def waithere():
        var = IntVar()
        # The time is 65 milliseconds off from a perfect second due to the music; I wanted the clock to finish at the same time as the music beat
        # A regular time.sleep(var) would not work here because it is a GUI and the whole thing would just stop not running anything
        root.after(1065, var.set, 1)
        root.wait_variable(var)
        
    # This will run when users want to stop playing and see who one
    def finish_game():
        # Removes these frames because users don't need to see them anymore
        labelframe_score.grid_remove()
        labelframe_letter.grid_remove()
        labelframe_timer.grid_remove()
        
        labelframe_finish.grid(row=0, column=0)

        # Finds the index of the winning player
        WPI = score_list.index(max(score_list))
        # Finds the player that has the most points. (May be a tie, but it will just choose the first player that is winning, and will use this to match against other players' scores)
        WP = max(score_list)
        # If there is only one person that has the highest score, then that person wins
        if score_list.count(WP) == 1:
            win_label = Label(labelframe_finish, text='The winner of Countdown and the person is taking of the Countdown Teapot is... {}'.format(player_list[WPI]))
            win_label.grid(row=0, column=0)
        #If there is a tie will print all players that have tied 
        else:
            # Counts how many times the top score occurs
            Tie_count = score_list.count(WP)
            winTie_label = Label(labelframe_finish, text='It was a {} way tie between.....'.format(Tie_count))
            winTie_label.grid(row=0, column=0)
            # Goes through each player's score, if it is the same as the winning score will print them as tied for first place
            for i in range(playern):
                player_winner = StringVar()
                player_winner.set(player_list[i])
                if (score_list[i]) == WP:
                    winPlayer_label = Label(labelframe_finish, textvariable=player_winner)
                    winPlayer_label.grid(row=i+1, column=0)

    # When players ask for another game, all variables need to be reset
    def reset():
        global i_position
        global x_position
        y_position = 0
        x_position = 0
        i_position = 0
        root.v_position = 0
        root.counti = 0
        root.countz = 0
        root.x_position = 0

        # Rebinds the enter button for the next game
        root.bind('<Return>', lambda event=None: number_button.invoke())

        # Because this label will have information from the previous game and will only update until it gets to that stage, this code will immediatley update the GUI
        # This prevents there being a period of time where where the GUI asks the last player what there word was
        letterDerive = Label(labelframe_length, text="How long was your word {}".format(player_list[0]))
        letterDerive.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)

        # Destroys all widgets in the labelframe ready to have new variables inserted
        for widget in labelframe_letter.winfo_children():
            widget.destroy()

        # Clears all these variables to reset the game
        cd_list.clear()
        final_words.clear()
        legit_words.clear()
        word_list.clear()
        length_list.clear()
        bad_words.clear()
        DictioneryConerLabel.destroy()
        labelframe_word.grid_remove()
        labelframe_length.grid(row=4, column=0)
        labelframe_score.grid_remove()
        labelframe_timer.grid_remove()
        labelframe_choose.grid(row=4, column=0)

        # Restates these buttons to normal allowing them to be used again
        letters_buttonVowel.config(state=NORMAL)
        letters_buttonConsonant.config(state=NORMAL)

        return cd_list

    # This function is run when players input the amount of people playing
    # This has error prevention in mind as it won't allow anything other than a positive integer greater
    # If this was the case it will show an error message and prevent them from continuing
    # Also if they input a number greater than 10, it will ask them to confirm 
    def playernumber():
        global playern
        try:
            playern = player_number.get()
        except:
            # If this requirement fails, then the user will see a message box with the following message
            messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
            # Resets the box so that the user can input a new value
            player_number.set("")
        # If the input is an integer, the code needs to check if it's above 0. It won't work if it isn't as the game will run for infinitely long trying to reach -n players by adding
        else:
            if playern < 1:
                messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
                player_number.set("")
            # Finally, if the number is real and valid, then if will ensure that they haven't accidently inputted a really large number that clearly wouldn't work
            else:
                if playern > 10:
                    MsgBox = messagebox.askquestion ('Are you sure', 'You have inputted a number more than 10, would you like to continue?',icon = 'warning')
                    if MsgBox == 'no':
                       messagebox.showinfo('Return','You will now return to the application screen')
                       player_number.set("")
                    else:
                        player_number.set("")
                        root.bind("<Return>", lambda e: None)
                        root.bind('<Return>', lambda event=None: playerbutton.invoke())
                        player_button.config(state=DISABLED)
                        playerbutton.config(state=NORMAL)
                        name_label = Label(labelframe_setup, text="What is player 1's name?")
                        name_label.grid(row=3, column=0)
                        return playern
                else:
                    player_number.set("")
                    root.bind("<Return>", lambda e: None)
                    root.bind('<Return>', lambda event=None: playerbutton.invoke())
                    player_button.config(state=DISABLED)
                    playerbutton.config(state=NORMAL)
                    name_label = Label(labelframe_setup, text="What is player 1's name?")
                    name_label.grid(row=3, column=0)

                    return playern

    # Function to attain the names of each person
    def nameGet():
        # Prompt for players to know what to input
        name_label = Label(labelframe_setup, text="What is player {}'s name?".format(root.countd+1))
        name_label.grid(row=3, column=0)
        #Getting player's names and appending to a list
        player_name = name_datum.get()
        name_datum.set("")
        player_list.append(player_name)
        if len(player_list) == playern:

            # Unbinds and binds the return key to the new function, to ensure no overlapping
            # Binds 'c' and 'v' for consonant and vowel button functions
            root.bind("<Return>", lambda e: None)
            root.bind('<Return>', lambda event=None: number_button.invoke())
            root.bind('c', lambda event=None: letters_buttonConsonant.invoke())
            root.bind('v', lambda event=None: letters_buttonVowel.invoke())
            labelframe_setup.grid_remove()
            labelframe_choose.grid(row=4, column=0)

        root.countd +=1
        return player_list

    # This function is designed to increase this variable by 1, it is used as a counter so that the code knows how many times something has been run 
    def increaseI():
        root.v_position +=1
        return root.v_position

    # This will just print the first name of the player_list to update necessery frames
    def player1print():
        letterDerive = Label(labelframe_length, text="How long was your word {}".format(player_list[0]))
        letterDerive.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)

    # A function for later that checks the word and adds it to a list if legit and correct 
    def wordCheck(word, length_word):
        if word in final_words:
            # If the word is valid, then the word will be appended
            if len(word) == length_word:
                legit_words.append(word)
                # If the word is not valid, nothing is appended to the list
            else:
                legit_words.append('')
        else:
            legit_words.append('')

    

    # This function is at the end of the game, where it is called after the final person inputs their word
    # It will create labels that have the information regarding the scores or each player, and the longest word possible, as well as a button if people want to have another game
    def funcscore():
        global DictioneryConerLabel
        # Manipulating lists to sort them and then take the longest word
        labelframe_choose.grid_remove()
        labelframe_score.grid(row=0, column=0)
        for i in range(playern):
            score_list.append(0)
        length_listV = list(length_list)
        legit_wordsV = list(legit_words)
        sortedwords = sorted(legit_wordsV,key = len)
        Long_word = sortedwords[-1]
        LW_length = len(Long_word)
        for y in range(playern):
            if len(legit_words[y]) == len(Long_word):
                score_list[y] = score_list[y] + LW_length

        scoreLabel = Label(labelframe_score, text="The scores at the moment are...")
        scoreLabel.grid(row=0, column=0, padx=50, pady=20)
        
        # Displays the relevant information regarding scores, and the longest word
        DictioneryConerLabel = Label(labelframe_score, text="The longest word we found in Dictionery Corner was {}".format(longestWord))
        DictioneryConerLabel.grid(row=playern+1, column=0, pady=30)
        # Print scores after each round
        for i in range(playern):
            scoreLabel = Label(labelframe_score, text="Player {} has {} points".format(i+1, score_list[i]))
            scoreLabel.grid(row=i+1, column=0)
            
        # Creates a button for people to press if which will run the function 'reset', which resets all variables and lists, allowing for another game to be played
        reset_button = ttk.Button(labelframe_score, text="Replay", command=reset)
        reset_button.grid(row=playern+2, column=0)

        # Creates a button for people to press if which will run the function 'finish_game', which causes the game to stop and prints the winner(s)
        finish_button = ttk.Button(labelframe_score, text="Finish", command=finish_game)
        finish_button.grid(row=playern+3, column=0)

        
        
    # This will run the function to test the words with the variables of the length of the word and the word itself
    # It returns the x_position as this will be updated again and again
    def funcwordList():
        global length_list
        
        player_word = VarEntry_word.get()
        player_wordLower = player_word.lower()
        word_list.append(player_wordLower)
        VarEntry_word.set("")

        
        # Runs the function to check the words, using the parameters of player's words and the lengths of their words
        wordCheck(word_list[root.x_position], length_list[root.x_position])
        root.x_position = root.x_position + 1


        # If everyone has inputted their words, the next part of the code can run
        if len(legit_words) == playern:
            # Unbinds everything that the return key was binded to, ready for this key to be rebinded to another
            root.bind("<Return>", lambda e: None)
            funcscore()
        else:
            # If not everyone has inputted their words, it will ask the next person
            root.counti +=1
            wordDerive2 = Label(labelframe_word, text="What was your word {}".format(player_list[root.counti]))
            wordDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
        return root.x_position
        return root.counti
    
    # This is designed to get each of the player's words by asking         
    def grabWord():
        global VarEntry_word

        # Unbinds everything that the return key was binded to, ready for this key to be rebinded to another
        root.bind("<Return>", lambda e: None)
        
        labelframe_length.grid_remove()
        labelframe_word.grid(row=4, column=0)
        wordDerive = Label(labelframe_word, text="What was your word {}".format(player_list[0]))
        wordDerive.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
              
        VarEntry_word = StringVar()
        VarEntry_word.set("")
        wordEntry = Entry(labelframe_word, textvariable=VarEntry_word)
        wordEntry.grid(row=6, column=0, columnspan=9, sticky="WE", padx=100,pady=10)

        # Runs funcwordList, the next part of the game
        wordEntryButton = Button(labelframe_word, text="Submit", command=funcwordList, bg="red", activebackground="lawngreen")
        wordEntryButton.grid(row=7, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
        root.bind('<Return>', lambda event=None: wordEntryButton.invoke())

        return VarEntry_word
      

    def declareLetters():
        if root.v_position == playern-1:
            root.v_position = 0
        # Built in error prevention
        try:
            length_word = number_declare.get()
        except:
            messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
            number_declare.set("")
        else:
            # Ensures that negative values were excluded
            if length_word < 1:
                messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
                player_number.set("")
                number_declare.set("")
            else:
                # If number is greater than 9, code will assume that this was a misinput, and there are only 9 letters so the code will ask for a confirmation
                if length_word > 9:
                    MsgBox = messagebox.askquestion ('Are you sure', 'You have inputted a number more than 9, would you like to continue?',icon = 'warning')
                    if MsgBox == 'no':
                       messagebox.showinfo('Return','You will now return to the application screen')
                       number_declare.set("")
                    else:
                        length_list.append(length_word)
                        number_declare.set("")
                        increaseI()
                        letterDerive2 = Label(labelframe_length, text="How long was your word {}".format(player_list[root.v_position]))
                        letterDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
                else:
                    length_list.append(length_word)
                    number_declare.set("")
                    if playern != 1:
                        increaseI()
                        letterDerive2 = Label(labelframe_length, text="How long was your word {}".format(player_list[root.v_position]))
                        letterDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
                    else:
                        letterDerive2 = Label(labelframe_length, text="How long was your word {}".format(player_list[0]))
                        letterDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
                
        if len(length_list) == playern:
            grabWord()


                    
    def disButton():
        global longestWord
        global list_var
        player1print()
        # Normalise button 
        number_button.config(state=NORMAL)
        # Plays the mp3 file called 'Countdownsound'
        winsound.PlaySound('CountdownSound', winsound.SND_ASYNC)

        # This code is important prevents error later in the code if the buttons are disabled to ensure that no more than 9 letters are generated
        letters_buttonVowel.config(state=DISABLED)
        letters_buttonConsonant.config(state=DISABLED)
        
        # Creates a list with ALL words that contain only the 9 letters (duaplicates are included)
        cd_set = set(cd_list)
        for word in cd_words.splitlines():
            word_letters = set(word)
            if word_letters <= cd_set:
                final_words.append(word)
            else:
                pass

        # Uses the 'count' function as a test for each word and adds to a valid word list
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
            
        # Finds the longest possible word using the letters by going through the list of all possible words
        longestWord = ""
        for posword in final_words:
            if len(posword) > len(longestWord):
                longestWord = posword

        # This is timer which uses the a for loop with range of 30 to print a label with no text but a background of blue
        # Using the function of 'waitthere' which waits for 1 second, the timer will acurately time for 30 seconds
        # The two '|' are used as the start and stop parts to players can visually see when its going to end
        labelframe_timer.grid(row=8, column=0)
        createLabelstart = Label(labelframe_timer, text="|")
        createLabelstart.grid(row=0, column=0)
        for i in range(1,31):
            copylabel = Label(labelframe_timer)
            copylabel.grid(row=0, column=i)
            if i == 30:
                createLabelend = Label(labelframe_timer, text="|")
                createLabelend.grid(row=0, column=i)
        for i in range(1,30):
            timeLabel = Label(labelframe_timer, text="", bg='blue')
            timeLabel.grid(row=0, column=i)
            waithere()

        # returns the var longestWord as another function then takes this and then prints later on in the game
        return longestWord
    # The buttons to generate vowels and consonant when players press them
    def vowel_letter():
        global i_position
        final_vowel = random.choices(possible_vowels, weights=vowel_weights, k=1)[0]
        cd_list.append(final_vowel)
        vowel_datum = StringVar()
        vowel_datum.set(final_vowel.capitalize())
        label_vowel = Label(labelframe_letter, textvariable=vowel_datum)
        label_vowel.config(font=("Courier", 20))
        label_vowel.grid(row=4, column=i_position,columnspan=1)
        
        i_position = i_position + 1
        if i_position == 9:
            disButton()
            
    def consonant_letter():
        global i_position
        final_consanent = random.choices(possible_consanents, weights=consonant_weights, k=1)[0]
        cd_list.append(final_consanent)
        consanent_datum = StringVar()
        consanent_datum.set(final_consanent.capitalize())
        label_consanent = Label(labelframe_letter, textvariable=consanent_datum)
        label_consanent.config(font=("Courier", 20))
        label_consanent.grid(row=4, column=i_position,columnspan=1)
        
        i_position = i_position + 1
        if len(cd_list) == 9:
            disButton()
        
    # Label to pose the question that will be visible to the players
    n_players = Label(labelframe_setup, text='How many people are playing?')
    n_players.grid(row=0, column=0)

    # Widgets for acquiring the number of people playing, and will run function 'playernumber'
    player_number = IntVar()
    player_number.set("")
    playerEntry = Entry(labelframe_setup, textvariable=player_number)
    playerEntry.grid(row=1, column=0)
    player_button = ttk.Button(labelframe_setup, text="Submit", command=playernumber)
    player_button.grid(row=2, column=0, padx=100,pady=10)
    root.bind('<Return>', lambda event=None: player_button.invoke())

    # An entry box and button combo to acquire the names of the people who are playing, and will run the function 'nameGet'
    name_datum = StringVar()
    name_datum.set("")
    nameEntry = Entry(labelframe_setup, textvariable=name_datum)
    nameEntry.grid(row=4, column=0)
    playerbutton = Button(labelframe_setup, text="Submit", command=nameGet)
    playerbutton.grid(row=5, column=0)
    playerbutton.config(state=DISABLED)

    # Widgets for acquiring the whether players want a vowel or consonant, and will run the functions 'vowel_letter' and 'consonant_letter' respectively
    letters_buttonVowel = ttk.Button(labelframe_choose, text="Vowel", command=vowel_letter)
    letters_buttonVowel.grid(row=2, column=0, columnspan=9, sticky="WE", padx=100)
    letters_buttonConsonant = ttk.Button(labelframe_choose, text="Consonant", command=consonant_letter)
    letters_buttonConsonant.grid(row=3, column=0, columnspan=9, sticky="WE", padx=100)

    # This is an entrybox and submit button combo which will run the function 'declareLetters', which stores the length of the words in as a variable called length_word
    number_declare = IntVar()
    number_declare.set("")
    number_entry = Entry(labelframe_length, textvariable=number_declare)
    number_entry.grid(row=6, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
    number_button = Button(labelframe_length, text="Submit", command=declareLetters, bg="red", activebackground="lawngreen")
    number_button.grid(row=7, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
    number_button.config(state=DISABLED)

def NormalDel():
    # Used global here to define these lists, didn't use return because it won't be transferred to the other function of this level.
    # As in these variables are staying in this function 'NormalDel' and won't leave it
    global length_list
    global word_list
    global cd_list
    global final_words
    global bad_words
    global legit_words
    global score_list

    label_Game.grid_remove()
    player_list = []

    
    # Creates different label frames for each different subset
    labelframe_choose = LabelFrame(root, text="Choose")
    
    labelframe_word = LabelFrame(labelframe_choose, text="Word")
    labelframe_word.grid_remove()

    labelframe_length = LabelFrame(labelframe_choose, text="Length")
    labelframe_length.grid(row=4, column=0) 

    labelframe_setup = LabelFrame(root, text="Setup")
    labelframe_setup.grid(row=0, column=0)

    labelframe_timer = LabelFrame(root, text="Timer")

    labelframe_score = LabelFrame(root, text="Score")
    labelframe_score.grid_remove()

    labelframe_letter = LabelFrame(root, text="Letter")
    labelframe_letter.grid(row=5, column=0)

    labelframe_finish = LabelFrame(root, text="End")

    labelframe_delete = LabelFrame(root, text="Elimination")

    # Declaring variabes
    root.v_position = 0
    root.counti = 0
    root.countz = 0
    root.x_position = 0
    root.countd = 1
    x_position = 0
    i_position = 0 
    y_position = 0
    length_list = []
    word_list = []
    cd_list = []
    final_words = []
    bad_words = []
    legit_words = []
    score_list = []
    player_legitList = []
    
    # 'waithere' is a function used as a timing system, where when it runs, the program pauses for 1 second
    def waithere():
        var = IntVar()
        root.after(1065, var.set, 1)
        root.wait_variable(var)
        
    # This will run when users want to stop playing and see who one
    def finish_game():
        # Removing specific frames that are don't need to be seen anymore
        labelframe_score.grid_remove()
        labelframe_letter.grid_remove()
        labelframe_timer.grid_remove()
        # Creating a frame for the following information
        labelframe_finish.grid(row=0, column=0)
        # Calculates the scores and who is the winner
        WPI = score_list.index(max(score_list))
        WP = max(score_list)
        if score_list.count(WP) == 1:
            win_label = Label(labelframe_finish, text='The winner of Countdown and the person is taking of the Countdown Teapot is... {}'.format(player_list[WPI]))
            win_label.grid(row=0, column=0)
        #If there is a tie will print all players that have tied 
        else:
            # Counts how many people have the same score
            Tie_count = score_list.count(WP)
            # Prints winners
            winTie_label = Label(labelframe_finish, text='It was a {} way tie between.....'.format(Tie_count))
            winTie_label.grid(row=0, column=0)
            for i in range(playern):
                player_winner = StringVar()
                player_winner.set(player_list[i])
                if (score_list[i]) == WP:
                    winPlayer_label = Label(labelframe_finish, textvariable=player_winner)
                    winPlayer_label.grid(row=i+1, column=0)

    # When players ask for another game, all variables need to be reset
    def reset():
        global i_position
        global x_position
        global playern
        
        # Resets all variables
        y_position = 0
        x_position = 0
        i_position = 0
        root.v_position = 0
        root.counti = 0
        root.countz = 0
        root.x_position = 0
        # Rebind enter key to the 'number button'
        root.bind('<Return>', lambda event=None: number_button.invoke())


        # Destroying labels, clearing lists, and revealing or hiding frames again ready for the next game
        for widget in labelframe_letter.winfo_children():
            widget.destroy()

        for widget in labelframe_score.winfo_children():
            widget.destroy()
        cd_list.clear()
        final_words.clear()
        legit_words.clear()
        word_list.clear()
        length_list.clear()
        bad_words.clear()
        DictioneryConerLabel.destroy()
        labelframe_word.grid_remove()
        labelframe_length.grid(row=4, column=0)
        labelframe_score.grid_remove()
        labelframe_timer.grid_remove()
        labelframe_choose.grid(row=4, column=0)
        labelframe_delete.grid(row=0, column=0)

        # This is an intermediate step using a variable to be equal to the 'printword_list' as in that function there is a return variable is a parameter, meaning that now
        # this variable is now equal to that returned variable
        funcVar = printword_list()
        

        # Forming a list for the last_place players
        randomDelete = []

        # Making a copy and then sorting that list in terms of its length
        legit_wordsV = list(funcVar)
        sortedwords = sorted(legit_wordsV,key = len)
        shortest_word = sortedwords[0]

        # Goes through the legit_words and appends the smallest word(s) to the random_delete list
        for q in range(len(legit_wordsV)):
            if len(legit_wordsV[q]) == len(shortest_word):
                randomDelete.append(q)
                
        # A var integer randomly assinged a value from 1-5
        varRandom = random.randint(1,5)

        # If that var was 1 or 2, then the lowest scoring person is getting eliminated. If it is a tie, then it will randomly choose a player
        if varRandom == 2 or varRandom == 1:
            nDelete = random.choice(randomDelete) 
            deleteLabel = Label(labelframe_delete, text='The person getting eliminated is {}'.format(player_list[nDelete]))
            deleteLabel.grid(row=0, column=0)
            # This player needs to be outed from the list as they are no longer playing
            player_list.pop(nDelete)
            # As well as the total number of people player has now decreased by one
            playern = playern - 1
        else:
            # If the integer was not 1 or 2, then no one is eliminated
            nullDelete = Label(labelframe_delete, text='No one is getting eliminated this round')
            nullDelete.grid(row=0, column=0)


        # Sets the label to player 1 if the original player 1 was eliminated
        letterDerive = Label(labelframe_length, text="How long was your word {}".format(player_list[0]))
        letterDerive.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
        
        # Waits 3 seconds before destorying the label with the elimination information
        for i in range(3):
            waithere()
        for widget in labelframe_delete.winfo_children():
            widget.destroy()
        labelframe_delete.grid_remove()

        
        # If there is only one person remaining that player has automatically won
        if playern == 1:
            labelframe_score.grid_remove()
            labelframe_letter.grid_remove()
            labelframe_timer.grid_remove()
            labelframe_choose.grid_remove()
            labelframe_finish.grid(row=0, column=0)
            win_label = Label(labelframe_finish, text='The winner of Countdown and the person is taking of the Countdown Teapot is... {}'.format(player_list[0]))
            win_label.grid(row=0, column=0)

        # Now these two lists need to be cleared as they are now no longer needed
        player_legitList.clear()
        randomDelete.clear()
        # Normalising buttons only after the 3 second timer has elapsed
        letters_buttonVowel.config(state=NORMAL)
        letters_buttonConsonant.config(state=NORMAL)
        

    # This function is run when players input the amount of people playing
    # This has error prevention in mind as it won't allow anything other than a positive integer greater than 0
    # If this was the case it will show an error message and prevent them from continuing
    # Also if they input a number greater than 10, it will ask them to confirm 
    def playernumber():
        global playern
        # Attempts to get the value for playern
        try:
            playern = player_number.get()
        # If there is an error, let players now and allow to reinput
        except:
            messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
            player_number.set("")
        # If this isn't the case: continue
        else:

            # The following tests if the number is a number greater than 1 and is less than 10
            if playern < 2:
                messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number greater than 1")
                player_number.set("")


            else:
                if playern > 10:
                    MsgBox = messagebox.askquestion ('Are you sure', 'You have inputted a number more than 10, would you like to continue?',icon = 'warning')
                    if MsgBox == 'no':
                       messagebox.showinfo('Return','You will now return to the application screen')
                       player_number.set("")
                    else:
                        player_number.set("")
                        root.bind("<Return>", lambda e: None)
                        root.bind('<Return>', lambda event=None: playerbutton.invoke())
                        player_button.config(state=DISABLED)
                        playerbutton.config(state=NORMAL)
                        name_label = Label(labelframe_setup, text="What is player 1's name?")
                        name_label.grid(row=3, column=0)
                        return playern
                else:
                    player_number.set("")
                    root.bind("<Return>", lambda e: None)
                    root.bind('<Return>', lambda event=None: playerbutton.invoke())
                    player_button.config(state=DISABLED)
                    playerbutton.config(state=NORMAL)
                    name_label = Label(labelframe_setup, text="What is player 1's name?")
                    name_label.grid(row=3, column=0)
                
                return playern

    # Function to get all the names of each players and store them into a list
    def nameGet():
        
        name_label = Label(labelframe_setup, text="What is player {}'s name?".format(root.countd+1))
        name_label.grid(row=3, column=0)
        
        player_name = name_datum.get()
        name_datum.set("")
        player_list.append(player_name)
        if len(player_list) == playern:

            # Unbinds and binds the return key to the new function, to ensure no overlapping
            # Binds 'c' and 'v' for consonant and vowel button functions
            root.bind("<Return>", lambda e: None)
            root.bind('<Return>', lambda event=None: number_button.invoke())
            root.bind('c', lambda event=None: letters_buttonConsonant.invoke())
            root.bind('v', lambda event=None: letters_buttonVowel.invoke())
            labelframe_setup.grid_remove()
            labelframe_choose.grid(row=4, column=0)
            for i in range(playern):
                score_list.append(0)

        root.countd +=1
        return player_list

    # Function to increase the var root.v_position
    # Doesn't need global because it is defined inside the actual root program
    def increaseI():
        root.v_position +=1
        return root.v_position

    # This is for the program to print whoever is first in the list, incase that the original player 1 was eliminated
    def player1print():
        letterDerive = Label(labelframe_length, text="How long was your word {}".format(player_list[0]))
        letterDerive.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)

    # A function for later that checks the word and adds it to a list if legit and correct 
    def wordCheck(word, length_word):
        if word in final_words:
            if len(word) == length_word:
                legit_words.append(word)
            else:
                # Appends nothing because their true word length is now 0, as the player's word was not valid
                legit_words.append('')
        else:
            legit_words.append('')

    

    # This function is at the end of the game, where it is called after the final person inputs their word
    # It will create labels that have the information regarding the scores or each player, and the longest word possible, as well as a button if people want to have another game
    def funcscore():
        global DictioneryConerLabel

        # Removes specific frames as they are no longer need
        labelframe_choose.grid_remove()
        labelframe_score.grid(row=0, column=0)

        # Copying specific lists ready to manipulate them and then compare against the original
        length_listV = list(length_list)
        legit_wordsV = list(legit_words)
        sortedwords = sorted(legit_wordsV,key = len)
        Long_word = sortedwords[-1]
        LW_length = len(Long_word)
        for y in range(playern):
            if len(legit_words[y]) == len(Long_word):
                score_list[y] = score_list[y] + LW_length

        scoreLabel = Label(labelframe_score, text="The scores at the moment are...")
        scoreLabel.grid(row=0, column=0, padx=50, pady=20)
        
        # Displays the relevant information regarding scores, and the longest word
        DictioneryConerLabel = Label(labelframe_score, text="The longest word we found in Dictionery Corner was {}".format(longestWord))
        DictioneryConerLabel.grid(row=playern+1, column=0, pady=30)

        for i in range(playern):
            scoreLabel = Label(labelframe_score, text="Player {} has {} points".format(i+1, score_list[i]))
            scoreLabel.grid(row=i+1, column=0)
            
        # Creates a button for people to press if which will run the function 'reset', which resets all variables and lists, allowing for another game to be played
        reset_button = ttk.Button(labelframe_score, text="Replay", command=reset)
        reset_button.grid(row=playern+2, column=0)

        # Creates a button for people to press if which will run the function 'finish_game', which causes the game to stop and prints the winner(s)
        finish_button = ttk.Button(labelframe_score, text="Finish", command=finish_game)
        finish_button.grid(row=playern+3, column=0)

    # This function is used to return the var player_legitList
    # Once it is called the var can be used in another function
    def printword_list():
        for word in legit_words:
            player_legitList.append(word)
        return player_legitList
      
    # This will run the function to test the words with the variables of the length of the word and the word itself
    # It returns the x_position as this will be updated again and again
    def funcwordList():
        global length_list
        # Gets the players' words and then adds them to a list
        player_word = VarEntry_word.get()
        player_wordLower = player_word.lower()
        word_list.append(player_wordLower)
        VarEntry_word.set("")
        # Runs the function to check all the words
        wordCheck(word_list[root.x_position], length_list[root.x_position])
        root.x_position = root.x_position + 1
        # If everyone has inputted their words, the next part of the code can run
        if len(legit_words) == playern:
            # Unbinds everything that the return key was binded to, ready for this key to be rebinded to another
            root.bind("<Return>", lambda e: None)
            printword_list()
            funcscore()
        # If not everyone has inputted their words, it will ask the next person   
        else:
            root.counti +=1
            wordDerive2 = Label(labelframe_word, text="What was your word {}".format(player_list[root.counti]))
            wordDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
        return root.x_position
        return root.counti

    # Function to get all the words of the players 
    def grabWord():
        global VarEntry_word

        # Unbinds everything that the return key was binded to, ready for this key to be rebinded to another
        root.bind("<Return>", lambda e: None)
        # Hides the previous frame and reveals the 'word' frame
        labelframe_length.grid_remove()
        labelframe_word.grid(row=4, column=0)
        #Prompts users so that they know what to input
        wordDerive = Label(labelframe_word, text="What was your word {}".format(player_list[0]))
        wordDerive.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
              
        VarEntry_word = StringVar()
        VarEntry_word.set("")
        wordEntry = Entry(labelframe_word, textvariable=VarEntry_word)
        wordEntry.grid(row=6, column=0, columnspan=9, sticky="WE", padx=100,pady=10)

        wordEntryButton = Button(labelframe_word, text="Submit", command=funcwordList, bg="red", activebackground="lawngreen")
        wordEntryButton.grid(row=7, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
        root.bind('<Return>', lambda event=None: wordEntryButton.invoke())
        return VarEntry_word
      
    # Code that gets the lengths of the player's words and tests it to see if it is a positive integer greater than 1
    def declareLetters():
        if root.v_position == playern-1:
            root.v_position = 0
        # Built in error prevention
        try:
            length_word = number_declare.get()
        except:
            messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
            number_declare.set("")
        else:
            # Ensures that negative values were excluded
            if length_word < 1:
                messagebox.showerror("Error", "Oops, didn't quite get that \n Please input a valid number")
                player_number.set("")
                number_declare.set("")
            else:
                # If number is greater than 9, code will assume that this was a misinput, and there are only 9 letters so the code will ask for a confirmation
                if length_word > 9:
                    MsgBox = messagebox.askquestion ('Are you sure', 'You have inputted a number more than 9, would you like to continue?',icon = 'warning')
                    if MsgBox == 'no':
                       messagebox.showinfo('Return','You will now return to the application screen')
                       number_declare.set("")
                    else:
                        length_list.append(length_word)
                        number_declare.set("")
                        increaseI()
                        letterDerive2 = Label(labelframe_length, text="How long was your word {}".format(player_list[root.v_position]))
                        letterDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
                else:
                    length_list.append(length_word)
                    number_declare.set("")
                    increaseI()
                    letterDerive2 = Label(labelframe_length, text="How long was your word {}".format(player_list[root.v_position]))
                    letterDerive2.grid(row=5, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
                
        if len(length_list) == playern:
            grabWord()


                    
    def disButton():
        global longestWord
        global list_var
        player1print()

        # Enabling button for this part of the code
        number_button.config(state=NORMAL)

        # This is the imported library to play the downloaded song of countdown
        winsound.PlaySound('CountdownSound', winsound.SND_ASYNC)

        # This code is important prevents error later in the code if the buttons are disabled to ensure that no more than 9 letters are generated
        letters_buttonVowel.config(state=DISABLED)
        letters_buttonConsonant.config(state=DISABLED)
        
        # Creates a list with ALL words that contain only the 9 letters (duaplicates are included)
        cd_set = set(cd_list)
        for word in cd_words.splitlines():
            word_letters = set(word)
            if word_letters <= cd_set:
                final_words.append(word)
            else:
                pass

        # Uses the 'count' function as a test for each word and adds to a valid word list
        for word in final_words:
            for i in range(9):
                if cd_list[i] in word:
                    count = word.count(cd_list[i])
                    # If there are more letters in the word than in the list, then it cannot be a valid word
                    if count > cd_list.count(cd_list[i]) and word not in bad_words:
                        bad_words.append(word)
                    else:
                        pass
                else:
                    pass
        for word in bad_words:
            final_words.remove(word)
            
        # Finds the longest possible word using the letters by going through the list of all possible words
        longestWord = ""
        for posword in final_words:
            if len(posword) > len(longestWord):
                longestWord = posword

        # This is timer which uses the a for loop with range of 30 to print a label with no text but a background of blue
        labelframe_timer.grid(row=8, column=0)
        # The two '|' are used as the start and stop parts to players can visually see when its going to end
        createLabelstart = Label(labelframe_timer, text="|")
        createLabelstart.grid(row=0, column=0)
        for i in range(1,31):
            copylabel = Label(labelframe_timer)
            copylabel.grid(row=0, column=i)
            if i == 30:
                createLabelend = Label(labelframe_timer, text="|")
                createLabelend.grid(row=0, column=i)
        # Using the function of 'waitthere' which waits for 1 second, the timer will acurately time for 30 seconds
        for i in range(1,30):
            timeLabel = Label(labelframe_timer, text="", bg='blue')
            timeLabel.grid(row=0, column=i)
            waithere()

        # returns the var longestWord as another function then takes this and then prints later on in the game
        return longestWord
    
     # The buttons to generate vowels and consonant when players press them
    def vowel_letter():
        global i_position
        final_vowel = random.choice(possible_vowels)
        cd_list.append(final_vowel)
        vowel_datum = StringVar()
        vowel_datum.set(final_vowel.capitalize())
        label_vowel = Label(labelframe_letter, textvariable=vowel_datum)
        label_vowel.config(font=("Courier", 20))
        label_vowel.grid(row=4, column=i_position,columnspan=1)
        # Once nine letters have been chosen the next part of the code will run
        i_position = i_position + 1
        if i_position == 9:
            disButton()
    def consonant_letter():
        global i_position
        final_consanent = random.choice(possible_consanents)
        cd_list.append(final_consanent)
        consanent_datum = StringVar()
        consanent_datum.set(final_consanent.capitalize())
        label_consanent = Label(labelframe_letter, textvariable=consanent_datum)
        label_consanent.config(font=("Courier", 20))
        label_consanent.grid(row=4, column=i_position,columnspan=1)
        # Once nine letters have been chosen the next part of the code will run
        i_position = i_position + 1
        if len(cd_list) == 9:
            disButton()
        
    # Label to pose the question that will be visible to the players
    n_players = Label(labelframe_setup, text='How many people are playing? (minimum 2)')
    n_players.grid(row=0, column=0)

    # Widgets for acquiring the number of people playing
    player_number = IntVar()
    player_number.set("")
    playerEntry = Entry(labelframe_setup, textvariable=player_number)
    playerEntry.grid(row=1, column=0)
    # Run function 'playernumber'
    player_button = ttk.Button(labelframe_setup, text="Submit", command=playernumber)
    player_button.grid(row=2, column=0, padx=100,pady=10)
    root.bind('<Return>', lambda event=None: player_button.invoke())

    # An entry box and button combo to acquire the names of the people who are playing
    name_datum = StringVar()
    name_datum.set("")
    nameEntry = Entry(labelframe_setup, textvariable=name_datum)
    nameEntry.grid(row=4, column=0)
    # Run the function 'nameGet', getting the names of each player
    playerbutton = Button(labelframe_setup, text="Submit", command=nameGet)
    playerbutton.grid(row=5, column=0)
    playerbutton.config(state=DISABLED)

    # Widgets for acquiring the whether players want a vowel or consonant, and will run the functions 'vowel_letter' and 'consonant_letter' respectively
    letters_buttonVowel = ttk.Button(labelframe_choose, text="Vowel", command=vowel_letter)
    letters_buttonVowel.grid(row=2, column=0, columnspan=9, sticky="WE", padx=100)
    letters_buttonConsonant = ttk.Button(labelframe_choose, text="Consonant", command=consonant_letter)
    letters_buttonConsonant.grid(row=3, column=0, columnspan=9, sticky="WE", padx=100)

    # This is an entrybox and submit button combo for users to input the lengths of their words  
    number_declare = IntVar()
    number_declare.set("")
    number_entry = Entry(labelframe_length, textvariable=number_declare)
    number_entry.grid(row=6, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
    # Run the function 'declareLetters', which stores the length of the words in as a variable called length_word
    number_button = Button(labelframe_length, text="Submit", command=declareLetters, bg="red", activebackground="lawngreen")
    number_button.grid(row=7, column=0, columnspan=9, sticky="WE", padx=100,pady=10)
    number_button.config(state=DISABLED)


# This is what people see when they first start the game, allowing them to choose which game they want to play
label_Game = Frame(root)
label_Game.grid(row=0, column=0)
StartLabel = Label(label_Game, text="Choose which game you would like to play: ")
StartLabel.grid(row=0, column=0)
# Will trigger the normal part of the game
ButtonNor = ttk.Button(label_Game, text="Normal", command=Normalmain)
ButtonNor.grid(row=1, column=0)
# Will trigger the elimination round of countdown
ButtonDel = ttk.Button(label_Game, text="Elimination", command=NormalDel)
ButtonDel.grid(row=2, column=0)
i_position = 0
x_position = 0
# Runs the GUI
root.mainloop()
