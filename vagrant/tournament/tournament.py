#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import numpy as np

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('delete from Matches;')
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute('delete from Players;')
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    count = c.fetchone()[0]
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (NAME) values (%s)", (bleach.clean(name),))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []
    db = connect()
    c = db.cursor()
    ids_query = 'select id from players;'
    c.execute(ids_query)
    ids = c.fetchall()   
    for id_ in ids:
        id_ = id_[0]
        name = 'select name from players where id = %d;' %id_
        wins = 'select count(*) from matches where winner = %d;' %id_
        matches = 'select count(*) from matches where winner = %d or loser = %d;'%(id_, id_)
        c.execute(name)
        name = c.fetchone()[0]
        c.execute(wins)
        wins = c.fetchone()[0]
        c.execute(matches)
        matches = c.fetchone()[0]
        standings.append((id_, name, wins, matches))
    db.close()
    return standings
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches values (%d, %d)" % (winner,loser))  # Better, but ...
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    pairings = []
    standings = playerStandings()
    dtype = [('id', int), ('name', 'S10'), ('wins', int), ('matches', int)]
    values = standings
    a = np.array(values, dtype=dtype)       # create a structured array
    pairings_temp = np.sort(a, order='wins') 
    for i in range(0,len(pairings_temp)/2):
        id1 = pairings_temp[(2*i)][0]
        name1 = pairings_temp[(2*i)][1]
        id2 = pairings_temp[(2*i+1)][0]
        name2 = pairings_temp[(2*i+1)][1]
        pairings.append((id1, name1, id2, name2))
    return pairings

