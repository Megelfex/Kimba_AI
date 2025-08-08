class KimbaMemory:
    """
    EN: Simple in-memory store for short-term or session-based message tracking.
    DE: Einfacher In-Memory-Speicher zur kurzzeitigen oder sitzungsbasierten Nachrichtenverfolgung.
    """

    def __init__(self, storage_path):
        """
        EN: Initializes the memory with a given storage path (currently unused).
        DE: Initialisiert den Speicher mit einem angegebenen Pfad (derzeit ungenutzt).

        Args:
            storage_path (str): Placeholder path for future file-based persistence.
        """
        self.storage_path = storage_path
        self.log = []

    def remember(self, message):
        """
        EN: Stores a message in the memory log.
        DE: Speichert eine Nachricht im Speicherprotokoll.

        Args:
            message (str): The message or input to store.
        """
        self.log.append(message)

    def recall(self):
        """
        EN: Returns all remembered messages in order.
        DE: Gibt alle gespeicherten Nachrichten in Reihenfolge zurück.

        Returns:
            list[str]: Stored message log.
        """
        return self.log
