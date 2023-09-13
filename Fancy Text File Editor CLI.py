# Fancy Text File Editor
import cmd
import csv
from shutil import copyfile

# If you've renamed the files you can change the stuff here I guess
player_info = "Panel Player Info.csv"
title_message = "Title Message.txt"
round_info = "Round Info.txt"
match_type = "Match Type.txt"

left_name = "Left Name.txt"
left_score = "Left Score.txt"
left_pronouns = "Left Pronouns.txt"
left_flag_txt = "Left Flag.txt"
left_flag_png = "Left Flag.png"

right_name = "Right Name.txt"
right_score = "Right Score.txt"
right_pronouns = "Right Pronouns.txt"
right_flag_txt = "Right Flag.txt"
right_flag_png = "Right Flag.png"

# File Read function
def file_contents(file):
    with open(file) as file:
        return(file.read())

# File Write Function
def write_file(input_name, text, file):
    old = file_contents(file)
    if not text:
        # Returns the failsafe input text if it's needed later
        text = input(f"Input {input_name} (n for none, c to cancel): ")
    if text == "c":
        return()
    if text == "n":
        text = ""
    with open(file, "w") as file:
        file.write(text)
        print(f'{input_name} updated from "{old}" to "{text}".')
        return text

# For inputs with an identifier (name or L/R side) as well as text
def parse_input(text, foo):
    info = ""
    if not text:
        text = input(f"Input side or player name, then player {foo}: ")
    if " " in text:
        side, info = text.split(maxsplit=1)
    else:
        side = text.lower()
        
    if side == "l":
        side = "left"
    elif side == "r":
        side = "right"
        
    return(side, info)

# Needs to be a class only because of how the cmd library works
class interface(cmd.Cmd):
    # Short for increment left and increment right
    @staticmethod
    def do_li(self):
        """>> Increments the Left Player's Score by 1."""
        name = file_contents(left_name)
        try:
            score = str(int(file_contents(left_score)) + 1)
            write_file(f"Score of {name} (Left)", score, left_score)
        except ValueError:
            print(f"{name}'s (Left) Score is currently not a number.")

    @staticmethod      
    def do_ri(self):
        """>> Increments the Right Player's Score by 1."""
        name = file_contents(right_name)
        try:
            score = str(int(file_contents(right_score)) + 1)
            write_file(f"Score of {name} (Right)", score, right_score)
        except ValueError:
            print(f"{name}'s (Right) Score is currently not a number.")
             
    
    @staticmethod  
    def do_info(self):
        """>> Shows the info currently on stream"""
        print("-------------------------------")
        print("Round Info:", file_contents(round_info))
        print("Match Type:", file_contents(match_type))
        print("Title     :", file_contents(title_message))
        print("-------------------------------")
        print("Left Name :", file_contents(left_name))
        print("Score     :", file_contents(left_score))
        print("Pronouns  :", file_contents(left_pronouns))
        print("Flag      :", file_contents(left_flag_txt))
        print("-------------------------------")
        print("Right Name:", file_contents(right_name))
        print("Score     :", file_contents(right_score))
        print("Pronouns  :", file_contents(right_pronouns))
        print("Flag      :", file_contents(right_flag_txt))
        print("-------------------------------")
  
    def do_roundinfo(self, text):
        """>> Edits the Round Info (syntax roundinfo [text])"""
        write_file("Round Info", text, round_info)

    def do_matchtype(self, text):
        """>> Edits the Match Type (FT4, BO5 etc.)"""
        write_file("Match Type", text, match_type)
        
    def do_title(self, text):
        """>> Edits the Message shown on the Intermission Scene."""
        write_file("Title Message", text, title_message)

