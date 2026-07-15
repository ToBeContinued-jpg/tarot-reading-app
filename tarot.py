import random
from tarot_card_data import card_data


class Card():
    
    def __init__(self, name, image, upright, reverse):
        self.name = name
        self.image = image 
        self.upright = upright 
        self.reverse = reverse

class Deck():
    
    def __init__(self):
        self.cards = []
        for data in card_data:
            card = Card(
        data["name"],
        data["image"],
        data["upright"],
        data["reversed"]
        )
            self.cards.append(card)
        
    def shuffle(self):
        random.shuffle(self.cards)
    
    def pop(self) -> Card:
        return self.cards.pop()

class Reading():
    
    orientations = ["upright", "reverse"]
    # card_num = [1,3]
    
    def __init__(self):
        self.deck = Deck()
        self.drawn_cards = []
        
    def shuffle(self):
        self.deck.shuffle()
        
    def draw(self, num):
        if num == 3:
            self.shuffle()
            for i in range(random.choice([1, 3])):
                random.shuffle(self.orientations)
                self.drawn_cards.append((self.deck.pop(),self.orientations[0]))
        elif num == 1:
            self.shuffle()
            random.shuffle(self.orientations)
            self.drawn_cards.append((self.deck.pop(),self.orientations[0]))
        elif num == 2:
            self.shuffle()
            for i in range(3):
                random.shuffle(self.orientations)
                self.drawn_cards.append((self.deck.pop(),self.orientations[0]))
        return self.drawn_cards
            
from openai import OpenAI


class TarotInterpreter:

    def __init__(self):
        self.client = OpenAI()

    def create_message(self, drawn_cards, question):
        card_descriptions = []

        for card, orientation in drawn_cards:

            if orientation == "upright":
                meaning = card.upright
            else:
                meaning = card.reverse

            description = (
                f"{card.name} — {orientation}\n"
                f"Meaning: {meaning}"
            )

            card_descriptions.append(description)

        cards_text = "\n\n".join(card_descriptions)

        prompt = f"""
The user asked:
{question}

The cards drawn were:

{cards_text}

Explain how these cards work together and provide one overall
message for the reading.

Keep the interpretation encouraging and reflective.
Do not claim that the future is guaranteed.
Use clear language and write approximately two to four paragraphs.
"""

        response = self.client.responses.create(
            model="gpt-5.6",
            instructions=(
                "You are a thoughtful tarot reader who interprets tarot "
                "as a tool for reflection, insight, and personal guidance."
            ),
            input=prompt
        )

        return response.output_text       
        
    
def main():
    # Create the API interpreter once
    interpreter = TarotInterpreter()

    print("==============================")
    print("      TAROT CARD READER")
    print("==============================")

    while True:
        # Create a fresh deck for every reading
        reading = Reading()

        print("\nChoose your reading:")
        print("1. One-card reading")
        print("2. Three-card reading")
        print("3. Random reading")

        choice = input("\nEnter 1, 2, or 3: ").strip()

        if choice == "1":
            number_of_cards = 1

        elif choice == "2":
            number_of_cards = 2

        elif choice == "3":
            number_of_cards = 3
            print(
                f"\nThe program selected a "
                f"{number_of_cards}-card reading."
            )

        else:
            print("\nPlease enter 1, 2, or 3.")
            continue

        question = input(
            "\nWhat question would you like guidance about?\n"
            "Press Enter for a general reading: "
        ).strip()

        if question == "":
            question = "What general guidance should I focus on right now?"

        drawn_cards = reading.draw(number_of_cards)

        print("\n========== YOUR CARDS ==========")

        for card, orientation in drawn_cards:
            print("\n--------------------")
            print(card.name)
            print("Orientation:", orientation)

            if orientation == "upright":
                print("Meaning:", card.upright)
            else:
                print("Meaning:", card.reverse)

        print("\nCreating your overall interpretation...")

        try:
            overall_message = interpreter.create_message(
                drawn_cards,
                question
            )

            print("\n========== OVERALL MESSAGE ==========")
            print(overall_message)

        except Exception as error:
            print("\nThe overall message could not be generated.")
            print("Your individual card results are still shown above.")
            print("Error:", error)

        while True:
            continue_choice = input(
                "\nWould you like another reading? (yes/no): "
            ).strip().lower()

            if continue_choice in ["yes", "y"]:
                break

            elif continue_choice in ["no", "n"]:
                print("\nThank you for using the tarot reader!")
                return

            else:
                print("Please enter yes or no.")


if __name__ == "__main__":
    main()
    

        


