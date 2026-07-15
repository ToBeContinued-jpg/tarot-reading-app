import random
from pathlib import Path

import streamlit as st


from tarot import Reading, TarotInterpreter


# Find the project folder regardless of where the app is run
BASE_DIR = Path(__file__).resolve().parent


st.set_page_config(
    page_title="Tarot Card Reader",
    page_icon="🔮",
    layout="centered"
)


# Set up values that should survive Streamlit reruns
if "drawn_cards" not in st.session_state:
    st.session_state.drawn_cards = None

if "overall_message" not in st.session_state:
    st.session_state.overall_message = None

if "question" not in st.session_state:
    st.session_state.question = None

if "api_error" not in st.session_state:
    st.session_state.api_error = False


st.title("🔮 Tarot Card Reader")

st.write(
    "Choose your reading type, ask a question, "
    "and receive an interpretation of your cards."
)


# A form waits until the button is clicked before processing inputs
with st.form("tarot_reading_form"):

    reading_type = st.radio(
        "Choose a reading:",
        [
            "One-card reading",
            "Three-card reading",
            "Random reading"
        ]
    )

    question = st.text_area(
        "What would you like guidance about?",
        placeholder=(
            "Enter a question, or leave this blank "
            "for a general reading."
        )
    )

    submitted = st.form_submit_button(
        "Draw my cards",
        use_container_width=True
    )


if submitted:

    if reading_type == "One-card reading":
        number_of_cards = 1

    elif reading_type == "Three-card reading":
        number_of_cards = 2

    else:
        number_of_cards = random.choice([1, 3])
        st.info(
            f"The deck selected a "
            f"{number_of_cards}-card reading."
        )

    cleaned_question = question.strip()

    if cleaned_question == "":
        cleaned_question = (
            "What general guidance should I focus on right now?"
        )

    # Create a fresh deck and perform the reading
    reading = Reading()
    drawn_cards = reading.draw(number_of_cards)

    # Save the results so they remain visible after a rerun
    st.session_state.drawn_cards = drawn_cards
    st.session_state.question = cleaned_question
    st.session_state.overall_message = None
    st.session_state.api_error = False

    # Send the finished reading to the API
    with st.spinner("Interpreting your reading..."):

        try:
            interpreter = TarotInterpreter()

            message = interpreter.create_message(
                drawn_cards,
                cleaned_question
            )

            st.session_state.overall_message = message

        except Exception:
            st.session_state.api_error = True


# Display the saved results
if st.session_state.drawn_cards:

    st.header("Your Cards")

    drawn_cards = st.session_state.drawn_cards

    # Make one column per card
    card_columns = st.columns(len(drawn_cards))

    for column, drawn_card in zip(card_columns, drawn_cards):

        card, orientation = drawn_card

        with column:

            st.subheader(card.name)

            # The card.image value should be something such as:
            # images/00-TheFool.png
            image_path = BASE_DIR / card.image

            if image_path.exists():
                st.image(str(image_path))
            else:
                st.warning(
                    f"Image not found: {card.image}"
                )

            st.write(
                f"**Orientation:** {orientation.title()}"
            )

            if orientation == "upright":
                meaning = card.upright
            else:
                meaning = card.reverse

            st.write(f"**Meaning:** {meaning}")


    if st.session_state.overall_message:

        st.divider()
        st.header("Overall Message")
        st.write(st.session_state.overall_message)


    if st.session_state.api_error:

        st.error(
            "The cards were drawn, but the overall "
            "interpretation could not be generated."
        )