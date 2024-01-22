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
        self.max_opp_bid = 0

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
        print("round: ", round_num, " - ", game_clock, "s remaining\n")
        self.early_game = (round_num < NUM_ROUNDS // 4)

        if not self.early_game:
            monte_carlo_iters = 100
            wins = 0
            my_cards = [eval7.Card(card) for card in my_cards]

            for _ in range(monte_carlo_iters):
                idx = random.randint(0, len(self.opp_holes) - 1)
                opp_cards = self.opp_holes[idx]

                deck = eval7.Deck()
                opp_cards = [eval7.Card(card) for card in opp_cards]

                for card in set(my_cards + opp_cards):
                    deck.cards.remove(card)
                
                deck.shuffle()
                community_cards = deck.peek(5)

                my_hand = my_cards + community_cards
                opp_hand = opp_cards + community_cards

                my_hand_val = eval7.evaluate(my_hand)
                opp_hand_val = eval7.evaluate(opp_hand)

                if my_hand_val > opp_hand_val:
                    wins += 2
                elif my_hand_val == opp_hand_val:
                    wins += 1
                else:
                    wins += 0
        
            winrate = wins / (2 * monte_carlo_iters)
            self.strong_hole = (winrate > 0.5)

        else:
            card1 = my_cards[0]
            card2 = my_cards[1]

            rank1 = card1[0] # "Ad", "9c", "Th" -> "A", "9", "T"
            rank2 = card2[0]

            self.strong_hole = False
            if rank1 == rank2 or (rank1 in "AKQJT9" and rank2 in "AKQJT9") or self.consecutive_suited(card1, card2):
                self.strong_hole = True


    def consecutive_suited(self, card1, card2):
        rank1 = card1[0]
        suit1 = card1[1]
        rank2 = card2[0]
        suit2 = card2[1]
        if (suit2 == suit1):
            rnk1 = ord(rank1)
            rnk2 = ord(rank2)
            if abs(rnk1 - rnk2) == 1 and min(rnk1, rnk2) >= 55: 
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
        if (opp_bid and opp_bid > self.max_opp_bid):
            self.max_opp_bid = opp_bid
        
        if len(opp_cards) >= 2:
            self.opp_holes.append(opp_cards[:2])
            self.opp_bids.append(opp_bid)

    def calculate_strength_flop(self, my_cards, flop, iters):
        deck = eval7.Deck()
        cards = [eval7.Card(card) for card in my_cards]
        for my_card in cards:
            deck.cards.remove(my_card)
        board = [eval7.Card(card) for card in flop]
        for flop_card in board:
            deck.cards.remove(flop_card)
        wins_w_auction = 0
        wins_wo_auction = 0
        community = 2

        for i in range(iters):
            deck.shuffle()
            opp = 3
            draw = deck.peek(opp+community)
            draw = draw + board

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
            draw = draw + board
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
                #We tied the round
                wins_w_auction += 0
        
        strength_w_auction = wins_w_auction / (2* iters)
        strength_wo_auction = wins_wo_auction/ (2* iters)

        return (strength_w_auction -  strength_wo_auction) > 0.2

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
    
    def best_hand(self, my_cards, board):
        eval_board = [eval7.Card(card) for card in board]
        eval_my_cards = [eval7.Card(card) for card in my_cards]
        my_hand = eval7.handtype(eval7.evaluate(eval_board + eval_my_cards))
        return my_hand in ["Trips", "Straight", "Flush", "Full House", "Quads", "Straight Flush"]
    
    # def raise_amount(self, street, my_cards, board_cards, my_stack, opp_stack, min_raise, max_raise):
        # if street==0:
        #     if self.strong_hole == 0:
        #         return 0
        #     if self.strong_hole == 1:
        #         if 2*BIG_BLIND == min_raise:
        #             return min_raise
        #     else:
        #         return min_raise*2
        # else:
        #     hand = self.best_hand(my_cards, board_cards)
        #     if hand in ["Trips", "Straight", "Flush"]:
        #         return min_raise
        #     if hand in ["Full House", "Quads", "Straight Flush"]:
        #         if street < 5:
        #             return min(my_stack, opp_stack)
        #         return min_raise + random.random()*(max_raise - min_raise)
        # return 0

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
        opp_num_cards = len(round_state.hands[1-active])
        print(opp_num_cards)
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
        
        # if street == 0:
        #     if RaiseAction in legal_actions:
        #         if self.strong_hole == 1 and 2*BIG_BLIND == min_raise:
        #             return RaiseAction(min_raise)
        #         if self.strong_hole == 2:
        #             return RaiseAction(min(my_stack, min_raise * 2))
        #     if CheckAction in legal_actions:
        #         return CheckAction()
        #     return CallAction()

        if self.early_game: # loose passive
            if street == 0:
                if RaiseAction in legal_actions:
                    if 2 * BIG_BLIND == min_raise or self.strong_hole:
                        return RaiseAction(min_raise)
                if CheckAction in legal_actions:
                    return CheckAction()
                if CallAction in legal_actions:
                    if self.strong_hole:
                        return CallAction()
                return FoldAction()
            if street == 3:
                stay = self.best_hand(my_cards, board_cards)
                if BidAction in legal_actions:
                    if self.strong_hole:
                        return BidAction(min(1, my_stack))
                    return BidAction(int(random.random()*my_stack))
                if RaiseAction in legal_actions and stay:
                    raise_frac = 0.2 + random.random() * 0.2
                    raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
                    return RaiseAction(raise_amount)
                if CheckAction in legal_actions:
                    return CheckAction()
                if CallAction in legal_actions:
                    if stay:
                        return CallAction()
                return FoldAction()
            else:
                stay = self.best_hand(my_cards, board_cards)
                if stay:
                    if RaiseAction in legal_actions:
                        raise_frac = 0.2 + random.random() * 0.2
                        raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
                        return RaiseAction(raise_amount)
                    if CheckAction in legal_actions:
                        return CheckAction()
                    return CallAction()
                else:
                    if CheckAction in legal_actions:
                        return CheckAction()
                    return FoldAction()
        
        else: # tight aggressive
            if self.strong_hole: # tight range
                if BidAction in legal_actions:
                    idx = random.randint(1, len(self.opp_bids) - 1)
                    bid = self.opp_bids[idx] + 1
                    bid = min(bid, my_stack)
                    return BidAction(bid)
                if RaiseAction in legal_actions:
                    raise_frac = 0.2 + random.random() * 0.2
                    raise_amount = int(min_raise + (max_raise - min_raise) * raise_frac)
                    return RaiseAction(raise_amount)
                if CallAction in legal_actions:
                    return CallAction()
            if CheckAction in legal_actions:
                return CheckAction()
            if BidAction in legal_actions:
                return BidAction(1)
            return FoldAction()
    

if __name__ == '__main__':
    run_bot(Player(), parse_args())