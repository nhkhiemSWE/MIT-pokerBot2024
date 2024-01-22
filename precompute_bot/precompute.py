import pickle
import eval7
import itertools

def calculate_strength( my_cards, iters):
    deck = eval7.Deck()
    my_cards = [eval7.Card(card) for card in my_cards]
    for card in my_cards:
        deck.cards.remove(card)
    wins_w_auction = 0
    wins_wo_auction = 0

    for i in range(iters):
        deck.shuffle()
        opp = 3
        community = 5
        draw = deck.peek(opp+community)
        opp_cards = draw[:opp]
        community_cards = draw[opp:]

        our_hand = my_cards + community_cards
        opp_hand = opp_cards + community_cards

        our_hand_val = eval7.evaluate(our_hand)
        opp_hand_val = eval7.evaluate(opp_hand)

        if our_hand_val > opp_hand_val:
            # We won the round
            wins_wo_auction += 2
        if our_hand_val == opp_hand_val:
            # We tied the round
            wins_wo_auction += 1
        else:
            # We lost the round
            wins_wo_auction

    for i in range(iters):
        deck.shuffle()
        opp = 2
        community = 5
        auction = 1
        draw = deck.peek(opp+community+auction)
        opp_cards = draw[:opp]
        community_cards = draw[opp: opp + community]
        auction_card = draw[opp+community:]
        our_hand = my_cards + auction_card + community_cards
        opp_hand = opp_cards + community_cards

        our_hand_val = eval7.evaluate(our_hand)
        opp_hand_val = eval7.evaluate(opp_hand)

        if our_hand_val > opp_hand_val:
            # We won the round
            wins_w_auction += 2
        elif our_hand_val == opp_hand_val:
            # we tied the round
            wins_w_auction += 1
        else:
            #We tied the round
            wins_w_auction += 0
        
        strength_w_auction = wins_w_auction / (2* iters)
        strength_wo_auction = wins_wo_auction/ (2* iters)

    return strength_w_auction, strength_wo_auction

def hand_to_strength(my_cards): #AcKs, Jc9s

        card_1 = my_cards[0]
        card_2 = my_cards[1]

        rank_1, suit_1 = card_1
        rank_2, suit_2 = card_2

        num_1 = rank_to_numeric[rank_1]
        num_2 = rank_to_numeric[rank_2]

        suited = 'o'
        if suit_1 == suit_2:
            suited = "s"

        if num_1 >= num_2:
            key = rank_1 + rank_2 + suited
        else:
            key = rank_2 + rank_1 + suited

        return key

if __name__ == "__main__":

#     ranks = "AKQJT98765432"
#     iters = 2500

#     offrank_holes = list(itertools.combinations(ranks, 2))
#    # [0,1,2] [a,b,c] ---> [(0,a), (1,b), (2,c)]
#     paired_holes = list(zip(ranks,ranks))

#     suited_off_rank_str = [hole_card[0] + hole_card[1] + 'o' for hole_card in offrank_holes] #AKo, AKs, KAs
#     off_suit_off_rank_str = [hole_card[0] + hole_card[1] + 's' for hole_card in offrank_holes]
#     paired_cards_str = [hole_card[0] +  hole_card[1] + 'o' for hole_card in paired_holes]

#     suited_off_rank = [[hole_card[0] + 'c', hole_card[1] + 'c'] for hole_card in offrank_holes]
#     off_suit_off_rank = [[hole_card[0] + 'c', hole_card[1] + 's'] for hole_card in offrank_holes]
#     paired_cards = [[hole_card[0] + 'c', hole_card[1] + 's'] for hole_card in paired_holes]

#     suited_off_rank_strength = [calculate_strength(hole_cards, iters) for hole_cards in suited_off_rank]
#     off_suit_off_rank_strength = [calculate_strength(hole_cards, iters) for hole_cards in off_suit_off_rank]
#     paired_cards_strength = [calculate_strength(hole_cards, iters) for hole_cards in paired_cards]

#     all_holes = suited_off_rank_str + off_suit_off_rank_str + paired_cards_str
#     all_strengths = suited_off_rank_strength + off_suit_off_rank_strength + paired_cards_strength

#     hand_to_strength = dict()

#     for cards, strength in zip(all_holes, all_strengths):

#         print("strength:", strength)
#         hand_to_strength[cards] = strength
#     print("DONE!!!!! \n")
#     print(hand_to_strength)

#     rank_to_numeric = dict()

#     for i in range(2,10):
#         rank_to_numeric[str(i)] = i

#     for num, rank in enumerate("TJQKA"): #[(0,T), (1,J), (2,Q) ...]
#         rank_to_numeric[rank] = num + 10
    
#     with open("hand_strengths", "wb") as file:
#         pickle.dump(hand_to_strength, file)
    done = []
    deck = eval7.Deck()
    curr_card = deck.peek(1)[0]
    done.append(curr_card)
    result = dict()
    result_list = []
    while len(deck):
        temp_deck = eval7.Deck()
        print(temp_deck)
        for card in done:
            print(card)
            temp_deck.cards.remove(card)
        while len(temp_deck):
            next_card = temp_deck.peek(1)[0]
            result_list.append([str(curr_card), str(next_card)])
        curr_card = deck.peek(1)[0]
        done.append(curr_card)
    print(result_list)

        






