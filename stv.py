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
            if i == 0 or not candidate:
                continue  # Skip the voter ID column and empty values
            candidates.add(Candidate(candidate))


ballots: list[Ballot] = []

# Process the votes into ballots
for vote in rows:
    choices: list[Candidate] = []

    for i, candidate in enumerate(vote.values()):
        if i == 0 or not candidate:
            continue

        choices.append(Candidate(candidate))

    ballots.append(Ballot(ranked_candidates=choices))

election_results = pyrankvote.single_transferable_vote(
    candidates=list(candidates),
    ballots=ballots,
    number_of_seats=4,
)

print(election_results)

# Export the results to a pseudo-CSV
# following ElectionBuddy's format

with open("results.csv", "w", newline="") as csvfile:
    # Write the header
    csvfile.write("Elección DCC 2023-1\n\n")
    # Election type
    csvfile.write("Members at Large\n")
    # Separator
    csvfile.write("**************************\n\n")
    # Rounds

    for i, round in enumerate(election_results.rounds):
        csvfile.write(f"Round {i + 1}\n\n")
        # Header row
        csvfile.write("Candidate,Votes,Percentage\n")
        # Write the results for each candidate
        # Calculate total number of votes
        total_votes = sum(result.number_of_votes for result in round.candidate_results)

        for candidate_result in round.candidate_results:
            csvfile.write(f"{candidate_result.candidate.name},")
            csvfile.write(f"{candidate_result.number_of_votes},")
            # Calculate the percentage
            percentage =(
                candidate_result.number_of_votes / total_votes
            ) * 100

            csvfile.write(f"{percentage:.2f}%\n")

        # Round info
        csvfile.write(f"\n Votes tallied: {total_votes}\n")
        csvfile.write(f" Abstentions: {round.number_of_blank_votes}\n")
        # Threshold



