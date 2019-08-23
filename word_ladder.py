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
            "If do not wish to exclude any words press ENTER \n" +
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
                print("Please ensure your excluded words only contain letters and are in the format stated.")
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
                  "If do not wish to include a word press ENTER\n\n" +
                  "Word to include: ")).replace(" ", "").lower()
        if include_word == "":
            print("No word provided to include in laddergram search, please wait...\n")
            return include_word
        elif len(include_word) == len(start) and len(include_word) == len(target):
            if not verify_input(include_word):
                print("Please enter a valid word only containing letters!!!")
                included_input()
            else:
                print("{} has been included in the laddergram search, please wait...\n".format(include_word))
                return include_word
                break
        elif not verify_input(include_word):
            print("Please enter a valid word only containing letters!")
        elif len(include_word) != len(start) or len(target):
            print("Please ensure your word to include is the same length as your start and target word!")


# Returns the number of letters and indexes that are the same
def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])


# Returns the result of each word iterated in the words list and searches through each word in that list to ensure that
# it doesn't exist in either the seen list or path list.
def build(pattern, words, seen, list):
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and
            word not in list]


# Main Function
def find(word, words, seen, target, path):
    list = []

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
lines = verify_dictionary_input().readlines()

while True:
    start = str(start_input())
    target = str(target_input())
    excluded_words = str(excluded_input())
    include_word = str(included_input())
    words = []

    for line in lines:
        # Removes any trailing characters from the dictionary from the right (removes spaces by default)
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

# Finds the start word to the word to include, then finds from the included word to target word
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

# Finds the start word to the target word
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
