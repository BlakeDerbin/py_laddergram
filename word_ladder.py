# imports python's regular expressions
import re


# Verifies the input of the dictionary file exists in the directory, then returns the opened file to the user.
# If the input has any errors IOError will catch them and print the error number and the description of the error.
# If an unexpected error that isn't caught by IOError occurs the code will print "Unexpected error, please try again."
def verify_dictionary_input():
    while True:
        try:
            fname = input("Enter dictionary name: ")
            open_dict = open(fname, "r")
            return open_dict
        except IOError as e:
            error_num, str_error = e.args
            print("Input Error ({0}): {1}".format(error_num, str_error))
        except:
            print("Unexpected error, please try again.")
            raise


def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])


def build(pattern, words, seen, list):
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and
            word not in list]


def find(word, words, seen, target, path):
    list = []
    for i in range(len(word)):
        list += build(word[:i] + "." + word[i + 1:], words, seen, list)
    if len(list) == 0:
        return False
    list = sorted([(same(w, target), w) for w in list])
    for (match, item) in list:
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


# Uses the function verify_dictionary_input to ensure the file input for the program is valid
lines = verify_dictionary_input().readlines()

# Verifies the start word by using regular expressions to iterate over the input step by step to ensure that the input
# only matches the letters from a - z in lowercase and uppercase, will continue until input is valid
while True:
    try:
        start = input("Enter start word: ")
        validate_word = re.findall(r'^[a-zA-Z]+$', start)
        if not validate_word:
            print("Please ensure the start word only contains letters!")
        else:
            break
    except ValueError:
        print("Please enter a valid start word!")

# Verifies the target word by using regular expressions to iterate over the input step by step to ensure that the input
# only matches the letters from a - z in lowercase and uppercase, will continue until input is valid
while True:
    try:
        target = input("Enter target word: ")
        validate_word = re.findall(r'^[a-zA-Z]+$', target)
        if not validate_word:
            print("Please ensure the target word only contains letters!")
        else:
            break
    except ValueError:
        print("Please enter a valid target word!")

while True:
    words = []
    for line in lines:
        word = line.rstrip()
        if len(word) == len(start):
            words.append(word)
    break

count = 0
path = [start]
seen = {start: True}
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")