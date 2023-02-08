#!/bin/python3

import fileinput

# Dictionary stores records for a player
records = {}

# Data structure to store match result for a given player
class record:
    def __init__(self, opp, res, s1, s2):
        self.opponent = opp
        self.result = res
        self.my_score = s1
        self.opp_score = s2

# Counts number of wins a player has
def win_count(player):
    count = 0
    for rec in records[player]:
        if rec.result == 'win':
            count += 1
    return count

# Take in records from a spreadsheet
for line in fileinput.input(files = 'records.csv'):
    args = line.split(',')

    p1 = args[0]
    if p1 not in records:
        records[p1] = []

    p2 = args[1]
    if p2 not in records:
        records[p2] = []

    g1 = args[2]
    g2 = args[3]

    if (g1 > g2):
        records[p1].append(record(p2, 'win', g1, g2))
        records[p2].append(record(p1, 'loss', g2, g1))
    else:
        records[p1].append(record(p2, 'loss', g1, g2))
        records[p2].append(record(p1, 'win', g2, g1))

# Printing a record
def print_rec(rec, player):
    print(player, "beat" if rec.result == 'win' else "lost to", rec.opponent, rec.my_score, '-', rec.opp_score)

# BFS to compare 2 players
def bfs_comp(p1, p2):
    q = []
    for rec in records[p1]:
        q.append((rec, 1))

    visited = []
    while (q):
        rec, degrees = q.pop(0)

        if rec.opponent in visited:
            continue
        visited.append(rec.opponent)

        if (rec.opponent == p2):
            print(p1, 'has a', degrees, 'degree', rec.result, 'against', p2)
            break

        for next in records[rec.opponent]:
            if next.result == rec.result:
                q.append((next, degrees + 1))

# Interactive program
while True:
    line = input()
    if line == 'quit':
        break
    args = str(line).split()

    command = args[0]
    p1 = args[1] + ' ' + args[2]

    # Print leaderboard
    if command == 'lb':
        players = list(records.keys())
        players.sort(reverse=True, key=lambda player : win_count(player))
        for player in players:
            print(player, win_count(player))
    
    # Print comparison between two players
    elif command == 'comp':
        p2 = args[3] + ' ' + args[4]
        
        # Number of wins
        print(p1, 'has', win_count(p1), 'wins')
        print(p2, 'has', win_count(p2), 'wins')
        
        # Check if they have played before
        for rec in records[p1]:
            if rec.opponent == p2:
                print_rec(rec, p1)

        # Check if they can be indirectly compared
        bfs_comp(p1, p2)

    # Print all records of player
    elif command == 'stat':
        for rec in records[p1]:
            print_rec(rec, p1)