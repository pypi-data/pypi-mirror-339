from dataclasses import dataclass
from enum import Enum
from typing import Optional

from bridgepy.bid import Bid
from bridgepy.card import Card, Rank, Suit
from bridgepy.exception import PlayerBidNotFoundException, PlayerInvalidHandException

@dataclass
class PlayerId:
    value: str

    def __hash__(self) -> int:
        return hash(self.value)
    
    def __repr__(self) -> str:
        return self.value

@dataclass
class PlayerHand:
    player_id: PlayerId
    cards: list[Card]

    def points(self) -> int:
        self.__validate(self.cards)
        points: int = 0
        points += self.__calculate_points_by_suit(Suit.CLUB)
        points += self.__calculate_points_by_suit(Suit.DIAMOND)
        points += self.__calculate_points_by_suit(Suit.HEART)
        points += self.__calculate_points_by_suit(Suit.SPADE)
        return points

    def __validate(self, cards: list[Card]) -> None:
        if not (len(cards) == 13 and len(set(cards)) == len(cards)):
            raise PlayerInvalidHandException()
    
    def __calculate_points_by_suit(self, suit: Suit) -> int:
        return max(0, self.__count_cards_by_suit(suit) - 4) + self.__calculate_high_card_points_by_suit(suit)

    def __count_cards_by_suit(self, suit: Suit) -> int:
        return len(self.__get_cards_by_suit(suit))
    
    def __get_cards_by_suit(self, suit: Suit) -> list[Card]:
        return [card for card in self.cards if card.suit == suit]
    
    def __calculate_high_card_points_by_suit(self, suit: Suit) -> int:
        points: int = 0
        for card in self.__get_cards_by_suit(suit):
            if card.rank == Rank.ACE:
                points += 4
            if card.rank == Rank.KING:
                points += 3
            if card.rank == Rank.QUEEN:
                points += 2
            if card.rank == Rank.JACK:
                points += 1
        return points

    def points_by_suit(self, suit: Suit) -> int:
        self.__validate(self.cards)
        return self.__calculate_points_by_suit(suit)

@dataclass
class PlayerBid:
    player_id: PlayerId
    bid: Optional[Bid]

    def require_bid(self) -> Bid:
        if self.bid is None:
            raise PlayerBidNotFoundException()
        return self.bid

@dataclass
class PlayerTrick:
    player_id: PlayerId
    trick: Card

@dataclass
class PlayerScore:
    player_id: PlayerId
    score: int
    won: bool = False
    voted: bool = False

class PlayerAction(str, Enum):
    BID = "BID"
    CHOOSE_PARTNER = "CHOOSE_PARTNER"
    TRICK = "TRICK"
    RESET = "RESET"
