def adjust_response_by_mood(response, mood):
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
        return response  # neutral oder unbekanntes Mood

# Beispiel zur Nutzung:
if __name__ == "__main__":
    print(adjust_response_by_mood("Ich habe deinen Ordner sortiert.", "verspielt"))
