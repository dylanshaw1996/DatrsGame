# Author : Dylan Shaw
# StudentID: R00128608
# Class: Software Development


import logging

import grpc

import darts_match_pb2 as darts_match_pb2
import darts_match_pb2_grpc as darts_match_pb2_grpc
from datatype.enums import DartMultiplier
from app.gameimpl import x01_match


def run():
    channel = grpc.insecure_channel('127.0.0.1:50055')
    stub = darts_match_pb2_grpc.DartsMatchStub(channel)

    startingScore = x01_match.STARTING_TOTAL
    print("Starting score is : ", startingScore)

    player1name = input("What is players 1s name: ")
    match1 = stub.CreateMatch(darts_match_pb2.MatchRequest(userName=player1name, matchType='X01')).matchId
    m1_player1 = 0
    player2name = input("What is player 2s name: ")
    m1_player2 = stub.RegisterPlayer(darts_match_pb2.RegisterRequest(matchId=match1, userName=player2name)).playerIndex
    stub.FinalizeMatch(darts_match_pb2.FinalizeRequest(matchId=match1))
    player1Starting = x01_match.STARTING_TOTAL
    player2Starting = x01_match.STARTING_TOTAL

    while player1Starting > 0 or player2Starting > 0:
        dartScore = input("Please enter player 1s score:")
        my_visit = []
        for i in range(3):
            player1score = 0
            splitScore = dartScore.split()
            newNumber = splitScore[i][1] + splitScore[i][2]
            int_newNumber = int(newNumber)
            segment = int_newNumber
            dmultiplyer = splitScore[i][0]
            if dmultiplyer == 'T' or dmultiplyer == 't':
                visit = darts_match_pb2.Dart(multiplier=DartMultiplier.TREBLE, segment=segment)
                newSegment = segment * 3
                player1score = player1score + newSegment
            elif dmultiplyer == 'D' or dmultiplyer == 'd':
                visit = darts_match_pb2.Dart(multiplier=DartMultiplier.DOUBLE, segment=segment)
                newSegment = segment * 2
                player1score = player1score + newSegment
            elif dmultiplyer == 'S' or dmultiplyer == 's':
                visit = darts_match_pb2.Dart(multiplier=DartMultiplier.SINGLE, segment=segment)
                newSegment = segment
                player1score = player1score + newSegment
            else:
                print("Score not in correct format")

                return visit
            player1Starting = player1Starting - player1score
            my_visit.append(visit)

        response = stub.ProcessVisit(darts_match_pb2.VisitRequest(matchId=match1, playerIndex=m1_player1, visit=my_visit))
        print(response.message)
        if player1Starting <=0:
            break

        dartScore1 = input("Please enter player 2s score:")
        my_visit2 = []
        for j in range(3):
            player2score = 0
            splitScore = dartScore1.split()
            newNumber = splitScore[j][1] + splitScore[j][2]
            int_newNumber = int(newNumber)
            segment = int_newNumber
            dmultiplyer = splitScore[j][0]
            if dmultiplyer == 'T' or dmultiplyer == 't':
                visit = darts_match_pb2.Dart(multiplier=DartMultiplier.TREBLE, segment=segment)
                newSegment = segment * 3
                player2score = player2score + newSegment
            elif dmultiplyer == 'D' or dmultiplyer == 'd':
                visit = darts_match_pb2.Dart(multiplier=DartMultiplier.DOUBLE, segment=segment)
                newSegment = segment * 2
                player2score = player2score + newSegment
            elif dmultiplyer == 'S' or dmultiplyer == 's':
                visit = darts_match_pb2.Dart(multiplier=DartMultiplier.SINGLE, segment=segment)
                newSegment = segment
                player2score = player2score + newSegment
            else:
                print("Score not in correct format")

                return visit
            player2Starting = player2Starting - player2score
            my_visit2.append(visit)

        response = stub.ProcessVisit(darts_match_pb2.VisitRequest(matchId=match1, playerIndex=m1_player2, visit=my_visit2))
        print(response.message)

        if player2Starting < 0:
            break


if __name__ == '__main__':
    logging.basicConfig()
    run()
