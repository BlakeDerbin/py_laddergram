import word_ladder
import unittest


class test_word_ladder_functions(unittest.TestCase):

    # Checks incorrect file as the dictionary input
    def test_verify_dictionary_input(self):
      self.assertEqual(word_ladder.verify_dictionary_input("test.txt"), None, "Input Error ({}): {}")


    # Checks if a number returns nothing
    # Checks if a word input returns the same
    def test_verify_input(self):
      self.assertFalse(word_ladder.verify_input(64654), None)
      self.assertTrue(word_ladder.verify_input("word"), "word")


    # Checks if a word is returned in the same format as the input
    # Checks if a number returns nothing and the correct error message is printed
    # Checks if the input is none and the correct error message is printed
    def test_verify_start_input(self):
      self.assertEqual(word_ladder.verify_start_input("hide"), "hide")
      self.assertEqual(word_ladder.verify_start_input(243215), None, "Please ensure your excluded words only contain letters and are in the format stated.\n")
      self.assertEqual(word_ladder.verify_start_input(""), None, "Please enter a start word!")

    # Checks if a word is returned in the same format as the input
    # Checks if a number returns nothing and the correct error message is printed
    # Checks if a word that doesn't match the length of the start word returns nothing and the correct error message is printed
    def test_verify_target_input(self):
      self.assertEqual(word_ladder.verify_target_input("seek"), "seek")
      self.assertEqual(word_ladder.verify_target_input(243215), None, "Please enter a valid target word only containing letters!")
      self.assertEqual(word_ladder.verify_target_input("seeks"), None, "Please ensure your target word is the same length as your start word")

    # Tests if a blank input returns none and the correct message is printed
    # Tests if a the excluded words is returns the same
    # Checks if a number returns nothing and the correct error message is printed
    # Checks if a collection of words not in the correct format returns nothing
    def test_verify_excluded_input(self):
      self.assertEqual(word_ladder.verify_excluded_input(""), None, "No words provided to exclude from the laddergram search\n")
      self.assertEqual(word_ladder.verify_excluded_input("seek, reef, leek"), ['seek', ' reef', ' leek'])
      self.assertEqual(word_ladder.verify_excluded_input(243215), None, "Please ensure your excluded words only contain letters and are in the format stated.\n")
      self.assertTrue(word_ladder.verify_excluded_input("seek reef leek"), None)

    # Checks if an input is none, and the return value is none, and the correct message is printed
    # Checks if a word input is returned the same
    # Checks if a word input that doesn't match the length of the start word, and returns nothing, and the correct error message is printed
    # Checks if a number returns nothing
    def test_verify_included_input(self):
      self.assertEqual(word_ladder.verify_included_input(None), None, "No word provided to include in laddergram search, please wait...\n")
      self.assertEqual(word_ladder.verify_included_input("reef"), "reef")
      self.assertEqual(word_ladder.verify_included_input("reefs"), None, "Please ensure your word to include is the same length as your start or target word!\n")
      self.assertFalse(word_ladder.verify_included_input(43215), None)

    # Checks if the 2 words are exactly 5 steps apart
    # Checks if the 2 words are next to each other
    # Checks if the 2 words that are not 1 step apart raises an exception error
    def test_same(self):
      self.assertEqual(word_ladder.same("check", "checking"), 5)
      self.assertTrue(word_ladder.same("beef", "been"), 0)
      self.assertRaises(TypeError, word_ladder.same("test", "pool"), 1)

    # Checks if the pattern from hide to seek is correct
    def test_build(self):
      self.assertFalse(word_ladder.build(".ide", "side, site, sits, sies, sees, seek", {"seek": True}, []) == False)

    # Checks if the pattern from hide to seek is correct
    def test_find(self):
      self.assertTrue(word_ladder.find("hide", "hide, side, site, sits, sies, sees, seek", {"hide": True}, "seek", ["hide"]) == False )


if __name__ == '__main__':
    unittest.main()