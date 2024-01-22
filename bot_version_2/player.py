'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, BidAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import random
import eval7


class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        self.opp_holes = []
        self.opp_bids = []  

        self.starting_strengths = {'AKo': (0.7594, 0.4838), 'AQo': (0.754, 0.4578), 'AJo': (0.7612, 0.4456), 'ATo': (0.7444, 0.4416),
                                   'A9o': (0.7424, 0.4448), 'A8o': (0.7462, 0.4254), 'A7o': (0.7306, 0.4344), 'A6o': (0.7208, 0.4126),
                                   'A5o': (0.7272, 0.42), 'A4o': (0.714, 0.406), 'A3o': (0.7058, 0.418), 'A2o': (0.6956, 0.3822),
                                   'KQo': (0.749, 0.4564), 'KJo': (0.728, 0.4398), 'KTo': (0.7416, 0.427), 'K9o': (0.7296, 0.4144),
                                   'K8o': (0.7066, 0.394), 'K7o': (0.7074, 0.3844), 'K6o': (0.6982, 0.413), 'K5o': (0.695, 0.371),
                                   'K4o': (0.692, 0.3584), 'K3o': (0.6774, 0.3664), 'K2o': (0.678, 0.3388),
                                   'QJo': (0.7288, 0.42), 'QTo': (0.7376, 0.425), 'Q9o': (0.7188, 0.391), 'Q8o': (0.7148, 0.3962),
                                   'Q7o': (0.7, 0.3622), 'Q6o': (0.6828, 0.3498), 'Q5o': (0.6902, 0.3584), 'Q4o': (0.6692, 0.3324),
                                   'Q3o': (0.6788, 0.3506), 'Q2o': (0.6616, 0.3348),
                                   'JTo': (0.721, 0.4088), 'J9o': (0.7212, 0.3922),'J8o': (0.6904, 0.3634), 'J7o': (0.689, 0.3488),
                                   'J6o': (0.6846, 0.336), 'J5o': (0.6786, 0.3414), 'J4o': (0.662, 0.33), 'J3o': (0.6616, 0.318), 'J2o': (0.6492, 0.313),
                                   'T9o': (0.7102, 0.3718), 'T8o': (0.7092, 0.3634), 'T7o': (0.6982, 0.341), 'T6o': (0.6898, 0.3266),
                                   'T5o': (0.6684, 0.2844), 'T4o': (0.6526, 0.299), 'T3o': (0.634, 0.3172), 'T2o': (0.6338, 0.3098),
                                   '98o': (0.6932, 0.3618), '97o': (0.6882, 0.3392), '96o': (0.6592, 0.3284), '95o': (0.6632, 0.2906),
                                   '94o': (0.6482, 0.291), '93o': (0.6286, 0.2766), '92o': (0.6312, 0.288),
                                   '87o': (0.6792, 0.3328), '86o': (0.6654, 0.316), '85o': (0.6484, 0.3136), '84o': (0.6336, 0.2932),
                                   '83o': (0.6316, 0.2578), '82o': (0.617, 0.2626),
                                   '76o': (0.674, 0.3128), '75o': (0.681, 0.3002), '74o': (0.6482, 0.2936), '73o': (0.6242, 0.2684), '72o': (0.598, 0.2544),
                                   '65o': (0.6396, 0.2926), '64o': (0.6318, 0.2814), '63o': (0.6064, 0.2654), '62o': (0.597, 0.2602),
                                   '54o': (0.6658, 0.3124), '53o': (0.6396, 0.287), '52o': (0.6044, 0.2606),
                                   '43o': (0.6158, 0.2744), '42o': (0.6124, 0.2534),
                                   '32o': (0.594, 0.2498),
                                   'AKs': (0.7544, 0.4638), 'AQs': (0.7442, 0.4586), 'AJs': (0.7228, 0.4424), 'ATs': (0.7264, 0.4446),
                                   'A9s': (0.7194, 0.409), 'A8s': (0.7122, 0.3992), 'A7s': (0.7056, 0.3894), 'A6s': (0.6956, 0.3804),
                                   'A5s': (0.6962, 0.3796), 'A4s': (0.6912, 0.3572), 'A3s': (0.6798, 0.3612), 'A2s': (0.6732, 0.3624),
                                   'KQs': (0.7242, 0.4352), 'KJs': (0.7184, 0.4196), 'KTs': (0.7228, 0.3914), 'K9s': (0.698, 0.3764),
                                   'K8s': (0.6846, 0.3782), 'K7s': (0.6766, 0.3596), 'K6s': (0.6682, 0.3506), 'K5s': (0.6826, 0.3358),
                                   'K4s': (0.6692, 0.3242), 'K3s': (0.6508, 0.322), 'K2s': (0.6552, 0.325),
                                   'QJs': (0.7126, 0.4062), 'QTs': (0.7202, 0.3934), 'Q9s': (0.7014, 0.362), 'Q8s': (0.683, 0.3362),
                                   'Q7s': (0.685, 0.3408), 'Q6s': (0.671, 0.3272), 'Q5s': (0.6706, 0.313), 'Q4s': (0.6428, 0.3074),
                                   'Q3s': (0.6382, 0.3102), 'Q2s': (0.6328, 0.294),
                                   'JTs': (0.722, 0.3752), 'J9s': (0.6794, 0.3484), 'J8s': (0.6678, 0.346), 'J7s': (0.6682, 0.3268),
                                   'J6s': (0.658, 0.305), 'J5s': (0.6486, 0.2994), 'J4s': (0.6348, 0.2932), 'J3s': (0.6206, 0.2754), 'J2s': (0.6036, 0.2678),
                                   'T9s': (0.658, 0.3778), 'T8s': (0.6702, 0.3138), 'T7s': (0.664, 0.3018), 'T6s': (0.6496, 0.2944),
                                   'T5s': (0.6276, 0.281), 'T4s': (0.6158, 0.2662), 'T3s': (0.6094, 0.2722), 'T2s': (0.6084, 0.2632),
                                   '98s': (0.6736, 0.3288), '97s': (0.6636, 0.3064), '96s': (0.645, 0.2932), '95s': (0.6306, 0.2684),
                                   '94s': (0.6244, 0.2492), '93s': (0.6132, 0.2404), '92s': (0.5928, 0.246),
                                   '87s': (0.6652, 0.2988), '86s': (0.6226, 0.2864), '85s': (0.6368, 0.278),
                                   '84s': (0.6044, 0.2492), '83s': (0.596, 0.2396), '82s': (0.5826, 0.2304),
                                   '76s': (0.6474, 0.2864), '75s': (0.6282, 0.2816), '74s': (0.597, 0.246), '73s': (0.5864, 0.2294), '72s': (0.5834, 0.2174),
                                   '65s': (0.6184, 0.2666), '64s': (0.597, 0.266), '63s': (0.5954, 0.2258), '62s': (0.5606, 0.2122),
                                   '54s': (0.6328, 0.2806), '53s': (0.6006, 0.2348), '52s': (0.5734, 0.2204),
                                   '43s': (0.5806, 0.2352), '42s': (0.5748, 0.1998), '32s': (0.5464, 0.199),
                                   'AAo': (0.8828, 0.6864), 'KKo': (0.865, 0.6508), 'QQo': (0.8494, 0.622), 'JJo': (0.8314, 0.6034), 'TTo': (0.8046, 0.5846),
                                   '99o': (0.7944, 0.5518), '88o': (0.7644, 0.5092), '77o': (0.7562, 0.4808), '66o': (0.7252, 0.472), '55o': (0.7192, 0.421),
                                   '44o': (0.6844, 0.3862), '33o': (0.6772, 0.3508), '22o': (0.635, 0.3276)}
        
        rank_to_numeric = dict()

        for i in range(2,10):
            rank_to_numeric[str(i)] = i

        for num, rank in enumerate("TJQKA"): #[(0,T), (1,J), (2,Q) ...]
            rank_to_numeric[rank] = num + 10

        self.rank_to_numeric = rank_to_numeric

        self.num_showdowns = 0
        self.opp_avg_strength = 0.5


    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind

        self.is_big_blind = big_blind
        self.opp_actions = []
        self.my_actions = []

        if self.is_big_blind:
            self.my_actions.append("B")
            self.opp_actions.append("S")
        else:
            self.opp_actions.append("B")
            self.my_actions.append("S")

        self.early_game = (round_num < NUM_ROUNDS // 4)

        self.strong_hole = False

        if not self.early_game:

            card_strength = self.hand_to_strength(my_cards)
            card_strength = (card_strength[0] + card_strength[1])/2

            print(card_strength, self.opp_avg_strength)

            if card_strength > self.opp_avg_strength:
                self.strong_hole = True
        else:
            self.strong_hole = self.hand_to_strength(my_cards)[1] > 0.3

    def hand_to_strength(self, my_cards): #AcKs, Jc9s

        card_1 = my_cards[0]
        card_2 = my_cards[1]

        rank_1, suit_1 = card_1
        rank_2, suit_2 = card_2

        num_1 = self.rank_to_numeric[rank_1]
        num_2 = self.rank_to_numeric[rank_2]

        suited = 'o'
        if suit_1 == suit_2:
            suited = "s"

        if num_1 >= num_2:
            key = rank_1 + rank_2 + suited
        else:
            key = rank_2 + rank_1 + suited

        return self.starting_strengths[key]
    
    def consecutive_suited(self, card1, card2):
        rank1 = card1[0]
        suit1 = card1[1]
        rank2 = card2[0]
        suit2 = card2[1]
        if (suit2 == suit1):
            rnk1 = ord(rank1)
            rnk2 = ord(rank2)
            if abs(rnk1 - rnk2) == 1 and min(rnk1, rnk2) >= 57:
                return True
        return False
    
    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        my_cards = previous_state.hands[active]  # your cards
        opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed

        opp_bid = previous_state.bids[1-active]

        if len(opp_cards) >= 2:
            opp_cur_strength = self.hand_to_strength(opp_cards[:2])
            opp_cur_strength = (opp_cur_strength[0] + opp_cur_strength[1])/2
            self.opp_avg_strength = (self.opp_avg_strength *self.num_showdowns + opp_cur_strength) /(self.num_showdowns + 1)
            self.num_showdowns += 1
            self.opp_holes.append(opp_cards[:2])
            self.opp_bids.append(opp_bid)
        print("our actions:", self.my_actions)
        print("opp actions:", self.opp_actions)
        print("We are big blind?", self.is_big_blind, "\n")

    def calculate_strength_flop(self, my_cards, board_cards, iters):
        deck = eval7.Deck()
        cards = [eval7.Card(card) for card in my_cards]
        for card in my_cards:
            deck.cards.remove(card)
        board = [eval7.Card(card) for card in board_cards]
        for card in board:
            deck.cards.remove(card)
        wins_w_auction = 0
        wins_wo_auction = 0
        community = 5 - len(board)

        for i in range(iters):
            deck.shuffle()
            opp = 3
            draw = deck.peek(opp+community)
            draw += board
            opp_cards = draw[:opp]
            community_cards = draw[opp:]

            our_hand = cards + community_cards
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
                wins_wo_auction += 0

        for i in range(iters):
            deck.shuffle()
            opp = 2
            auction = 1
            draw = deck.peek(opp+community+auction)
            draw += board
            opp_cards = draw[:opp]
            community_cards = draw[(opp + auction + 1) :]
            auction_card = [draw[opp+auction]]

            our_hand = cards + auction_card + community_cards
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
                #We lost the round
                wins_w_auction += 0
        
        strength_w_auction = wins_w_auction / (2* iters)
        strength_wo_auction = wins_wo_auction/ (2* iters)

        return strength_w_auction, strength_wo_auction

    # def calculate_strength_w_aunction(self, my_cards, flop, iters):
    #     deck = eval7.Deck()
    #     my_cards = [eval7.Card(card) for card in my_cards]
    #     for card in my_cards:
    #         deck.cards.remove(card)
    #     table = [eval7.Card(card) for card in flop]
    #     for card in flop:
    #         deck.cards.remove(card)
    #     wins_w_auction = 0
    #     community = 2
    #     for i in range(iters):
    #         deck.shuffle()
    #         opp = 2
    #         auction = 1
    #         draw = deck.peek(opp+community+auction)
    #         opp_cards = draw[:opp]
    #         community_cards = draw[opp: opp + community]
    #         auction_card = draw[opp+community:]
    #         our_hand = my_cards + auction_card + community_cards
    #         opp_hand = opp_cards + community_cards

    #         our_hand_val = eval7.evaluate(our_hand)
    #         opp_hand_val = eval7.evaluate(opp_hand)

    #         if our_hand_val > opp_hand_val:
    #             # We won the round
    #             wins_w_auction += 2
    #         elif our_hand_val == opp_hand_val:
    #             # we tied the round
    #             wins_w_auction += 1
    #         else:
    #             #We tied the round
    #             wins_w_auction += 0
            
    #     strength_w_auction = wins_w_auction / (2* iters)
    #     return strength_w_auction
    # def is_good_hand(self, my_cards, board):
    #     eval_board = [eval7.Card(card) for card in board]
    #     eval_my_cards = [eval7.Card(card) for card in my_cards]
    #     temp_board = eval_board
    #     temp_board.append(eval_my_cards[0])
    #     temp_board.append(eval_my_cards[1])
    #     hand_value = eval7.evaluate(temp_board)
    #     if len(eval_my_cards) == 2:
    #         my_hand = eval7.handtype(hand_value)
    #     else:
    #         temp_board = eval_board
    #         temp_board.append(eval_my_cards[2])
    #         temp_board.append(eval_my_cards[0])
    #         hand_value = max( hand_value, eval7.evaluate(temp_board))
    #         temp_board.pop()
    #         temp_board.append(eval_my_cards[1])
    #         hand_value = max( hand_value, eval7.evaluate(temp_board))
    #         my_hand = eval7.handtype(hand_value)
    #     return my_hand in ["Trips", "Straight", "Flush", "Full House", "Quads", "Straight Flush"]
    
    def is_good_hand(self, my_cards, board):
        if len(board == 0):
            card1 = my_cards[0]
            card2 = my_cards[1]

            rank1 = card1[0] # "Ad", "9c", "Th" -> "A", "9", "T"
            rank2 = card2[0]

            return (rank1 == rank2) or (rank1 in "AKQJT9" and rank2 in "AKQJT9")

        if len(my_cards) == 2:
            opp_cards = 3
        else:
            opp_cards = 2
        wins = 0

        deck = eval7.Deck()
        my_hand = [eval7.Card(card) for card in my_cards]
        for card in my_hand:
            deck.cards.remove(card)
        board_cards = [eval7.Card(card) for card in board]
        for card in board_cards:
            deck.cards.remove(card)

        for i in range(self.iter):
            deck.shuffle()
            draw = deck.peek(opp_cards + 5 - len(board))
            draw += board_cards

            opp_hand = draw[:opp_cards] + draw[opp_cards:]
            our_hand = my_hand + draw[opp_cards:]

            my_hand_val = eval7.evaluate(our_hand)
            opp_hand_val = eval7.evaluate(opp_hand)

            if my_hand_val > opp_hand_val:
                wins += 2
            elif my_hand_val == opp_hand_val:
                wins += 1
            else:
                wins += 0
        return (wins/(self.iter * 2)) > 0.5

    def best_hand(self, my_cards, board):
        eval_board = [eval7.Card(card) for card in board]
        eval_my_cards = [eval7.Card(card) for card in my_cards]
        temp_board = eval_board
        temp_board.append(eval_my_cards[0])
        temp_board.append(eval_my_cards[1])
        hand_value = eval7.evaluate(temp_board)
        if len(eval_my_cards) == 2:
            my_hand =  eval7.handtype(hand_value)
        else:
            temp_board = eval_board
            temp_board.append(eval_my_cards[2])
            temp_board.append(eval_my_cards[0])
            hand_value = max( hand_value, eval7.evaluate(temp_board))
            temp_board.pop()
            temp_board.append(eval_my_cards[1])
            hand_value = max( hand_value, eval7.evaluate(temp_board))
            my_hand = eval7.handtype(hand_value)
        return my_hand in ["Trips", "Straight", "Flush", "Full House", "Quads", "Straight Flush"]

    def update_opp_action(self, continue_cost):
        if (self.my_actions[-1] == "A"):
            self.opp_actions.append("A")
        else:
            if self.is_big_blind:
                if continue_cost > 0:
                    self.opp_actions.append("R")
                else:
                    if (self.my_actions[-1] == "R"):
                        self.opp_actions.append("C")
                    else:
                        self.opp_actions.append("K")
            else:
                if continue_cost >0:
                    self.opp_actions.append("R")
                else:
                    if (self.my_actions[-1] == "R"):
                        self.opp_actions.append("C")
                    else:
                        self.opp_actions.append("K")
    def update_action(self, my_action, continue_cost):

        if self.is_big_blind:
            self.my_actions.append(my_action)
            if continue_cost > 0:
                self.opp_actions.append("R")
            else:
                if my_action == "A":
                    self.opp_actions.append("A")
                else:
                    if self.my_actions[-2] == "A":
                        pass
                    else:
                        if (self.my_actions[-1] == "R"):
                            self.opp_actions.append("C")
                        else:
                            self.opp_actions.append("K")
        else:
            self.my_actions.append(my_action)
            if self.my_actions[-2] == "S":
                pass
            else:
                if continue_cost >0:
                    self.opp_actions.append("R")
                else:
                    if my_action == "A":
                        self.opp_actions.append("A")
                    elif (my_action == "R"):
                        self.opp_actions.append("C")
                    else:
                        self.opp_actions.append("K")


    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        # May be useful, but you may choose to not use.
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        my_bid = round_state.bids[active]  # How much you bid previously (available only after auction)
        opp_bid = round_state.bids[1-active]  # How much opponent bid previously (available only after auction)
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        if RaiseAction in legal_actions:
           min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
           min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
           max_cost = max_raise - my_pip  # the cost of a maximum bet/raise



        if self.early_game: # loose passive
            if RaiseAction in legal_actions and street == 0:
                if 2 * BIG_BLIND == min_raise:
                    self.update_action("R", continue_cost)
                    return RaiseAction(min_raise)
            if BidAction in legal_actions:
                self.update_action("A", continue_cost)
                return BidAction(int(random.random()*my_stack))
            if CheckAction in legal_actions:
                self.update_action("K", continue_cost)
                return CheckAction()
            self.update_action("C", continue_cost)
            return CallAction()
        
        else: # tight aggressive
            if self.strong_hole: # tight range
                if BidAction in legal_actions:
                    if len(self.opp_bids) == 0:
                        self.update_action("A", continue_cost)
                        return BidAction(int(random.random()*my_stack))
                    elif len(self.opp_bids) == 1:
                        idx = 0
                    else:
                        idx = random.randint(1, len(self.opp_bids) - 1)
                    bid = self.opp_bids[idx] + 1
                    bid = min(bid, my_stack)
                    self.update_action("A", continue_cost)
                    return BidAction(bid)
                if RaiseAction in legal_actions:
                    raise_frac = 0.2 + random.random() * 0.2
                    raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
                    self.update_action("R", continue_cost)
                    return RaiseAction(raise_amount)
                if CallAction in legal_actions:
                    self.update_action("C", continue_cost)
                    return CallAction()

            if CheckAction in legal_actions:
                self.update_action("K", continue_cost)
                return CheckAction()
            if BidAction in legal_actions:
                self.update_action("A", continue_cost)
                return BidAction(0)
            self.update_action("F", continue_cost)
            return FoldAction()

        
        # for action in legal_actions:
        #     if isinstance(commit_action, action):
        #         self.update_action(act, continue_costion)
        # return commit_action


        # if self.early_game: # loose passive
        #     if street == 0:
        #         if RaiseAction in legal_actions:
        #             if 2* BIG_BLIND == min_raise or self.strong_hole:
        #                 # if 2 * BIG_BLIND == min_raise:
        #                 return RaiseAction(min_raise)
        #                 # else:
        #                 #     if my_contribution < self.hand_to_strength(my_cards)[1] * STARTING_STACK:
        #                 #         return RaiseAction(min_raise)
        #         if CheckAction in legal_actions:
        #             return CheckAction()
        #         if CallAction in legal_actions:
        #             if self.strong_hole:
        #                 return CallAction()
        #         return FoldAction()
        #     if street == 3:
        #         stay = self.best_hand(my_cards, board_cards)
        #         if BidAction in legal_actions:
        #             if self.strong_hole:
        #                 return BidAction(min(1, my_stack))
        #             return BidAction(int(random.random()*my_stack))
        #         if RaiseAction in legal_actions and stay:
        #             raise_frac = 0.2 + random.random() * 0.2
        #             raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
        #             return RaiseAction(raise_amount)
        #         if CheckAction in legal_actions:
        #             return CheckAction()
        #         if CallAction in legal_actions:
        #             if stay:
        #                 return CallAction()
        #         return FoldAction()
        #     else:
        #         stay = self.best_hand(my_cards, board_cards)
        #         if stay:
        #             if RaiseAction in legal_actions:
        #                 raise_frac = 0.2 + random.random() * 0.2
        #                 raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
        #                 return RaiseAction(raise_amount)
        #             if CheckAction in legal_actions:
        #                 return CheckAction()
        #             return CallAction()
        #         else:
        #             if CheckAction in legal_actions:
        #                 return CheckAction()
        #             return FoldAction()
        
        # else: # tight aggressive
        #     if self.strong_hole: # tight range
        #         if BidAction in legal_actions:
        #             if len(self.opp_bids) == 0:
        #                 return BidAction(int(random.random()*my_stack))
        #             elif len(self.opp_bids) == 1:
        #                 idx = 0
        #             else:
        #                 idx = random.randint(1, len(self.opp_bids) - 1)
        #             bid = self.opp_bids[idx] + 1
        #             bid = min(bid, my_stack)
        #             return BidAction(bid)
        #         if RaiseAction in legal_actions:
        #             raise_frac = 0.2 + random.random() * 0.2
        #             raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
        #             return RaiseAction(raise_amount)
        #         if CallAction in legal_actions:
        #             return CallAction()
        #     if CheckAction in legal_actions:
        #         return CheckAction()
        #     if BidAction in legal_actions:
        #         return BidAction(min(1, my_stack))
        #     return FoldAction()
        
        # if street == 0:
        #     if self.strong_hole:
        #         return self.play_aggressive()
        #     return self.play_safe()
        # else:
        #     if BidAction in legal_actions:
        #         if self.strong_hole:
        #             return self.bid_slightly()
        #         return self.bid_aggressive()
        #     if self.is_good_hand(my_cards, board_cards):
        #         return self.play_aggressive()
        #     return self.play_safe()
            
if __name__ == '__main__':
    run_bot(Player(), parse_args())