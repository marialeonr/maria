import random

# Define the Card class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

# Define the Hand class
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

# Define the Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades'] for value in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

# Define the BlackjackGame class
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet = 0

    def deal_card(self, hand):
        card = self.deck.deal_card()
        hand.add_card(card)

    def calculate_score(self, hand):
        score = sum(self.card_value(card) for card in hand.cards)
        if score > 21 and any(card.value == 'Ace' for card in hand.cards):
            score -= 10
        return score

    def card_value(self, card):
        if card.value in ['Jack', 'Queen', 'King']:
            return 10
        elif card.value == 'Ace':
            return 11
        else:
            return int(card.value)

    def display_hands(self, show_dealer_card=False):
        print("\nPlayer's hand:")
        for card in self.player_hand.cards:
            print(f"{card.value} of {card.suit}")
        print(f"Total score: {self.calculate_score(self.player_hand)}")

        print("\nDealer's hand:")
        if show_dealer_card:
            for card in self.dealer_hand.cards:
                print(f"{card.value} of {card.suit}")
            print(f"Total score: {self.calculate_score(self.dealer_hand)}")
        else:
            print(f"{self.dealer_hand.cards[0].value} of {self.dealer_hand.cards[0].suit}")
            print("Second card is hidden.")

    def player_turn(self):
        action = input("\nDo you want to 'Hit' or 'Stand'? ").lower()
        return action

    def dealer_turn(self):
        while self.calculate_score(self.dealer_hand) < 17:
            print("Dealer hits.")
            self.deal_card(self.dealer_hand)
            print(f"Dealer's new card: {self.dealer_hand.cards[-1].value} of {self.dealer_hand.cards[-1].suit}")
        print("Dealer stands.")

    def play_round(self):
        print("The first two cards are being given out.")
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet = int(input("Enter your bet: "))

        for _ in range(2):
            self.deal_card(self.player_hand)
            self.deal_card(self.dealer_hand)

        self.display_hands(show_dealer_card=False)

        if self.calculate_score(self.player_hand) == 21:
            print("Blackjack! You win!")
            return 1.5 * self.bet
        else:
            print("Player's turn:")
            action = self.player_turn()
            if action == 'hit':
                print("Hit! Here is your card.")
                self.deal_card(self.player_hand)
                self.display_hands(show_dealer_card=False)
                if self.calculate_score(self.player_hand) > 21:
                    print("Bust! You lose!")
                    return -self.bet
            else:
                print("Stand.")

        print("Dealer's turn:")
        self.dealer_turn()
        self.display_hands(show_dealer_card=True)

        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            print("You win!")
            return self.bet
        elif player_score < dealer_score:
            print("You lose!")
            return -self.bet
        else:
            print("It's a tie!")
            return 0


if __name__ == "__main__":
    game = BlackjackGame()

    while True:
        result = game.play_round()
        print(f"\nYour balance: {result}")

        play_again = input("Do you want to play again? (yes/no) ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break
