#######################################################################
# IMPORTS
#######################################################################
from datetime import datetime, timedelta
import string
import random
import vigenere
from geopy import Nominatim
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.core.window import Window

######################################################################
# Set Window Size
######################################################################
Window.size = (360, 680)


######################################################################
# MAIN FUNCTIONS
######################################################################
class MyLayout(BoxLayout):
    ##################################################################
    # PORT SCANNER FUNCTIONS *** IN NEXT VERSION ***
    ##################################################################
    # PASSWORD GENERATOR
    ##################################################################
    def passwordgen(self):
        char_to_replace = {'a': '@', 'e': '3', 'i': '!', 's': '$'}
        result = ''
        with open("wordlist.txt", "r") as file:
            allText = file.read()
            allText = list(map(str, allText.split()))

        # Using list comprehension to loop through the text and only pick words where len == 4-7 characters
        words = [i for i in allText if 4 <= len(i) <= 7]

        # Grabs 4 words from the wordlist adding them to pwj
        pwj = random.choices(words, k=4)

        # Displays the words before character substitution.
        self.ids.passgen_words.text = ' '.join(pwj)
        pw = ''.join(pwj)

        # Iterate over all characters in string
        for char in pw:
            # Check if character is in dict as key
            if char in char_to_replace:
                # If yes then add the value of that char
                # from dict to the new string
                result += char_to_replace[char]
            else:
                # If not then add the character in new string
                result += char

        self.ids.passgen_output.text = result

    ##################################################################
     # BINARY CONVERTER
    ##################################################################
    def flip(self):  # flip button function for conversion screen. This function changes the state.
        if self.state == 0:
            self.state = 1
            self.ids.con_title.text = "Decimal to Binary"
            self.ids.con_input.hint_text = "enter a decimal number"
            self.ids.con_input.text = ""
            self.ids.con_results.text = ""
            self.ids.con_results_title.text = ""
        elif self.state == 1:
            self.state = 2
            self.ids.con_title.text = "String to Binary"
            self.ids.con_input.hint_text = "enter a string"
            self.ids.con_input.text = ""
            self.ids.con_results.text = ""
            self.ids.con_results_title.text = ""
        elif self.state == 2:
            self.state = 0
            self.ids.con_title.text = "Binary to Decimal"
            self.ids.con_input.hint_text = "enter a binary number"
            self.ids.con_input.text = ""
            self.ids.con_results.text = ""
            self.ids.con_results_title.text = ""

    def convert(self):  # Binary converter that switches between different states of conversion
        try:
            if "." not in self.ids.con_input.text:
                if self.state == 0:
                    val = int(self.ids.con_input.text, 2)
                    self.ids.con_results.text = str(val)
                    self.ids.con_results_title.text = "in decimal"
                elif self.state == 1:
                    val = bin(int(self.ids.con_input.text))[
                          2:]  # every bin cenvertion returns a string. EXAMPLE: bin(int("8"))= 0b1000. So to remove the 0b from the string we use slice.
                    self.ids.con_results_title.text = "in binary"
                    self.ids.con_results.text = val
                elif self.state == 2:
                    val = ''.join('{0:08b}'.format(ord(x), 'b') for x in self.ids.con_input.text)
                    self.ids.con_results_title.text = "in binary"
                    self.ids.con_results.text = val
                    if val == "":
                        self.ids.con_results_title.text = "please enter at least one character"


            else:
                # floating point numbers conversion
                whole, fract = self.ids.con_input.text.split(".")

                if self.state == 0:
                    # convert binary to decimal
                    whole = int(whole, 2)
                    floating = 0
                    for idx, digit in enumerate(fract):
                        floating += int(digit) * 2 ** (-(idx + 1))
                    self.ids.con_results_title.text = "in decimal"
                    self.ids.con_results.text = str(whole + floating)

                else:
                    # convert decimal to binary
                    decimal_places = 10
                    whole = bin(int(whole))[2:]
                    fract = float("0." + fract)
                    floating = []
                    for i in range(decimal_places):
                        if fract * 2 < 1:
                            floating.append("0")
                            fract *= 2
                        elif fract * 2 > 1:
                            floating.append("1")
                            fract = fract * 2 - 1
                        elif fract * 2 == 1.0:
                            floating.append("1")
                            break
                    self.ids.con_results_title.text = "in binary"
                    self.ids.con_results.text = whole + "." + "".join(floating)
        except ValueError:
            self.ids.con_results.text = ""
            if self.state == 0:
                self.ids.con_results_title.text = "please enter a valid binary number"
            elif self.state == 1:
                self.ids.con_results_title.text = "please enter a valid decimal number"

    ##################################################################
    # SECRET MEETING
    ##################################################################
    def cryptofunction(self):
        '''geolocator = Nominatim(user_agent="geoapiExercises")
                Latitude = "40.41402"
                Longitude = "-3.708136"
                location = geolocator.reverse(Latitude + "," + Longitude)
                address = location.raw['address']
                City = address.get('city')'''
        # Generating meeting in plaintext from datetime and city
        rd = random.randrange(7)
        Otherday = datetime.today() + timedelta(days=rd)
        Key = Otherday.strftime('%A')

        with open("city.txt", "r") as file:
            allCities = file.read()
            cities = list(map(str, allCities.split()))
        City = random.choice(cities)
        Meeting = f"{City, Key}"

        # PLAIN TEXT
        Meeting = Meeting.replace(' ', '')
        Meeting = Meeting.lower()

        # PLAINTEXT KEY
        CypherKey = datetime.today() + timedelta(days=-1)
        CypherKey = CypherKey.strftime('%A')
        CypherKey = CypherKey.lower()

        # importing functions from vigenere.py
        vc = vigenere.Vigenere()

        keyword = str(CypherKey)

        plaintext = str(Meeting)

        enciphered = vc.encipher(plaintext, keyword)

        deciphered = vc.decipher(enciphered, keyword)
        self.keyword_s = keyword
        self.deciphered_s = deciphered
        self.ids.crypto_text.text = str(enciphered)

    def check_crypto(self):  # Check user input for if it matches with the keyword
        crypto_input = self.ids.crypto_flag.text

        if crypto_input == str(self.keyword_s):
            self.ids.crypto_text.text = str(self.deciphered_s)
            self.ids.crypto_hint.text = "NOW WE KNOW WHERE THEY ARE GOING TO BE!"
            self.ids.cry_btn.disabled = True
            self.flagprogress()
            self.show_cry_dialog()
        else:
            toast("Sorry, that is not the right key! Please try again.")

    def show_cry_dialog(self):  # Show Back in time dialog
        self.dialog = MDDialog(
            radius=[20, 7, 20, 7],
            md_bg_color=(72 / 255, 169 / 255, 175 / 255, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            title="YOU GOT ANOTHER FLAG!",
            text="25 more points added!",
            type="confirmation",

        )
        self.dialog.open()

    ##################################################################
    # FLAG PROGRESS BAR
    ##################################################################
    def flagprogress(self):  # Updates the progress bar value with +25 on every completed flag!

        current = self.ids.progress_bar.value
        current += 25
        self.ids.progress_bar.value = current
        self.ids.progress_bar_text.text = f"Progress: {str(current)}/100.0"

        if current == 50:  # Unlocks new functions as you gain more points.
            self.ids.bin_converter.disabled = False
        elif current >= 50:
            self.ids.passgenerator.disabled = False
        elif current == 100:
            self.ids.game.disabled = False
        else:
            toast("You unlock more functions as you gain more points.")

    ##################################################################
    # BACK IN TIME CHALLENGE
    ##################################################################
    def check_bit(self):  # Check user input for flag. And
        bit_input = self.ids.bit_flag.text

        if bit_input == "1853":
            self.ids.bit_text.text = "The first telegraph line between two cities was completed in 1844, and the first one between two cities in Sweden was completed in 1853. And connected Stockholm to Uppsala."
            self.ids.bit_btn.disabled = True
            self.flagprogress()
            self.show_bit_dialog()
        else:
            toast("Sorry, that is not the right key! Please try again.")

    def show_bit_dialog(self):  # Show Back in time dialog
        self.dialog = MDDialog(
            radius=[20, 7, 20, 7],
            md_bg_color=(72 / 255, 169 / 255, 175 / 255, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            title="YOU GOT ANOTHER FLAG!",
            text="25 more points added!",
            type="confirmation",

        )
        self.dialog.open()

    ##################################################################
    # LOGIN METHODS AND FUNCTIONALITIES
    ##################################################################
    def check_data_login(self):  # Login Authentication function
        dialog = None
        sosecret = f"{str(datetime.now().hour)}${str(datetime.now().strftime('%M'))}cents"
        self.secret = sosecret

        print(self.secret)

        username = self.ids['username'].text
        password = self.ids['password'].text
        print(username)
        print(password)
        if not username and not password:
            toast("Username and password are required")
        elif not username:
            toast("Username is required ")
        elif not password:
            toast("Password is required")
        else:
            #if username == "admin" and password == self.secret:
            if username == "admin" and password == "admin":

                self.change_screen("home")
                self.flagprogress()
                self.show_login_dialog()
                self.cryptofunction()
                self.state = 0
                self.flip()

            else:
                toast("Wrong username or password, TIME IS $ and cents!")

    def change_screen(self, screen, *args):  # Change Screen function
        self.scr_mngr.current = screen

    def show_login_dialog(self):  # Show confirmation dialog
        self.dialog = MDDialog(
            radius=[20, 7, 20, 7],
            md_bg_color=(72 / 255, 169 / 255, 175 / 255, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            title="FIRST FLAG IN THE BAG!",
            text="You now have 25/100 points!",
            type="confirmation",

        )
        self.dialog.open()


########################################################################
# MAIN App Class
########################################################################
class HackNMove(MDApp):
    def build(self):  # Build function that returns screen
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        screen = Builder.load_file("main.kv")

        return screen


if __name__ == '__main__':
    HackNMove().run()
