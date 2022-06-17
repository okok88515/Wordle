from copy import deepcopy
from itertools import count
import sys
import random
from itertools import combinations

#modified from https://github.com/sjw269/Wordle-Solver/blob/main/wordle_solver.py

def badLetters(result, guess):
    """Finds incorrect letters in word"""
    bad_letters = []
    for i in range(0, 7):
        if result[i] == "0":
            bad_letters.append(guess[i])
    return bad_letters

def correctLetters(result, guess):
    """Finds fully correct letters in word"""
    correct_letters = []
    for i in range(0, 7):
        if result[i] == "1":
            correct_letters.append([guess[i], i])
    return correct_letters

def positionWrongLetters(result, guess):
    """Finds correct letters that are misplaced in word"""
    position_wrongLetters = []
    for i in range(0, 7):
        if result[i] == "2":
            position_wrongLetters.append([guess[i], i])
    return position_wrongLetters

def capitalWrongLetters(result, guess):
    """Finds correct letters that are misplaced in word"""
    capital_wrongLetters = []
    for i in range(0, 7):
        if result[i] == "3":
            capital_wrongLetters.append([guess[i], i])
    return capital_wrongLetters

def positionCapitalWrongLetters(result, guess):
    """Finds correct letters that are misplaced in word"""
    position_capital_wrongLetters = []
    for i in range(0, 7):
        if result[i] == "4":
            position_capital_wrongLetters.append([guess[i], i])
    return position_capital_wrongLetters


def word_remover(result, guess, possible_words):
    """Returns the list of words with incorrect possibilties removed"""
    bad_letters = badLetters(result, guess)
    correct_letters = correctLetters(result, guess)
    position_wrongLetters = positionWrongLetters(result, guess)
    capital_wrongLetters = capitalWrongLetters(result, guess)
    positionCapital_wrongLetters = positionCapitalWrongLetters(result, guess)
    good_letters = []
    for c in capital_wrongLetters:
        c[0] = c[0].swapcase()
        #c = ''.join(c)
        correct_letters.append(c)
    for pc in positionCapital_wrongLetters:
        #print(type(pc))
        pc[0] = pc[0].swapcase()
        #pc = ''.join(pc)
        position_wrongLetters.append(pc)
    for g in correct_letters:
        good_letters.append(g[0])
    for p in position_wrongLetters:
        good_letters.append(p[0])
    
    #print(bad_letters)
    #print(correct_letters)
    #print(partial_letters)
    #print(good_letters)
    acceptable_words1 = []
    #print(possible_words)
    for w in possible_words:
        check = 0
        for b in bad_letters:
            if b in w:
                if b in good_letters:
                    pass
                else:
                    check = 1
                    break
        if check == 0:
            acceptable_words1.append(w)
    #print(acceptable_words1)

    acceptable_words2 = []
    for w in acceptable_words1:
        check = 0
        for g in correct_letters:
            if w[g[1]] != g[0]:
                check = 1
                break
        if check == 0:
            acceptable_words2.append(w)
    #print(acceptable_words2)
    
    acceptable_words3 = []
    for w in acceptable_words2:
        check = 0
        for p in position_wrongLetters:
            #print(p[1])
            if w[p[1]] == p[0]:
                check = 1
                break
        if check == 0:
            acceptable_words3.append(w)
    #print(acceptable_words3)
    
    acceptable_words4 = []
    for w in acceptable_words3:
        check = 0
        for g in good_letters:
            if g not in w:
                check = 1
                break
        if check == 0:
            acceptable_words4.append(w)
    #print(acceptable_words4)

    acceptable_words5 = []
    for w in acceptable_words4:
        check = 0
        for b in bad_letters:
            if b in good_letters:
                if w.count(b) != good_letters.count(b):
                    check = 1
                    break
        if check == 0:
            acceptable_words5.append(w)
    #print(acceptable_words5)
    return acceptable_words5

def letterFreq(possible_words):
    """Finds frequencies of letters in each position"""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    arr = {}
    for c in alphabet:
        freq = [0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 7):
            for w in possible_words:
                if w[i] == c:
                    freq[i] += 1
        arr.update({c: freq})
    return arr

def wordScore(possible_words, frequencies):
    """Computes a score based off letter frequencies"""
    words = {}
    max_freq = [0, 0, 0, 0, 0, 0, 0]
    for c in frequencies:
        for i in range(0, 7):
            if max_freq[i] < frequencies[c][i]:
                max_freq[i] = frequencies[c][i]
    for w in possible_words:
        score = 1
        for i in range(0, 7):
            c = w[i]
            score *= 1 + (frequencies[c][i] - max_freq[i]) ** 2
        words.update({w: score})
        import numpy
        #score += numpy.random.uniform(0, 1)     
    return words

