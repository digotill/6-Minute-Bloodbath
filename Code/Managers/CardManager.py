from Code.Variables.SettingVariables import *
from Code.Individuals.Interactable import *


class CardManager:
    def __init__(self, game):
        self.game = game

        # Initialize the list of cards
        self.cards = []
        # Create and position cards based on the game's render resolution and settings
        for i in range(1, GENERAL["misc"][6] + 1):
            self.cards.append(Cards(self.game, (
                self.game.render_resolution[0] / (GENERAL["misc"][6] + 1) * i,
                self.game.render_resolution[1] / 2), self.game.methods.create_card()))
        # Initialize a timer for card interactions
        self.on_timer = Timer(GENERAL['cooldowns'][2], self.game.ticks)

    def update(self):
        # Update each card's state
        for card in self.cards:
            card.update()
            card.change_colour()
            # Set card active state based on the game's card toggle
            card.active = self.game.cards_on
            # Check for user input and timer update to apply card effects
            if card.check_for_input() and self.game.inputM.get("left_click") and self.on_timer.update(
                    self.game.ticks):
                card.apply_effect()
                # Disable cards after an effect is applied
                self.game.cards_on = False

    def draw(self):
        # Draw cards only if the game is not in a 'died' state
        if not self.game.died:
            for card in self.cards:
                card.draw()

    def toggle(self):
        # Enable card interactions and reset the timer
        self.game.cards_on = True
        self.on_timer.reactivate(self.game.ticks)
        # Randomly select and reset cards with new attributes
        for i in range(0, GENERAL["misc"][6]):
            index = random.randint(0, 165)

            # Find the appropriate key in CARDS based on the random index
            selected_key = None
            for key in sorted(CARDS.keys()):
                if index <= key:
                    selected_key = key
                    break

            # Retrieve card type and value, calculate multiplier
            card_type, card_value = CARDS[selected_key]
            multiplier = selected_key - index + 1
            # Create a dictionary of card attributes and update with new values
            dictionary = {"damage": 0, "health": 0, "pierce": 0, "attack_speed": 0, "stamina": 0,
                          "shots": 0, "knockback": 0}
            dictionary.update({card_type: card_value * multiplier})
            # Reset the card with new attributes
            self.cards[i].reset(dictionary, index)
