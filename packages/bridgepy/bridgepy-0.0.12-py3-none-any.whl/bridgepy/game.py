from dataclasses import dataclass, field
from typing import Optional

from bridgepy.bid import Bid
from bridgepy.card import Card, Deck, Suit
from bridgepy.entity import Entity
from bridgepy.exception import GameAlready4Players, GameAlreadyDealtException, GameAlreadyFinishedException,\
    GameAuctionAlreadyFinishedException, GameAuctionNotFinishedException, GameInvalidBidException,\
    GameInvalidBidStateException, GameInvalidPlayerTrickException, GameInvalidTrickStateException, GameNotBidWinner,\
    GameNotConcludedYetException, GameNotPlayerBidTurnException, GameNotPlayerTrickTurnException,\
    GameNotReadyForTrickWinnerExcception, GameNotReadyToDealYetException, GamePartnerAlreadyChosenException,\
    GamePartnerNotChosenYetException, GamePlayerAlreadyAdded, GamePlayerAlreadyVotedResetException, GamePlayerNotFound
from bridgepy.player import PlayerAction, PlayerBid, PlayerHand, PlayerId, PlayerScore, PlayerTrick


@dataclass
class GameId:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class GameTrick:
    player_tricks: list[PlayerTrick]

    def ready_for_trick_winner(self) -> bool:
        return len(self.player_tricks) == 4

    def trick_winner(self, trump_suit: Suit | None) -> PlayerId:
        if not self.ready_for_trick_winner():
            raise GameNotReadyForTrickWinnerExcception()
        first_suit: Suit = self.first_suit()
        no_trump_player_tricks = self.__player_tricks_by_suit(first_suit)
        no_trump_winner_trick = self.__player_trick_winner(no_trump_player_tricks)
        if trump_suit is None:
            return no_trump_winner_trick.player_id
        trump_player_tricks = self.__player_tricks_by_suit(trump_suit)
        if len(trump_player_tricks) == 0:
            return no_trump_winner_trick.player_id
        trump_winner_trick = self.__player_trick_winner(trump_player_tricks)
        return trump_winner_trick.player_id

    def first_suit(self) -> Suit:
        if len(self.player_tricks) == 0:
            raise GameInvalidTrickStateException()
        return self.player_tricks[0].trick.suit
    
    def __player_tricks_by_suit(self, suit: Suit) -> list[PlayerTrick]:
        return [player_trick for player_trick in self.player_tricks if player_trick.trick.suit == suit]
    
    def __player_trick_winner(self, player_tricks: list[PlayerTrick]) -> PlayerTrick:
        return max(player_tricks, key = lambda player_trick: player_trick.trick)

@dataclass
class GamePlayerSnapshot:
    game_id: GameId
    player_id: PlayerId
    player_actions: list[PlayerAction]
    player_hand: PlayerHand
    bids: list[PlayerBid]
    bid_winner: Optional[PlayerBid]
    partner: Optional[Card]
    partner_player_id: Optional[PlayerId]
    tricks: list[GameTrick]
    scores: list[PlayerScore]
    player_turn: Optional[PlayerId]

