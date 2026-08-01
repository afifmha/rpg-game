import json
import os

class LocaleManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocaleManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, default_lang="id"):
        if self._initialized:
            return
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.locale_dir = os.path.join(self.BASE_DIR, "locale")
        self.current_lang = default_lang
        self.translations = {}
        self.load_translations()
        self._initialized = True

    def load_translations(self):
        file_path = os.path.join(self.locale_dir, f"{self.current_lang}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception:
            self.translations = {}

    def set_language(self, lang):
        if lang in ["en", "id"]:
            self.current_lang = lang
            self.load_translations()
            return True
        return False

    def t(self, key, **kwargs):
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

# Global instance
locale_manager = LocaleManager()
