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


# Verifies that an input is lowercase and between only contains letters
def verify_input(word_input):
    return re.findall(r'^[a-z]+$', str(word_input))


# Allows the user to provide a list of words to exclude from the ladder gram, if nothing is entered the program will
# proceed with the ladder gram, if an input is detected the program will exclude the words if they're in the dictionary.
def excluded_input(exclude_words):
    while True:
        if exclude_words == "":
            print("No excluded words provided, please wait...\n")
            break
        else:
            excluded_list = exclude_words.split(',')
            print("Excluded words accepted, please wait...\n")
            return excluded_list


# Processes the users input for the included word in the search
# Verifies that the input matches the length of the start and target word
# Then checks if the word contains letters, if it does the function will return the word the include in the search
# If the input doesn't contain letters the function will return an error message
# If the length of the input doesn't match the start and target word, the function will return an error message
def included_input():
    while True:
            include_word = str(input("Enter word to include in laddergram: ")).replace(" ", "").lower()
            if include_word == "":
                print("No word provided to include in laddergram, please wait...\n")
                return include_word
            elif len(include_word) == len(start) and len(include_word) == len(target):
                if not verify_input(include_word):
                    print("Please enter a valid word only containing letters!!!")
                    included_input()
                else:
                    print("{} has been included in the laddergram, please wait...\n".format(include_word))
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

    # Searches the list for
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

# Verifies the start word by using regular expressions to iterate over the input step by step to ensure that the input
# only matches the letters from a - z in lowercase, will convert users input to lowercase if uppercase is used.
while True:
    try:
        start = input("Enter your start word: ").lower()
        validate_word = verify_input(start)
        if not validate_word:
            print("Please ensure that your start word only contains letters!")
        else:
            break
    except ValueError:
        print("Please enter a valid start word!")

# Verifies the target word by using regular expressions to iterate over the input step by step to ensure that the input
# only matches the letters from a - z in lowercase, will convert users input to lowercase if uppercase is used.
while True:
    try:
        target = input("Enter your target word: ").lower()
        validate_word = verify_input(target)
        if not validate_word:
            print("Please ensure that your target word only contains letters!")
        else:
            break
    except ValueError:
        print("Please enter a valid target word!")

while True:
    # User supplies a list of excluded words, spaces between commas are replaced with no space & converted to lowercase
    user_list = str(input(
        "\nEnter a list of words that you do not wish to be included in the laddergram\n" +
        "If do not wish to exclude any words press ENTER \n" +
        "An example of how to input excluded words: hold, mold, weld, sell\n\n" +
        "Excluded words: ")).replace(" ", "").lower()
    excluded_words = str(excluded_input(user_list))
    include_word = included_input()

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
    while True:
        if find(start, words, seen, include_word, path):
            path.append(include_word)
            if find(include_word, words, seen, target, path):
                path.append(target)
        # Print formatting of final output, mainly formats the list into a more readable format
        print("{} steps taken to transform {} to {} while including {} in the search.\nWords used in laddergram: {}"
              .format(len(path) - 1, str(start), str(target), str(include_word), str(path)[1:-1].replace("'", "")))
        break
    else:
        print("No viable paths found to convert {} to {} with {} included in the search.".format(start, target, include_word))

# Finds the start word to the target word
if include_word == "":
    while True:
        if find(start, words, seen, target, path):
                path.append(target)
        # Print formatting of final output, mainly formats the list into a more readable format
        print("{} steps taken to transform {} to {}.\nWords used in laddergram: {}"
              .format(len(path) - 1, str(start), str(target), str(path)[1:-1].replace("'", "")))
        break
    else:
        print("No viable paths found to convert {} to {}".format(start, target))