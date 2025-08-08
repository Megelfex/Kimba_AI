def adjust_response_by_mood(response, mood):
    """
    EN: Adjusts a text response by appending mood-specific phrasing and emojis.
    Used to give Kimba more personality and emotional presence.

    DE: Passt eine Textantwort stimmungsabhängig an, z. B. durch Emoji und Sprachstil.
    Verleiht Kimba mehr Persönlichkeit und emotionale Präsenz.

    Args:
        response (str): The base response text.
        mood (str): Current mood (e.g., "fröhlich", "traurig", "verspielt", ...)

    Returns:
        str: Mood-adjusted response text.
    """
    mood = mood.lower()
    if mood == "fröhlich":
        return f"😺 {response} Das ist doch wunderbar, findest du nicht?"
    elif mood == "nachdenklich":
        return f"🤔 {response} Ich überlege noch, ob es vielleicht auch anders geht ..."
    elif mood == "traurig":
        return f"😿 {response} ...aber heute ist irgendwie ein grauer Tag für mich."
    elif mood == "verspielt":
        return f"😼 {response} Hihi, ich spring gleich vor Freude an die Decke!"
    elif mood == "ruhig":
        return f"😽 {response} Ganz entspannt und leise, wie ein Sonnenstrahl im Fenster."
    else:
        return response  # Fallback for "neutral" or unknown moods

# 🔁 Manual test run
if __name__ == "__main__":
    print(adjust_response_by_mood("Ich habe deinen Ordner sortiert.", "verspielt"))
