import json
import random
import os
from models.karakter import Karakter, Hero
from models.item import Item, Rarity_drop_chance


class GameManager:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.items_data = self.load_json(
            os.path.join(self.BASE_DIR, "data", "items.json")
        )
        self.monsters_data = self.load_json(
            os.path.join(self.BASE_DIR, "data", "monsters.json")
        )
        self.save_path = os.path.join(self.BASE_DIR, "data", "savegame.json")

    def load_json(self, path_file):
        try:
            with open(path_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File data di {path_file} tidak ditemukan!")
            return {}

    def spawn_monster(self, monster_key):
        # print(f"DEBUG: monster_key yang diminta -> '{monster_key}'")
        # print(f"DEBUG: Key yang TERSEDIA di JSON -> {list(self.monsters_data.keys())}")
        data = self.monsters_data.get(monster_key)
        if not data:
            return None

        return Karakter(
            nama=data["nama"],
            hp=data["max_hp"],
            max_hp=data["max_hp"],
            attack=data["attack"],
            defend=data["defend"],
        )

    def cari_musuh(self, player):
        if not self.monsters_data:
            print("[ERROR] Data monsters.json kosong!")
            return "slime"  # Fallback default jika json kosong

        # Ambil pity player, jika belum ada set ke 0
        current_pity = getattr(player, "boss_pity", 0)
        peluang_boss = 10 + (current_pity * 15)
        dice = random.randint(1, 100)

        print("\nMenjelajahi area...")

        # Kumpulan Boss
        boss_pool = ["cerberus", "red_dragon"]
        # Kumpulan Monster Biasa
        normal_pool = ["slime", "undead", "zombie", "orc", "golem"]

        # Cek apakah dapat Boss
        if dice <= peluang_boss or current_pity >= 50:
            print("⚠️ PERINGATAN! AURA MENCEKAM MUNCUL! (BOSS ENCOUNTER) ⚠️")
            player.boss_pity = 0  # Reset pity
            terpilih = random.choice(boss_pool)
        else:
            player.boss_pity = current_pity + 1  # Tambah pity
            terpilih = random.choice(normal_pool)

        # PASTIKAN BARIS RETURN INI ADA DAN TIDAK PADA BLOK TERSEMBUNYI!
        return terpilih

    def random_drop(self, monster_key):
        monster = self.monsters_data.get(monster_key)
        if not monster or "drop_list" not in monster:
            return []
        # Get Rarity list drop from monster
        list_rarity = []
        rarity_weights = []

        for rarity in monster["drop_list"]:
            drop_weight = Rarity_drop_chance.get(rarity, 0)
            if drop_weight > 0:
                list_rarity.append(rarity)
                rarity_weights.append(drop_weight)

        if not list_rarity:
            return []

        # randomize rarity untuk drop
        rarity_selected = random.choices(list_rarity, weights=rarity_weights, k=1)[0]

        # Bagi rata weight ke pool item dengan rarity yang sama
        item_pool = [
            key
            for key, detail in self.items_data.items()
            if detail.get("rarity") == rarity_selected
        ]

        # get attribute from selected item from item pool
        if item_pool:
            selected_item = random.choice(item_pool)
            item_data = self.items_data[selected_item]

            items = Item(
                nama=item_data["nama"],
                tipe=item_data["tipe"],
                efek=item_data["efek"],
                jenis_efek=item_data["jenis_efek"],
                rarity=item_data["rarity"],
            )
            return [items]
        return []

    def buka_inventory(self, player):
        if not player.inventory:
            print("\n🎒 Tas kamu kosong!")
            return False

        potion_list = [
            item
            for item in player.inventory
            if item.tipe.lower() in ["potion", "consumable"]
        ]

        if not potion_list:
            print("\n Kamu tidak memiliki Potion / Consumable di dalam inventory!")
            return False

        print("\n===========================")
        print("    POTION & CONSUMABLES      ")
        print("===========================")

        grouped_inventory = {}
        for item in potion_list:
            if item.nama in grouped_inventory:
                grouped_inventory[item.nama]["qty"] += 1
            else:
                grouped_inventory[item.nama] = {"item_object": item, "qty": 1}

        items_list = []
        no = 1
        for nama_item, data in grouped_inventory.items():
            obj = data["item_object"]
            qty = data["qty"]
            items_list.append(obj)

            print(
                f"{no}. {obj.nama} (x{qty}) [{obj.tipe.upper()}] -> +{obj.efek} {obj.jenis_efek}"
            )
            no += 1

        print("0. Kembali")
        pilihan = input("Pilih item: ").strip()

        if pilihan == "0" or not pilihan.isdigit():
            return False

        idx = int(pilihan) - 1
        if 0 <= idx < len(items_list):
            item_terpilih = items_list[idx]

            if item_terpilih.tipe.lower() == "potion":
                player.use_consumable(item_terpilih)
                return True

        print("❌ Pilihan tidak valid.")
        return False

    def Battle(self, player, monster_key):
        monster = self.spawn_monster(monster_key)
        if not monster:
            print(
                f"Monster dengan key '{monster_key}' tidak ditemukan di database sistem!"
            )
            return

        player.hp = player.max_hp

        print(f"\n[BATTLE START] {player.nama} vs {monster.nama}!")
        print(
            f"Status {monster.nama} - HP: {monster.hp}, ATK: {monster.attack}, DEF: {monster.defend}"
        )

        turn = 1
        while player.hp > 0 and monster.hp > 0:
            print(f"\n--- Turn {turn} ---")
            print(
                f"HP {player.nama}: {max(0, round(player.hp))}/{player.max_hp} | HP {monster.nama}: {max(0, round(monster.hp))}/{monster.max_hp}"
            )
            print("1. Serang Musuh")
            print("2. Buka Inventory (Belum Tersedia)")

            pilihan = input("Pilih tindakan Anda: ")
            action_done = False

            match pilihan.strip():
                case "1":
                    current_monster_hp = player.Serang(monster)
                    print(
                        f"💥 {player.nama} menyerang {monster.nama}! Sisa HP {monster.nama}: {max(0, current_monster_hp)}"
                    )

                    if monster.hp <= 0:
                        print(f"\n🎉 Selamat! {monster.nama} berhasil dikalahkan!")
                        hadiah = self.random_drop(monster_key)
                        if hadiah:
                            for item in hadiah:
                                player.inventory.append(item)
                                print(
                                    f"🎁 Anda mendapatkan item: [{item.rarity}] {item.nama}!"
                                )
                        else:
                            print(
                                "💨 Sayang sekali, monster tidak menjatuhkan item apa pun kali ini."
                            )
                        break
                    action_done = True

                case "2":
                    action_done = self.buka_inventory(player)
                    if not action_done:
                        print(" ⚠️ Batal menggunakan/memasang item.")
                        continue

                case _:
                    print("Pilihan tidak valid! Harap masukkan menu yang tersedia.")

            # Monster menyerang balik
            if action_done and monster.hp > 0:
                current_player_hp = monster.Serang(player)
                print(
                    f"🥊 {monster.nama} menyerang balik! Sisa HP {player.nama}: {max(0, current_player_hp)}"
                )
                if player.hp <= 0:
                    print(f"\n💀 Anda mati terbunuh oleh {monster.nama}!")
                    break

            turn += 1

        print(f"\nPertarungan selesai dalam {turn} turn/ronde.")
        print("[BATTLE END] Kembali ke Menu Utama.")

    def save_data(self, player):
        save_data = {
            "nama": player.nama,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack": player.attack,
            "defend": player.defend,
            "inventory": [],
        }

        for item in player.inventory:
            inventory_data = {
                "nama": item.nama,
                "tipe": item.tipe,
                "efek": item.efek,
                "jenis_efek": item.jenis_efek,
                "rarity": item.rarity,
            }

            save_data["inventory"].append(inventory_data)

        with open(self.save_path, "w") as file:
            json.dump(save_data, file, indent=4)

        print("\n[SYSTEM] Game Saved")

    def load_data_hero(self):
        if not os.path.exists(self.save_path):
            return None

        with open(self.save_path, "r") as file:
            save_data = json.load(file)

        loaded_data = Hero(
            nama=save_data["nama"],
            hp=save_data["hp"],
            max_hp=save_data["max_hp"],
            attack=save_data["attack"],
            defend=save_data["defend"],
        )

        for item in save_data.get("inventory", []):
            items = Item(
                nama=item["nama"],
                tipe=item["tipe"],
                efek=item["efek"],
                jenis_efek=item["jenis_efek"],
                rarity=item["rarity"],
            )
            loaded_data.inventory.append(items)

        return loaded_data
