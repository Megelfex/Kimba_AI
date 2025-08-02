class ThemeManager:
    THEMES = {
        "ghibli": {
            "background": "#E6E2AF",
            "text": "#046380",
            "accent": "#A7A37E",
            "highlight": "#E85A4F"
        },
        "dark": {
            "background": "#1E1E1E",
            "text": "#FFFFFF",
            "accent": "#FFB86C",
            "highlight": "#FF5555"
        }
    }

    def __init__(self, theme_name="ghibli"):
        self.theme = self.THEMES.get(theme_name, self.THEMES["ghibli"])

    def get(self, key):
        return self.theme.get(key)
