from Code.Variables.SettingVariables import *
from Code.Individuals.Interactable import *


class CardManager:
          def __init__(self, game):
                    self.game = game

                    self.cards = []
                    for i in range(1, GENERAL["misc"][6] + 1):
                              self.cards.append(Cards(self.game, (self.game.render_resolution[0] / (GENERAL["misc"][6] + 1) * i, self.game.render_resolution[1] / 2), self.game.methods.create_card()))
                    self.on_timer = Timer(GENERAL['cooldowns'][2], self.game.ticks)

          def update(self):
                    for card in self.cards:
                              card.update()
                              card.active = self.game.cards_on
                              if card.check_for_input() and self.game.inputM.get("left_click") and self.on_timer.update(self.game.ticks):
                                        card.apply_effect()
                                        self.game.cards_on = False

          def draw(self):
                    if not self.game.died:
                              for card in self.cards:
                                        card.draw()

          def toggle(self):
                    self.game.cards_on = True
                    self.on_timer.reactivate(self.game.ticks)
                    for i in range(0, GENERAL["misc"][6]):
                              index = random.randint(0, 165)

                              # Find the appropriate key in CARDS
                              selected_key = None
                              for key in sorted(CARDS.keys()):
                                        if index <= key:
                                                  selected_key = key
                                                  break

                              card_type, card_value = CARDS[selected_key]
                              multiplier = selected_key - index + 1
                              dictionary = {"damage": 0, "health": 0, "pierce": 0, "attack_speed": 0, "stamina": 0, "shots": 0, "knockback": 0}
                              dictionary.update({card_type: card_value * multiplier})
                              self.cards[i].reset(dictionary, index)
