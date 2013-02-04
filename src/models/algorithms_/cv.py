"""
Cumulative voting algorithm for the app.
"""

__author__ = 'Waseem Ahmad <waseem@rice.edu>'

import logging

def get_counts(ballots):
	"""
	Returns the number of votes for each candidate in the ballots.
	"""
	counts = {}
	for ballot in ballots:
		for candidate, votes in ballot.items():
			if candidate not in counts:
				counts[candidate] = votes
			else:
				counts[candidate] += votes
	return counts


def run_cv(ballots, num_winners):
	"""
	Computes the winners for the cumulative voting position. Due to insufficient
	number of candidates or ties, the number of winners returned is not
	gauranteed to be equal to num_winners.

	Args:
		ballots{List<dictionary>}: A list of ballots, where each ballot is a 
			dictionary whose keys are the candidates and values are the votes
			given.
		num_winners{Integer}: Number of winners to compute.
	Returns:
		winners{List}: A list of winners
	"""
	logging.info('Computing winners from %s ballots cast.', len(ballots))
	winners = []
	counts = get_counts(ballots)
	while counts and len(winners) < num_winners:
		max_count = max(counts.values())
		for candidate, count in counts.items():
			if count == max_count:
				winners.append(candidate)
				del counts[candidate]
	return winners