def get_quote(emotion):
    quotes = {
        "Happy": "Keep smiling! Your happiness inspires everyone 😊",
        "Sad": "Don't worry, tough times never last 💪",
        "Angry": "Take a deep breath and stay calm 🧘",
        "Surprise": "Life is full of surprises 😲",
        "Neutral": "Stay focused and keep going 👍"
    }
    return quotes.get(emotion, "Stay positive ✨")