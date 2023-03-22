import msvcrt
import os
import chat
from cryptography.fernet import Fernet

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Menu():
    def __init__(self):
        self.options={
            1: "Join room",
            2: "Create rooom",
            3: "Generate encrpytion key",
            4: "Exit"
        }

        self.options_functions = [
            self.join_room,
            self.create_room,
            self.generate_key,
            self.menu_exit
        ]

    def join_room(self):
        cls()
        channel=input("Channel: ")
        nickname=input("Enter your nickname: ")
        crypto_key=input("Enter your symmetric key: ")
        chat.run(nickname, crypto_key, input_channel=channel)

    def create_room(self):
        cls()
        print("Create room")
        nickname = input("Enter your nickname: ")
        crypto_key = input("Enter your symmetric key: ")
        chat.run(nickname, crypto_key, create_channel_flag=True)

    def generate_key(self):
        cls()
        key = Fernet.generate_key()
        print("This is your symmetric key. Keep it in a safe place.")
        print(key.decode())
        print("\nUse enter to return to menu")
        input()

    def menu_exit(self):
        cls()
        exit()

    def main_menu(self):
        while True:
            cls()
            for key in self.options.keys():
                print(f'{key}. {self.options[key]}')

            option=int(msvcrt.getch())
            print(option)

            if option in self.options.keys():
                self.options_functions[option-1]()

if __name__ == '__main__':
    m=Menu()
    m.main_menu()