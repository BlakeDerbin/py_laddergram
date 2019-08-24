import word_ladder
import unittest

class word_ladder_unit_testing(unittest.TestCase):

  def test_verify_dictionary_input(self):
    self.assertEqual(word_ladder.verify_input("4321543216"))

