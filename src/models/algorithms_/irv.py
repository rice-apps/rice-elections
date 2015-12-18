#
# Below code from StackOverflow.
# http://stackoverflow.com/questions/5762671/list-sorting-modify-problem
#
# Modified by Waseem Ahmad (waseem@rice.edu) to adapt to Owlection


import random
import logging

# Candidates:
candidates = ['John', 'Max', 'Philip', 'Eric', 'Jane']

def simul_ballots(num_voters):
    """
    Returns the (random) ballots of num_voters voters.
    """

    ballots = []

    choice = candidates[:]

    for _ in range(num_voters):
        random.shuffle(choice)
        ballots.append(choice[:])  # Copy

    return ballots

def get_counts(ballots):
    """
    Returns the number of votes for each candidate placed first in the
    ballots.

    Candidates present in the ballots but found in any first ballot
    places are given a count of zero.
    """

    counts = dict()
    for ballot in ballots:
        if ballot:
            vote = ballot[0]
            if vote in counts:
                counts[vote] += 1
            else:
                counts[vote] = 1

    # Python 2.7+ replacement for the above code:
    # counts = collections.Counter(ballot[0] for ballot in ballots)

    candidates = set()
    for ballot in ballots:
        candidates.update(ballot)

    for not_represented in set(candidates)-set(counts):
        counts[not_represented] = 0

    return counts


def get_winners(ballots):
    """
    Returns the winners in the given ballots (lists of candidates), or
    [] if there is no winner.

    A winner is a candidate with 50 % + 1 or more of the votes, or a
    candidate with as many votes as all the other candidates.
    """
    counts = get_counts(ballots)
    if not counts:
        return []

    max_count = max(counts.values())
    num_counts = sum(counts.values())

    potential_winners = [candidate for (candidate, count) in counts.items()
                                if count == max_count]

    if max_count >= num_counts/2. + 1 or len(potential_winners) == len(counts):
        return potential_winners
    else:
        return []


def get_losers(ballots):
    """
    Returns the loser(s) of the ballots, i.e. the candidate(s) with the
    fewest voters.

    Returns [] if all candidates have the same number of votes.
    """

    counts = get_counts(ballots)
    if not counts:
        return []
    
    min_count = min(counts.values())

    potential_losers = [candidate for (candidate, count) in counts.items()
                              if count == min_count]

    if len(potential_losers) == len(counts):
        return []
    else:
        return potential_losers

def remove_candidate(ballots, candidate):
    """
    Removes the given candidate from the ballots.
    """
    for ballot in ballots:
        if candidate in ballot:
            ballot.remove(candidate)


def run_irv(ballots):
    """
    Runs the instant run-off voting algorithm to find the winners for the election.
    
    Args:
        ballots {List<List<Object>>}: the ballots cast, will be modified by the algorithm
    
    Returns:
        winners {List<Object>}: the winners of the election, usually one. More than one in the case of a tie.
    """
    logging.info('Computing winner from %s ballots cast.', len(ballots))
    while True:
        logging.info('Counts: %s', get_counts(ballots))
        winners = get_winners(ballots)
        if winners:
            return winners
        
        losers = get_losers(ballots)
        if not losers:
            break
            
        for loser in losers:
            remove_candidate(ballots, loser)
    logging.info('Found %d winners requested', len(winners))
    return winners

def run_the_rounds(ballots):
    """
    Runs the IRV algorithm and returns the results by the generating rounds.

    :param ballots {List<List<Object>>}: the ballots cast, will be modified by the algorithm
    :return {Dictionary<Round Information>}: each round of computation to determin winner.
    """

    logging.info('Computing the Rounds from %s ballots cast.', len(ballots))
    rounds = []
    round_number = 1
    majority = False
    while True:
        new_round = {}

        counts = get_counts(ballots)
        candidates = counts.keys()
        logging.info('Counts: %s', counts)

        new_round['number'] = round_number
        new_round['prefs'] = counts

        winners = get_winners(ballots)

        losers = get_losers(ballots)
        new_round['cut'] = losers


        for loser in losers:
            candidates.remove(loser)
            remove_candidate(ballots, loser)

        new_round['remaining'] = candidates

        if winners:
            majority = True

        new_round['majority'] = majority

        rounds.append(new_round)

        round_number += 1

        if majority:
            break

    return rounds

def gen_ballots(file_name):
    ballots = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            ballots.append(line.split(', '))


    return ballots

if __name__ == '__main__':

    balls = gen_ballots('../../../wrc_ballots.txt')
    print run_the_rounds(balls)

    # ballots = simul_ballots(20)
    #
    # while True:
    #
    #     print "* Votes:"
    #     for ballot in ballots:
    #         print '-', ballot
    #     print "=> Counts:", get_counts(ballots)
    #
    #     winners = get_winners(ballots)
    #     if winners:
    #         break
    #
    #     # The losers are removed:
    #     losers = get_losers(ballots)
    #     print '=> Losers:', losers
    #     for loser in losers:
    #         remove_candidate(ballots, loser)
    #
    # print "Winners: ", winners