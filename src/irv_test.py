"""
Test cases for instant run-off voting algorithm.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'


import irv
import unittest


class TestInstantRunoffVoting(unittest.TestCase):

    def test_empty(self):
        ballots = []
        winners = irv.run_irv(ballots)
        self.assertEqual(winners, [])
    
    def test_no_majority(self):
        ballots = [['Slice', 'Sneaky'],
                   ['Sneaky', 'Slice']]
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Slice', 'Sneaky']))
    
    def test_single_ballot(self):
        ballots = [['Slice', 'Sneaky']]
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Slice']))

    def test_majority(self):
        ballots = [['Bluesy', 'Slice', 'Awesome', 'Mysterious'],
                   ['Bluesy', 'Slice', 'Awesome'],
                   ['Bluesy', 'Slice', 'Awesome'],
                   ['Bluesy', 'Slice', 'Awesome', 'Mysterious']]
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Bluesy']))
    
    def test_tie(self):
        ballots = [['Bluesy', 'Slice', 'Awesome'],
                   ['Bluesy', 'Awesome', 'Slice'],
                   ['Slice', 'Awesome', 'Bluesy'],
                   ['Slice', 'Awesome', 'Bluesy']]
        # Awesome should get eliminated, but that still leaves a tie
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Slice', 'Bluesy']))
        
    def test_eliminate_loser(self):
        ballots = [['Slice', 'Bluesy', 'Awesome'],
                   ['Bluesy', 'Slice', 'Awesome'],
                   ['Bluesy', 'Slice', 'Awesome'],
                   ['Bluesy', 'Slice', 'Awesome'],
                   ['Awesome', 'Slice', 'Bluesy'],
                   ['Awesome', 'Slice', 'Bluesy']]
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Bluesy']))
        for ballot in ballots:
            self.assertNotIn('Slice', ballot)
    
    def test_tie_3(self):
        ballots = [['Awesome', 'Bluesy', 'Slice'],
                   ['Awesome', 'Slice', 'Bluesy'],
                   ['Slice', 'Bluesy', 'Awesome'],
                   ['Slice', 'Awesome', 'Bluesy'],
                   ['Bluesy', 'Slice', 'Awesome'],
                   ['Bluesy', 'Awesome', 'Slice']]
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Awesome', 'Bluesy', 'Slice']))
        
    def test_write_in_winner(self):
        ballots = [['Mysterious', 'Slice', 'Bluesy', 'Awesome'],
                   ['Bluesy', 'Mysterious', 'Slice', 'Awesome'],
                   ['Mysterious', 'Bluesy', 'Slice', 'Awesome'],
                   ['Mysterious', 'Bluesy', 'Slice', 'Awesome'],
                   ['Awesome', 'Slice', 'Bluesy'],
                   ['Awesome', 'Slice', 'Bluesy']]
        winners = irv.run_irv(ballots)
        self.assertSetEqual(set(winners), set(['Mysterious']))

if __name__ == '__main__':
    unittest.main()