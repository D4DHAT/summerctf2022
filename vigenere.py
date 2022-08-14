#######################################################################
# IMPORTS
#######################################################################
import re
#######################################################################
# Cypher Class This class provides methods for enciphering and deciphering text using the Vigenere cipher.
#######################################################################
class Vigenere(object):

    def __init__(self):

        self.tabularecta = self.create_tabula_recta()

    # Creating the tabula recta object.

    def create_tabula_recta(self):

        tabularecta = []

        for r in range(0, 26): # Generating the rows in the tabula recta

            offset = 0
            row = []

            for column in range(0, 26): # Generating the cols in the tabula recta
                row.append(chr(r + 65 + offset))
                offset += 1
                if offset > (25 - r):
                    offset = offset - 26

            tabularecta.append(row)

        return tabularecta

    def encipher(self, plaintext, keyword): # Enciphering the plaintext. From the input in the main.py subclass.
        plaintext = self.process_plaintext(plaintext)
        keywordrepeated = self.get_keyword_repeated(keyword, len(plaintext))
        ciphertext = []

        for index, letter in enumerate(plaintext): # Using the index in the tabularecta to cipher each letter in the string.

            plaintextindex = ord(letter.upper()) - 65
            keywordindex = ord(keywordrepeated[index]) - 65

            encipheredletter = self.tabularecta[keywordindex][plaintextindex]

            ciphertext.append(encipheredletter)

        return "".join(ciphertext) # Removing the spacing and joining the string.

    def decipher(self, ciphertext, keyword):
        # Decrypts the ciphertext using the keyword from the input in the main.py subclass.
        # And presenting the decrypted ciphertext.

        keywordrepeated = self.get_keyword_repeated(keyword, len(ciphertext))
        decipheredtext = []

        for index, letter in enumerate(ciphertext):

            keywordindex = ord(keywordrepeated[index]) - 65
            decipheredletter = chr(self.tabularecta[keywordindex].index(letter) + 65)

            decipheredtext.append(decipheredletter)

        return "".join(decipheredtext)

    def process_plaintext(self, plaintext):
        # Processes the plaintext to display uppercase letters and removing any spacing.

        plaintext = plaintext.upper()
        plaintext = re.sub("[^A-Z]", "", plaintext)

        return plaintext

    def get_keyword_repeated(self, keyword, length):
        # Changing the length of the keyword by repeating itself until it matches the length of the plaintext.

        keyword = keyword.upper()
        keywordrepeated = []
        keywordlength = len(keyword)
        keywordindex = 0

        for i in range(0, length):
            keywordrepeated.append(keyword[keywordindex])
            keywordindex += 1
            if keywordindex > keywordlength - 1:
                keywordindex = 0

        return "".join(keywordrepeated)