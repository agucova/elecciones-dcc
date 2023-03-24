import csv

import pyrankvote
from pyrankvote import Ballot, Candidate

rows: list[dict[str, str]] = []
candidates: set[Candidate] = set()

# Infer list of candidates from the input files
with open("votes.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rows.append(row)
        for i, candidate in enumerate(row.values()):
            if i == 0 or not candidate.strip():
                continue  # Skip the voter ID column and empty values
            candidates.add(Candidate(candidate))


ballots: list[Ballot] = []

# Process the votes into ballots
for vote in rows:
    choices: list[Candidate] = []

    for i, candidate in enumerate(vote.values()):
        if i == 0 or not candidate.strip():
            continue
        if candidate not in (c.name for c in candidates):
            raise ValueError(f"Invalid candidate {candidate}")

        choices.append(Candidate(candidate))

    ballots.append(Ballot(ranked_candidates=choices))

election_results = pyrankvote.single_transferable_vote(
    candidates=list(candidates),
    ballots=ballots,
    number_of_seats=4,
)

print(election_results)
print(f"Threshold: {election_results.threshold}")
