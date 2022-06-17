from itertools import count
import sys

#modified from https://github.com/sjw269/Wordle-Solver/blob/main/wordle_solver.py

def badLetters(result, guess):
    """Finds incorrect letters in word"""
    bad_letters = []
    for i in range(0, 5):
        if result[i] == "0":
            bad_letters.append(guess[i])
    return bad_letters

def partialLetters(result, guess):
    """Finds correct letters that are misplaced in word"""
    partial_letters = []
    for i in range(0, 5):
        if result[i] == "2":
            partial_letters.append([guess[i], i])
    return partial_letters

def correctLetters(result, guess):
    """Finds fully correct letters in word"""
    correct_letters = []
    for i in range(0, 5):
        if result[i] == "1":
            correct_letters.append([guess[i], i])
    return correct_letters

def word_remover(result, guess, possible_words):
    """Returns the list of words with incorrect possibilties removed"""
    bad_letters = badLetters(result, guess)
    correct_letters = correctLetters(result, guess)
    partial_letters = partialLetters(result, guess)
    good_letters = []
    for g in correct_letters:
        good_letters.append(g[0])
    for p in partial_letters:
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
        for p in partial_letters:
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
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    arr = {}
    for c in alphabet:
        freq = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            for w in possible_words:
                if w[i] == c:
                    freq[i] += 1
        arr.update({c: freq})
    return arr

def wordScore(possible_words, frequencies):
    """Computes a score based off letter frequencies"""
    words = {}
    max_freq = [0, 0, 0, 0, 0]
    for c in frequencies:
        for i in range(0, 5):
            if max_freq[i] < frequencies[c][i]:
                max_freq[i] = frequencies[c][i]
    for w in possible_words:
        score = 1
        for i in range(0, 5):
            c = w[i]
            score *= 1 + (frequencies[c][i] - max_freq[i]) ** 2
        words.update({w: score})
        import numpy
        #score += numpy.random.uniform(0, 1)     # this will increase expectation from 2.95 to 3.23, but is technically fairer
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
    #from datetime import date
    #diff = (date.today() - date(2021, 6, 19)).days
    #del possible_words[0: diff]
    #print(possible_words)
    #print("Enter your first guess:")
    #guess = input()
    guess = suggestion
    #print("Enter your first result:")
    result_o = getResult2(answer, guess)
    result = result_o.replace(",","")
    print("The result is:" + result_o)
    counter = 1
    path = output_file
    f = open(path, 'a')
    f.write(str(counter)+';')
    f.write(guess+';')
    f.write(result_o+';')
    f.close()
    while result != "11111" :
            
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
        result_o = getResult2(answer, guess)
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

def getResult(answer, guess):
    result = [0,0,0,0,0]
    words = []
    for i in range(0, 5):
        words.append(answer[i])
    for i in range(0, 5):
        if guess[i] == answer[i]:
            result[i] = '1'
            words[i] = ""
    for i in range(0,5):
        if result[i] == '1':
            continue
        else:    
            for j in range(0, 5):
                if (guess[i] == answer[j]) and (guess[i] in words):
                    result[i] = '2'
                    break
            else:
                result[i] = '0'
    result = ",".join(result)
    return result

def getResult2(answer, guess):
    la = list(answer)
    lg = list(guess)
    results = [0] * len(la)
    matched = [0] * len(la)
    for i in range(len(lg)):
        if (lg[i]==la[i]):
            matched[i] = 1  # 1 for used
            results[i] = 1  # 1 for "A"
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
    for i in range(len(results)):
        results[i] = str(results[i])
    results = ",".join(results)
    return results

# Examples:
guess = "sauce"    # a 5 letter word must be the input
result = "yywww"   # y - correct letter, wrong place; g - fully correct; w - wrong

words_in = sys.argv[1]
def give_answerset():
    result = []
    with open(words_in, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            result.append(line)
    f.close()
    possible_words = result
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
    for line in t: 
        line = line.strip()
        f = open(path, 'a')
        f.write(line+'\n')
        f.close()
        possible_words = give_answerset()
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

#python Wordle_basic_frequency.py wordle-answers-alphabetical.txt wordle-answers-alphabetical_1.txt team27_first_.txt