@dataclass
class Game(Entity[GameId]):
    id: GameId
    player_ids: list[PlayerId]
    player_hands: list[PlayerHand] = field(default_factory = list)
    bids: list[PlayerBid] = field(default_factory = list)
    partner: Optional[Card] = None
    partner_player_id: Optional[PlayerId] = None
    tricks: list[GameTrick] = field(default_factory = list)
    reset_votes: list[PlayerId] = field(default_factory = list)

    def player_snapshot(self, player_id: PlayerId) -> GamePlayerSnapshot:
        if player_id not in self.player_ids:
            raise GamePlayerNotFound()
        dealt: bool = self.dealt()
        game_bid_ready: bool = self.game_bid_ready()
        bid_turn: bool = self.next_bid_player_id() == player_id if dealt and not game_bid_ready else False
        game_finished: bool = self.game_finished()
        trick_turn: bool = self.next_trick_player_id() == player_id if dealt and game_bid_ready and self.partner is not None and not game_finished else False
        bid_winner = self.bid_winner() if dealt and game_bid_ready else None
        scores: list[PlayerScore] = self.scores()
        game_concluded: bool = self.__game_concluded(scores)
        player_voted: bool = self.__player_score(player_id, scores).voted

        player_actions: list[PlayerAction] = []
        if bid_turn:
            player_actions.append(PlayerAction.BID)
        if bid_winner is not None and player_id == bid_winner.player_id and self.partner is None:
            player_actions.append(PlayerAction.CHOOSE_PARTNER)
        if trick_turn:
            player_actions.append(PlayerAction.TRICK)
        if game_concluded and not player_voted:
            player_actions.append(PlayerAction.RESET)

        player_turn = None
        if dealt and not game_bid_ready:
            player_turn = self.next_bid_player_id()
        if bid_winner is not None and self.partner is None:
            player_turn = bid_winner.player_id
        if dealt and game_bid_ready and self.partner is not None and not game_finished:
            player_turn = self.next_trick_player_id()

        return GamePlayerSnapshot(
            game_id = self.id,
            player_id = player_id,
            player_actions = player_actions,
            player_hand = self.find_player_hand(player_id),
            bids = self.bids,
            bid_winner = bid_winner,
            partner = self.partner,
            partner_player_id = self.partner_player_id,
            tricks = self.tricks,
            scores = scores,
            player_turn = player_turn,
        )
    
    def find_player_hand(self, player_id: PlayerId) -> PlayerHand:
        for player_hand in self.player_hands:
            if player_hand.player_id == player_id:
                return player_hand
        return PlayerHand(player_id, [])

    def add_player(self, player_id: PlayerId) -> None:
        if player_id in self.player_ids:
            raise GamePlayerAlreadyAdded()
        if len(self.player_ids) >= 4:
            raise GameAlready4Players()
        self.player_ids.append(player_id)
        if self.ready_to_deal():
            self.deal()

    def ready_to_deal(self) -> bool:
        return len(self.player_ids) == 4
    
    def dealt(self) -> bool:
        return len(self.player_hands) == 4
    
    def deal(self) -> None:
        if not self.ready_to_deal():
            raise GameNotReadyToDealYetException()
        if self.dealt():
            raise GameAlreadyDealtException()
        deck = Deck()
        n_cards_per_player = len(deck.cards) // len(self.player_ids)
        player_hands: list[PlayerHand] = []
        for i in range(len(self.player_ids)):
            player_id: PlayerId = self.player_ids[i]
            cards = deck.cards[i * n_cards_per_player : (i + 1) * n_cards_per_player]
            player_hand = PlayerHand(player_id = player_id, cards = sorted(cards, reverse = True))
            if player_hand.points() < 4:
                self.deal()
                return
            player_hands.append(player_hand)
        self.player_hands += player_hands

    def next_bid_player_id(self) -> PlayerId:
        return self.player_ids[(len(self.bids) + 1) % 4]

    def game_bid_ready(self) -> bool:
        for player_bid in reversed(self.bids):
            if player_bid.bid is None:
                continue
            if player_bid.bid == Bid(level = 7, suit = None):
                return True
        some_player_bid: bool = self.some_player_bid()
        return some_player_bid and len(self.bids) >= 3 and all(player_bid.bid is None for player_bid in self.bids[-3:])

    def valid_bid(self, bid: Bid | None) -> bool:
        if bid is None:
            return True
        valid_bid: bool = bid.level >= 1 and bid.level <= 7
        if not self.some_player_bid():
            return valid_bid
        return valid_bid and bid > self.last_player_bid().bid
    
    def some_player_bid(self) -> bool:
        return any(player_bid.bid is not None for player_bid in self.bids)

    def last_player_bid(self) -> PlayerBid:
        for player_bid in reversed(self.bids):
            if player_bid.bid is not None:
                return player_bid
        raise GameInvalidBidStateException()
    
    def bid(self, player_bid: PlayerBid) -> None:
        if player_bid.player_id not in self.player_ids:
            raise GamePlayerNotFound()
        if self.game_bid_ready():
            raise GameAuctionAlreadyFinishedException()
        if self.next_bid_player_id() != player_bid.player_id:
            raise GameNotPlayerBidTurnException()
        if not self.valid_bid(player_bid.bid):
            raise GameInvalidBidException()
        self.bids.append(player_bid)
        if self.__all_players_pass():
            self.reset_game()
    
    def __all_players_pass(self) -> bool:
        return len(self.bids) == 4 and all([player_bid.bid is None for player_bid in self.bids])

    def bid_winner(self) -> PlayerBid:
        if not self.game_bid_ready():
            raise GameAuctionNotFinishedException()
        return self.last_player_bid()
    
    def choose_partner(self, player_id: PlayerId, partner: Card) -> None:
        if player_id not in self.player_ids:
            raise GamePlayerNotFound()
        if self.bid_winner().player_id != player_id:
            raise GameNotBidWinner()
        if self.partner is not None:
            raise GamePartnerAlreadyChosenException()
        self.partner = partner

    def trump_suit(self) -> Suit | None:
        bid_winner = self.bid_winner()
        if bid_winner.bid is None:
            raise GameInvalidBidStateException()
        return bid_winner.bid.suit

    def game_finished(self) -> bool:
        return len(self.tricks) == 13 and self.tricks[-1].ready_for_trick_winner()
    
    def next_trick_player_id(self) -> PlayerId:
        if self.game_finished():
            raise GameAlreadyFinishedException()
        trump_suit: Suit | None = self.trump_suit()
        if len(self.tricks) == 0:
            bid_winner_player_id: PlayerId = self.bid_winner().player_id
            return self.next_player(bid_winner_player_id) if trump_suit is not None else bid_winner_player_id
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
            trick_winner_player_id: PlayerId = game_trick.trick_winner(trump_suit)
            return trick_winner_player_id
        last_player_trick: PlayerTrick = game_trick.player_tricks[-1]
        last_player_trick_player_id: PlayerId = last_player_trick.player_id
        return self.next_player(last_player_trick_player_id)

    def next_player(self, player_id: PlayerId) -> PlayerId:
        i = self.player_ids.index(player_id)
        return self.player_ids[(i + 1) % 4]

    def trick(self, player_trick: PlayerTrick) -> None:
        if player_trick.player_id not in self.player_ids:
            raise GamePlayerNotFound()
        if self.next_trick_player_id() != player_trick.player_id:
            raise GameNotPlayerTrickTurnException()
        if not self.__valid_player_trick(player_trick):
            raise GameInvalidPlayerTrickException()
        if self.__partner_revealed(player_trick):
            self.partner_player_id = player_trick.player_id
        self.find_player_hand(player_trick.player_id).cards.remove(player_trick.trick)
        if len(self.tricks) == 0:
            self.tricks.append(GameTrick(player_tricks = [player_trick]))
            return
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
           self.tricks.append(GameTrick(player_tricks = [player_trick]))
           return
        game_trick.player_tricks.append(player_trick)
    
    def __partner_revealed(self, player_trick: PlayerTrick) -> bool:
        if self.partner is None:
            raise GamePartnerNotChosenYetException()
        return player_trick.trick == self.partner

    def __valid_player_trick(self, player_trick: PlayerTrick) -> bool:
        player_hand: PlayerHand = self.find_player_hand(player_trick.player_id)
        trick_from_player_hand = player_trick.trick in player_hand.cards
        if not trick_from_player_hand:
            return False
        trump_trick: bool = player_trick.trick.suit == self.trump_suit()
        if trump_trick:
            return self.__can_trump(player_trick.player_id)
        if len(self.tricks) == 0:
            return True
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
            return True
        first_suit: Suit = game_trick.first_suit()
        if player_trick.trick.suit == first_suit:
            return True
        first_suit_cards = [card for card in player_hand.cards if card.suit == first_suit]
        return len(first_suit_cards) == 0
        
    def __can_trump(self, player_id: PlayerId) -> bool:
        player_hand: PlayerHand = self.find_player_hand(player_id)
        trump_suit: Suit | None = self.trump_suit()
        trump_cards = [card.suit == trump_suit for card in player_hand.cards]
        if len(trump_cards) == 0:
            return False
        if len(self.tricks) == 0:
            return all(trump_cards)
        game_trick: GameTrick = self.tricks[-1]
        if game_trick.ready_for_trick_winner():
            return self.__trump_broken() or all(trump_cards)
        if len(self.tricks) == 1:
            return False
        first_suit: Suit = game_trick.first_suit()
        if first_suit == trump_suit:
            return True
        first_suit_cards = [card for card in player_hand.cards if card.suit == first_suit]
        return len(first_suit_cards) == 0

    def __trump_broken(self) -> bool:
        for game_trick in reversed(self.tricks):
            for player_trick in reversed(game_trick.player_tricks):
                if player_trick.trick.suit == self.trump_suit():
                    return True
        return False
    
    def scores(self) -> list[PlayerScore]:
        player_scores = [PlayerScore(player_id, 0) for player_id in self.player_ids]
        for game_trick in self.tricks:
            if not game_trick.ready_for_trick_winner():
                continue
            trick_winner_player_id: PlayerId = game_trick.trick_winner(self.trump_suit())
            for player_score in player_scores:
                if player_score.player_id == trick_winner_player_id:
                    player_score.score += 1
                    break
        self.__derive_won_flag(player_scores)
        self.__derive_voted_flag(player_scores)
        return player_scores
    
    def __derive_won_flag(self, player_scores: list[PlayerScore]) -> None:
        if self.partner_player_id is None:
            return
        bid_winner: PlayerBid = self.bid_winner()
        if bid_winner.bid is None:
            raise GameInvalidBidStateException()
        bid_winner_player_ids: set[PlayerId] = {bid_winner.player_id, self.partner_player_id}
        opponent_player_ids: set[PlayerId] = set(self.player_ids) - set(bid_winner_player_ids)
        bid_winner_total_score: int = sum([player_score.score for player_score in player_scores if player_score.player_id in bid_winner_player_ids])
        opponent_total_score: int = sum([player_score.score for player_score in player_scores if player_score.player_id in opponent_player_ids])
        if bid_winner_total_score >= bid_winner.bid.level + 6:
            for player_score in player_scores:
                if player_score.player_id in bid_winner_player_ids:
                    player_score.won = True
            return
        if opponent_total_score >= 13 - (bid_winner.bid.level + 6) + 1:
            for player_score in player_scores:
                if player_score.player_id in opponent_player_ids:
                    player_score.won = True
    
    def __derive_voted_flag(self, player_scores: list[PlayerScore]) -> None:
        if len(self.reset_votes) == 0:
            return
        for player_score in player_scores:
            if player_score.player_id in self.reset_votes:
                player_score.voted = True
    
    def __player_score(self, player_id: PlayerId, player_scores: list[PlayerScore]) -> PlayerScore:
        for player_score in player_scores:
            if player_score.player_id == player_id:
                return player_score
        raise GamePlayerNotFound()
    
    def reset(self, player_id: PlayerId) -> None:
        if player_id not in self.player_ids:
            raise GamePlayerNotFound()
        if not self.game_concluded():
            raise GameNotConcludedYetException()
        if player_id in self.reset_votes:
            raise GamePlayerAlreadyVotedResetException()
        self.reset_votes = list(set(self.reset_votes).union({player_id}))
        if len(self.reset_votes) == 4:
            self.reset_game()
    
    def game_concluded(self) -> bool:
        player_scores: list[PlayerScore] = self.scores()
        return self.__game_concluded(player_scores)
    
    def __game_concluded(self, player_scores: list[PlayerScore]) -> bool:
        return any([player_score.won for player_score in player_scores])
    
    def reset_game(self) -> None:
        self.reset_votes.clear()
        self.player_hands.clear()
        self.bids.clear()
        self.partner = None
        self.partner_player_id = None
        self.tricks.clear()
        self.__rotate()
        if self.ready_to_deal():
            self.deal()
    
    def __rotate(self) -> None:
        self.player_ids = self.player_ids[1:] + [self.player_ids[0]]
