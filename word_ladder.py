# imports python's regular expressions
import re


# Verifies the input of the dictionary file exists in the directory, then returns the opened file to the user.
# If the input has any errors IOError will catch them and print the error number and the description of the error.
# If an unexpected error that isn't caught by IOError occurs the code will print "Unexpected error, please try again."
def verify_dictionary_input():
    while True:
        try:
            fname = input("Enter your dictionary file name: ")
            open_dict = open(fname, "r")
            return open_dict
        except IOError as e:
            error_num, str_error = e.args
            print("Input Error ({}): {}".format(error_num, str_error))
        except:
            print("Unexpected error, please try again.")
            raise


# Verifies input by using regular expressions to iterate over the input step by step to ensure
# that the input only matches the letters from a - z in lowercase,
def verify_input(word_input):
    return re.findall(r'^[a-z]+$', str(word_input))


# Checks if the start word input is not nothing and verifies the input using the verify_input function.
def start_input():
    while True:
        start = str(input("Enter your start word: ")).replace(" ", "").lower()
        if start == "":
            print("Please enter a start word!")
        elif not verify_input(start):
            print("Please enter a valid start word only containing letters!")
        else:
            return start


# Checks if the target word input is empty, prints error message if it is
# Checks if the length of the target word matches length of start word, if true then checks if it contains only letters
# If it only contains letters the program returns the target word
# If the length of the target word doesn't match the length of the start word an error message is printed
def target_input():
    while True:
        target = str(input("Enter your target word: ")).replace(" ", "").lower()
        if target == "":
            print("Please enter a target word!")
        elif len(target) == len(start) and target:
            if not verify_input(target):
                print("Please enter a valid target word only containing letters!")
            else:
                return target
        elif len(target) != len(start):
            print("Please ensure your target word is the same length as your start word")


# Takes user input of excluded words for the ladder gram, if nothing is entered the program will continue
# If an input is entered it is checked that it is a valid input only containing letters.
# If the input isn't valid an error message will occur
def excluded_input():
    while True:
        # User inputs list of excluded words, spaces between commas are replaced with no space & converted to lowercase
        exclude_words = str(input(
            "\nEnter a list of words that you do not wish to be included in the laddergram\n" +
            "If you do not wish to exclude any words press ENTER \n" +
            "An example of how to input excluded words: hold, mold, weld, sell\n\n" +
            "Excluded words: ")).replace(" ", "").lower()

        if exclude_words == "":
            print("No words provided to exclude from the laddergram search\n")
            break
        else:
            excluded_list = exclude_words.split(',')
            # To check if the list only contains letters, converts to string and removes all list characters.
            check_list = str(excluded_list)[1:-1].replace("'", "", ).replace(",", "").replace(" ", "")
            if not verify_input(check_list):
                print("Please ensure your excluded words only contain letters and are in the format stated.\n")
            else:
                print("{} has been excluded from the laddergram search\n".format(
                    str(excluded_list)[1:-1].replace("'", "", )))
                return excluded_list


# Processes the users input for the included word in the search
# Verifies that the input matches the length of the start and target word
# Then checks if the word contains letters, if it does the function will return the word the include in the search
# If the input doesn't contain letters the function will return an error message
# If the length of the input doesn't match the start and target word, the function will return an error message
def included_input():
    while True:
        include_word = str(
            input("Enter a word to include in the laddergram search from {} to {}\n".format(start, target) +
                  "If you do not wish to include a word press ENTER\n\n" +
                  "Word to include: ")).replace(" ", "").lower()
        if include_word == "":
            print("No word provided to include in laddergram search, please wait...\n")
            return include_word
        elif len(include_word) == len(start) and len(include_word) == len(target):
            if not verify_input(include_word):
                print("Please enter a valid word only containing letters!\n")
                included_input()
            else:
                print("{} has been included in the laddergram search, please wait...\n".format(include_word))
                return include_word
                break
        elif not verify_input(include_word):
            print("Please enter a valid word only containing letters!\n")
        elif len(include_word) != len(start) or len(target):
            print("Please ensure your word to include is the same length as your start or target word!\n")


