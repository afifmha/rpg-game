import random
from models.karakter import Hero
from engine.game_manager import GameManager
from engine.locale_manager import locale_manager


def main_menu():
    print("\n===========================")
    print(locale_manager.t("menu_title"))
    print("===========================")
    print(locale_manager.t("menu_status"))
    print(locale_manager.t("menu_adventure"))
    print(locale_manager.t("menu_inventory"))
    print(locale_manager.t("menu_exit"))
    print("----------------------------")


game_logic = GameManager()
player = game_logic.load_data_hero()

if player is not None:
    print(locale_manager.t("welcome_back", nama=player.nama))
else:
    # Ask for language preference first
    print("Pilih Bahasa / Select Language:")
    print("1. Bahasa Indonesia (id)")
    print("2. English (en)")
    lang_choice = input("Pilihan / Choice: ").strip()
    if lang_choice == "2":
        locale_manager.set_language("en")
    else:
        locale_manager.set_language("id")

    print(locale_manager.t("welcome_new"))
    nama = input(locale_manager.t("input_name"))
    hp = 100.0
    rand_attack = round(random.uniform(10, 30), 2)
    rand_def = round(random.uniform(5, 15), 2)

    player = Hero(nama, hp, hp, rand_attack, rand_def)


while True:
    main_menu()
    pilihan_menu = str(input(locale_manager.t("select_menu"))).lower()

    if pilihan_menu == "1":
        player.tampilkan_status()
        if player.stat_points > 0:
            pilihan_allocate = input(locale_manager.t("allocate_prompt")).strip().lower()
            if pilihan_allocate in ["y", "ya", "yes"]:
                player.alokasi_stat_points()
    elif pilihan_menu == "2":
        monster = game_logic.cari_musuh(player)
        game_logic.Battle(player, monster)
    elif pilihan_menu == "3":
        # Allow viewing and managing (using/equipping) items from inventory
        game_logic.buka_inventory(player)
    elif pilihan_menu == "4" or pilihan_menu == "exit":
        game_logic.save_data(player)
        print(locale_manager.t("exit_message"))
        break
    else:
        print(locale_manager.t("invalid_choice"))
