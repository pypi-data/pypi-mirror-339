"""
openf5-utils
Copyright (c) 2025 mrfakename. All rights reserved.
"""


class IPAPhonemizer:
    def __init__(self, lang="en-us"):
        """
        Initialize the IPAPhonemizer with a specified language.

        Args:
            lang (str): Language code to use for phonemization (default: "en-us")
        """
        from gruut import sentences

        self.sentences = sentences
        self.lang = lang

    def phonemize(self, text: str) -> str:
        """
        Convert text to IPA phonemes.

        Args:
            text (str): The input text to phonemize

        Returns:
            str: The phonemized text as a string of IPA symbols in phonemizer format
        """
        result = []

        for sent in self.sentences(text, lang=self.lang):
            sentence_parts = []
            for word in sent:
                if word.phonemes:
                    # Join phonemes without spaces between them
                    phonemes = "".join(word.phonemes)
                    sentence_parts.append(phonemes)
                else:
                    sentence_parts.append(word.text)

            # Join words with spaces and add sentence end marker
            result.append(" ".join(sentence_parts))

        # Join sentences with appropriate separator
        return " ".join(result)