# Checks if the word is the same
# Uses for loop to count the number of times word and target match, if they match then the count is increased.
# Final return value is the count of how many times item and target matched
def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])


# Returns the result of each word iterated in the words list and seen list
# It will use a regular expression search with a pattern to verify that word doesn't exist in either seen list or list
# word variable is returned
def build(pattern, words, seen, list):
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and
            word not in list]


# Main function:
# Creates a list using the build function, will include all variations that match the length of the start word
# List is the sorted based on the number of times start and target words matched in the dictionary
# For loop detects if the start word matches the length of the target word, if it matches the target word is appended to path
# Nested for loop detects any words with the letters x, y, z and removes them from the list
# 2nd for loop runs find function again and true, will then append each match, and item to the path list

def find(word, words, seen, target, path):
    list = []

    # Iterates through all words in the dictionary that match the length of the start word and stores as list variable
    for i in range(len(word)):
        list += build(word[:i] + "." + word[i + 1:], words, seen, list)
    if len(list) == 0:
        return False

    # List is sorted in descending order rather than ascending, offering shortest path
    list = sorted([(same(w, target), w) for w in list], reverse=True)

    for (match, item) in list:
        # For loop removes uncommon letters from list, improves search efficiency by excluding words containing x,y,z
        for letters in ['x', 'y', 'z']:
            if letters in item:
                list.remove((match, item))

        if match >= len(target) - 1:
            if match == len(target) - 1:
                path.append(item)
            return True
        seen[item] = True

    for (match, item) in list:
        path.append(item)
        if find(item, words, seen, target, path):
            return True
        path.pop()


# Uses function verify_dictionary_input to ensure file input for the program is valid, then reads the dictionary lines
# and stores the lines as a list in the variable lines
lines = verify_dictionary_input().readlines()

while True:
    start = str(start_input())
    target = str(target_input())
    excluded_words = str(excluded_input())
    include_word = str(included_input())
    words = []

    for line in lines:
        # Removes any spaces from the lines variable from the right
        word = line.rstrip()

        # Program continues without excluded words if string is empty i.e. user presses enter key
        if excluded_words == "":
            # Checks dictionary word matches the length of the start word. New list is formed with words the same length
            if len(word) == len(start) and word:
                words.append(word)

        # If the user provides the excluded words the program will exclude them from the search
        else:
            # Same as above but will not include excluded words in the new list built
            if len(word) == len(start) and word not in excluded_words:
                words.append(word)
    break

count = 0
path = [start]
seen = {start: True}

# Uses the start word to find until the include word, then uses the include word to find until the target word to perform the laddergram search
if include_word != "":
    try:
        if find(start, words, seen, include_word, path):
            path.append(include_word)
            if find(include_word, words, seen, target, path):
                path.append(target)
                # Print formatting of final output, mainly formats the list into a more readable format
                print("{} steps taken to transform {} to {} while including {} in the search.\nWords used in laddergram: {}"
                      .format(len(path) - 1, str(start), str(target), str(include_word), str(path)[1:-1].replace("'", "")))
            else:
                print("No viable paths found to convert {} to {} with {} included in the search.".format(start, target,
                                                                                                         include_word))
    except ValueError:
        print("A value error has occurred!")

# Uses the start word to the target word to perform the laddergram search
elif include_word == "":
    try:
        if find(start, words, seen, target, path):
            path.append(target)
            # Print formatting of final output, mainly formats the list into a more readable format
            print("{} steps taken to transform {} to {}.\nWords used in laddergram: {}"
                  .format(len(path) - 1, str(start), str(target), str(path)[1:-1].replace("'", "")))
        else:
            print("No viable paths found to convert {} to {}".format(start, target))
    except ValueError:
        print("A value error has occurred!")
