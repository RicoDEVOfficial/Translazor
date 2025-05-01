from googletrans import Translator as GoogleTranslator

class Translator:
    def __init__(self):
        self._tr = GoogleTranslator()

    def translate(self, text: str, src: str, dest: str) -> str:
        res = self._tr.translate(text, src=src, dest=dest)
        return res.text