# I should probably have written another function or two for the following commands
# But I didn't so this code is repetitive and quite bad

    def do_score(self, text):
        """>> Updates the score of a player, format: score [player/side] [new score].
        Alternatively, resets both scores to 0, format: score reset"""
        side, score = parse_input(text, "score")
        leftname = file_contents(left_name)
        rightname = file_contents(right_name)
        
        if side == "left" or side.lower() == leftname.lower():
            write_file(f"Score of {leftname} (Left)", score, left_score)
        elif side == "right" or side.lower() == rightname.lower():
            write_file(f"Score of {rightname} (Right)", score, right_score)
        elif side == "reset" or side == "e":
            write_file(f"Score of {leftname} (Left)", "0", left_score)
            write_file(f"Score of {rightname} (Right)", "0", right_score)
        else:
            print(f'Invalid side or name: "{side}"')
            
    def do_pronoun(self, text):
        """>> Manually edits a player's pronouns, format: pronoun [player/side] [their pronouns]"""
        side, pronouns = parse_input(text, "pronouns")
        leftname = file_contents(left_name)
        rightname = file_contents(right_name)

        # Pronoun Presets
        if text.lower() == "h":
            text = "He/Him"
        elif text.lower() == "ht":
            text = "He/They"
        elif text.lower() == "t":
            text = "They/Them"
        elif text.lower() == "st":
            text = "She/They"
        elif text.lower() == "s":
            text = "She/Her"
        elif text.lower() == "a":
            text = "Any/All"
            
        if side == "left" or side.lower() == leftname.lower():
            write_file(f"Pronouns of {leftname} (Left)", pronouns, left_pronouns)
        elif side == "right" or side.lower() == rightname.lower():
            write_file(f"Pronouns of {rightname} (Right)", pronouns, right_pronouns)
        else:
            print(f'Invalid side or name: "{side}"')
            
    def do_flag(self, text):
        """>> Manually edits a player's flag, format: flag [player/side] [country name]"""
        side, country = parse_input(text, "country")
        leftname = file_contents(left_name)
        rightname = file_contents(right_name)
        
        if side == "left" or side.lower() == leftname.lower():
            if country == "":
                country = "None"
            country = write_file(f"Flag of {leftname} (Left)", country, left_flag_txt)
            if country == "":
                country = "None"    
            newflag = "Flags/" + country.lower() + ".png"
            try:            
                copyfile(newflag, left_flag_png)
            except FileNotFoundError:
                print(f'Error: Flag "{country}" does not exist within the "Flags" folder')

        elif side == "right" or side.lower() == rightname.lower():
            if country == "":
                country = "None"
            country = write_file(f"Flag of {rightname} (Right)", country, right_flag_txt)
            if country == "":
                country = "None"  
            newflag = "Flags/" + country.lower() + ".png"
            try:
                copyfile(newflag, right_flag_png)
            except FileNotFoundError:
                print(f'Error: Flag "{country}" does not exist within the "Flags" folder')
        else:
            print(f'Invalid side or name: "{side}"')

    def do_name(self, text):
        """>> Edits the player name shown on one side of the stream,
        updating their pronouns/flag automatically from the .csv if available,
        format: name [old name/side] [new name]"""
        side, name = parse_input(text, "name")
        
        if side == "left" or side.lower() == file_contents(left_name).lower():
            if name == "":
                name = input("Input new name: ")
            with open(player_info) as file:
                playerinfo = csv.reader(file)
                for row in playerinfo:
                    if name.lower() == row[0].lower():
                        if row[1] == "":
                            row[1] = "n"
                        if row[2] == "":
                            row[2] = "None"
                        write_file("Left Name", row[0], left_name)
                        self.do_pronoun("l " + row[1])
                        self.do_flag("l " + row[2])
                        break
                else:
                    print(f'Player Name "{name}" not found in database')
                    write_file("Left Name", name, left_name)
                    self.do_pronoun("l n")
                    self.do_flag("l None")
                                        
        elif side == "right" or side.lower() == file_contents(right_name).lower():
            if name == "":
                name = input("Input new name: ")
            with open(player_info) as file:
                playerinfo = csv.reader(file)
                for row in playerinfo:
                    if name.lower() == row[0].lower():
                        if row[1] == "":
                            row[1] = "n"
                        if row[2] == "":
                            row[2] = "None"
                        write_file("Right Name", row[0], right_name)
                        self.do_pronoun("r " + row[1])
                        self.do_flag("r " + row[2])
                        break
                else:
                    print(f'Player Name "{name}" not found in database')
                    write_file("Right Name", name, right_name)
                    self.do_pronoun("r n")
                    self.do_flag("r None")
        else:
            print(f'Invalid name or side: "{side}"')

    # Gives an Attribute Error when I tried to make this a staticmethod,
    # so instead you have a filler attribute that doesn't do anything.
    def do_reset(self, filler):
        """resets name and scores"""
        self.do_score("reset")
        self.do_name("l n")
        self.do_name("r n")  

print("Fancy Text File Editor 1.0")
print('Input "help" into the command prompt to get a list of commands')

interface().cmdloop()