def bestWord(possible_words, frequencies):
    """Finds the best word"""
    max_score = 1000000000000000000     # start with a ridiculous score
    best_word = "words"     # start with a random word
    scores = wordScore(possible_words, frequencies)
    for w in possible_words:
        if scores[w] < max_score:
            max_score = scores[w]
            best_word = w
    return best_word

def wordleSolver(possible_words, answer, output_file):
    """Prompts you to solve Wordle"""
    print("Welcome to the Wordle Solver!")
    suggestion = bestWord(possible_words, letterFreq(possible_words))
    print("The suggested starting word is:", suggestion)
    #print(possible_words)
    #print("Enter your first guess:")
    #guess = input()
    guess = suggestion
    #print("Enter your first result:")
    result_o = compare2words_stage2(answer, guess)
    result = result_o.replace(",","")
    print("The result is:" + result_o)
    counter = 1
    path = output_file
    f = open(path, 'a')
    f.write(str(counter)+';')
    f.write(guess+';')
    f.write(result_o+';')
    f.close()
    while result != "1111111" :
        possible_words = word_remover(result, guess, possible_words)
        #print(possible_words)
        if len(possible_words) == 0:
            break
        suggestion = bestWord(possible_words, letterFreq(possible_words))
        print("The suggested word is:", suggestion)
        #print("Enter your next guess:")
        guess = suggestion
        #guess = input()
        #print("Enter your new result:")
        result_o = compare2words_stage2(answer, guess)
        result = result_o.replace(",","")
        print("The result is:" + result_o)
        counter += 1
            
        f = open(path, 'a')
        f.write('\n'+str(counter)+';')
        f.write(guess+';')
        f.write(result_o+';')
        f.close()
    if len(possible_words) == 0:
        print("Oh no! You made a mistake entering one of your results. Please try again.")
    else:
        f = open(path, 'a')
        f.write('\n'+str(counter)+'\n')
        f.close()
        print("Congratulations! We solved today's Wordle in", counter, "guesses.")


def compare2words_stage2(answer, guess):
    la = list(answer)
    lg = list(guess)
    results = [0] * len(la)
    matched = [0] * len(la)
    for i in range(len(lg)):
        if (lg[i]==la[i]):
            matched[i] = 1  # 1 for used
            results[i] = 1  # 1 for "A"
        elif (lg[i]==la[i].swapcase()):
            matched[i] = 1
            results[i] = 3
    for i in range(len(lg)):
        if (results[i]>0):
            continue
        for j in range(len(la)):
            if (matched[j]>0):
                continue
            if (lg[i]==la[j]):
                matched[j] = 1  # 1 for used
                results[i] = 2  # 2 for "B"
                break
    for i in range(len(lg)):
        if (results[i]>0):
            continue
        for j in range(len(la)):
            if (matched[j]>0):
                continue
            if(lg[i]==la[j].swapcase()):
                matched[j] = 1
                results[i] = 4
                break
            
    for i in range(len(results)):
        results[i] = str(results[i])
    results = ",".join(results)
    return results

# Examples:
guess = "sauce"    # a 5 letter word must be the input
result = "yywww"   # y - correct letter, wrong place; g - fully correct; w - wrong

words_in = sys.argv[1]

def tupleToNum(Tuple):
    line = ' '.join(map(str,Tuple))
    line = list(line.split(' '))
    return line

def combination():
    com_list = []
    for i in range(1, 8):
        com = combinations("0123456", i)
        for j in list(com):
            com_list.append(tupleToNum(j))
    return com_list


def give_answerset():
    result = []
    com_list = combination()
    with open(words_in, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            result.append(line)
            list1 = []
            #line1 = '%s' % line  
            for com in com_list:
                line1 = line
                for i in com:
                    i = int(i)
    #                print(i)
                    line1 = list(line1)
                    line1[i] = line1[i].upper()
                line1 = ''.join(line1)
                result.append(line1)
                #line = list(line)
                #line[i] = line[i].upper()
                #line = ''.join(line)
    f.close()
    possible_words = result
    #print(possible_words)
    return possible_words
    
# print(possible_words)
# List of possible words


#將測試檔案輸入，產生猜測過程及結果
def wordleSolver_1(test_file, output_file):
    test = test_file
    t = open(test, 'r')
    path = output_file
    f = open(path, 'w')
    f.close()
    answerset = give_answerset()
    for line in t: 
        line = line.strip()
        f = open(path, 'a')
        f.write(line+'\n')
        f.close()
        possible_words = deepcopy(answerset)
        wordleSolver(possible_words, line, output_file)
    t.close()
    
file_in = sys.argv[2]
file_out = sys.argv[3]

if len(sys.argv) != 4:
    print("Error")
    sys.exit(0)
else:
    wordleSolver_1(file_in, file_out)



#python team27.py wordle-answers-alphabetical.txt tests.txt team27_first_.txt

#python team27.py wordle-answers-alphabetical.txt wordle-answers-alphabetical_1.txt team27_first_.txt

#python team27_game2.py game2list1.txt test_game2.txt team27_game2_first.txt