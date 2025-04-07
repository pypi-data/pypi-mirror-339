from bridgepy.card import Card
from bridgepy.bid import Bid
from bridgepy.game import Game
from bridgepy.player import PlayerBid, PlayerId, PlayerTrick
from dataclasses import dataclass
from enum import IntEnum
from typing import Type, TypeVar

from bridgebot.dataencoder import BidEncoder, CardEncoder
from bridgebot.exception import BridgeActionInvalid


ActionType = TypeVar("ActionType", bound = "Action")

class ActionRange(IntEnum):
    BID_START = 0
    BID_END = 35
    PARTNER_START = 36
    PARTNER_END = 87
    TRICK_START = 88
    TRICK_END = 139
    UPDATE_REWARD = 140

@dataclass
class Action:
    value: int

    def apply(self, game: Game, player_id: PlayerId) -> None:
        if self.__bid_action():
            bid: Bid | None = BidEncoder.decode(self.value)
            game.bid(PlayerBid(player_id, bid))
        elif self.__choose_partner_action():
            card: Card = CardEncoder.decode(self.value - ActionRange.PARTNER_START)
            game.choose_partner(player_id, card)
        elif self.__trick_action():
            card: Card = CardEncoder.decode(self.value - ActionRange.TRICK_START)
            game.trick(PlayerTrick(player_id, card))
        elif self.__update_reward():
            pass
        else:
            raise BridgeActionInvalid()
    
    def __bid_action(self) -> bool:
        return ActionRange.BID_START <= self.value <= ActionRange.BID_END
    
    def __choose_partner_action(self) -> bool:
        return ActionRange.PARTNER_START <= self.value <= ActionRange.PARTNER_END

    def __trick_action(self) -> bool:
        return ActionRange.TRICK_START <= self.value <= ActionRange.TRICK_END

    def __update_reward(self) -> bool:
        return self.value == ActionRange.UPDATE_REWARD

    @classmethod
    def encode_bid(cls: Type[ActionType], bid: Bid | None) -> ActionType:
        value: int = BidEncoder.encode(bid)
        return cls(value = value + ActionRange.BID_START)
    
    @classmethod
    def encode_choose_partner(cls: Type[ActionType], partner: Card) -> ActionType:
        value: int = CardEncoder.encode(partner)
        return cls(value = value + ActionRange.PARTNER_START)
    
    @classmethod
    def encode_trick(cls: Type[ActionType], trick: Card) -> ActionType:
        value: int = CardEncoder.encode(trick)
        return cls(value = value + ActionRange.TRICK_START)
    
    @classmethod
    def encode_update_reward(cls: Type[ActionType]) -> ActionType:
        value: int = 0
        return cls(value = value + ActionRange.UPDATE_REWARD)
