import random
from models.karakter import Hero
from engine.game_manager import GameManager


def MainMenu():
    print("\n===========================")
    print("   RPG CLI - MENU UTAMA   ")
    print("===========================")
    print("1. Lihat Status Karakter")
    print("2. Mulai Petualangan")
    print("3. Lihat Inventory")
    print("4. Keluar Game")
    print("----------------------------")


gameLogic = GameManager()
Player = gameLogic.load_data_hero()

if Player is not None:
    print(f"Selamat Datang Kembali, {Player.nama}!")
else:
    print("Selamat Datang di RPG CLI!")
    nama = input("Masukkan nama karakter Anda : ")
    hp = 100
    rand_attack = round(random.uniform(10, 30), 2)
    rand_def = round(random.uniform(5, 15), 2)

    Player = Hero(nama, hp, hp, rand_attack, rand_def)


while True:
    MainMenu()
    pilihanMenu = str(input("Pilih menu yang tersedia diatas: ")).lower()

    if pilihanMenu == "1":
        Player.TampilkanStatus()
    elif pilihanMenu == "2":
        monster = gameLogic.cari_musuh(Player)
        gameLogic.Battle(Player, monster)
    elif pilihanMenu == "3":
        Player.TampilkanInventory()
    elif pilihanMenu == "4" or pilihanMenu == "exit":
        gameLogic.save_data(Player)
        print("\nTerima kasih sudah bermain! Sampai jumpa.")
        break
    else:
        print("\nPilihan tidak valid! cek lagi menu yang tersedia diatas!")
