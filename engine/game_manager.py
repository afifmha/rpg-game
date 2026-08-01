import json
import random
import os
from models.karakter import Karakter, Hero
from models.item import Item, Rarity_drop_chance
from engine.locale_manager import locale_manager


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
            print(locale_manager.t("file_not_found", path=path_file))
            return {}

    def spawn_monster(self, monster_key):
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
            print(locale_manager.t("monsters_empty"))
            return "slime"

        current_pity = getattr(player, "boss_pity", 0)
        peluang_boss = 10 + (current_pity * 15)
        dice = random.randint(1, 100)

        print(locale_manager.t("exploring"))

        boss_pool = ["cerberus", "red_dragon"]
        normal_pool = ["slime", "undead", "zombie", "orc", "golem"]

        if dice <= peluang_boss or current_pity >= 50:
            print(locale_manager.t("boss_warning"))
            player.boss_pity = 0
            terpilih = random.choice(boss_pool)
        else:
            player.boss_pity = current_pity + 1
            terpilih = random.choice(normal_pool)

        return terpilih

    def random_drop(self, monster_key):
        monster = self.monsters_data.get(monster_key)
        if not monster or "drop_list" not in monster:
            return []

        list_rarity = []
        rarity_weights = []

        for rarity in monster["drop_list"]:
            drop_weight = Rarity_drop_chance.get(rarity, 0)
            if drop_weight > 0:
                list_rarity.append(rarity)
                rarity_weights.append(drop_weight)

        if not list_rarity:
            return []

        rarity_selected = random.choices(list_rarity, weights=rarity_weights, k=1)[0]

        item_pool = [
            key
            for key, detail in self.items_data.items()
            if detail.get("rarity") == rarity_selected
        ]

        if item_pool:
            selected_item = random.choice(item_pool)
            item_data = self.items_data[selected_item]

            item_obj = Item.create(
                nama=item_data["nama"],
                tipe=item_data["tipe"],
                efek=item_data["efek"],
                jenis_efek=item_data["jenis_efek"],
                rarity=item_data["rarity"],
            )
            return [item_obj]
        return []

    def buka_inventory(self, player):
        if not player.inventory:
            print(locale_manager.t("bag_empty"))
            return False

        print("\n===========================")
        print(locale_manager.t("potion_title"))
        print("===========================")

        # List all items in inventory
        items_list = list(player.inventory)
        for idx, item in enumerate(items_list, 1):
            print(
                f"{idx}. {item.nama} [{item.tipe.upper()}] -> +{item.efek} {item.jenis_efek} ({item.rarity})"
            )

        print(locale_manager.t("go_back"))
        pilihan = input(locale_manager.t("choose_item")).strip()

        if pilihan == "0" or not pilihan.isdigit():
            return False

        idx = int(pilihan) - 1
        if 0 <= idx < len(items_list):
            item_terpilih = items_list[idx]
            if item_terpilih.tipe.lower() in ["potion", "consumable"]:
                player.use_consumable(item_terpilih)
                return True
            elif item_terpilih.tipe.lower() in ["weapon", "armor"]:
                player.equip_item(item_terpilih)
                return True

        print(locale_manager.t("invalid_selection"))
        return False

    def Battle(self, player, monster_key):
        monster = self.spawn_monster(monster_key)
        if not monster:
            print(locale_manager.t("monster_not_found", monster_key=monster_key))
            return

        player.hp = player.max_hp

        print(
            locale_manager.t(
                "battle_start", player=player.nama, monster=monster.nama
            )
        )
        print(
            locale_manager.t(
                "battle_monster_status",
                monster=monster.nama,
                hp=monster.hp,
                attack=monster.attack,
                defend=monster.defend,
            )
        )

        turn = 1
        while player.hp > 0 and monster.hp > 0:
            print(locale_manager.t("battle_turn_header", turn=turn))
            print(
                locale_manager.t(
                    "battle_hp_status",
                    player=player.nama,
                    player_hp=max(0.0, round(player.hp, 2)),
                    player_max_hp=player.max_hp,
                    monster=monster.nama,
                    monster_hp=max(0.0, round(monster.hp, 2)),
                    monster_max_hp=monster.max_hp,
                )
            )
            print(locale_manager.t("battle_action_attack"))
            print(locale_manager.t("battle_action_inventory"))

            pilihan = input(locale_manager.t("battle_choose_action"))
            action_done = False

            match pilihan.strip():
                case "1":
                    current_monster_hp = player.serang(monster)
                    print(
                        locale_manager.t(
                            "battle_attack_player",
                            player=player.nama,
                            monster=monster.nama,
                            hp=max(0.0, current_monster_hp),
                        )
                    )

                    if monster.hp <= 0:
                        print(
                            locale_manager.t(
                                "battle_defeat_monster", monster=monster.nama
                            )
                        )
                        hadiah = self.random_drop(monster_key)
                        if hadiah:
                            for item in hadiah:
                                player.inventory.append(item)
                                print(
                                    locale_manager.t(
                                        "battle_drop_item",
                                        rarity=item.rarity,
                                        nama=item.nama,
                                    )
                                )
                        else:
                            print(locale_manager.t("battle_no_drop"))
                        break
                    action_done = True

                case "2":
                    action_done = self.buka_inventory(player)
                    if not action_done:
                        print(locale_manager.t("battle_cancel_item"))
                        continue

                case _:
                    print(locale_manager.t("battle_invalid_action"))

            # Monster menyerang balik
            if action_done and monster.hp > 0:
                current_player_hp = monster.serang(player)
                print(
                    locale_manager.t(
                        "battle_attack_monster",
                        monster=monster.nama,
                        player=player.nama,
                        hp=max(0.0, current_player_hp),
                    )
                )
                if player.hp <= 0:
                    print(
                        locale_manager.t(
                            "battle_defeat_player", monster=monster.nama
                        )
                    )
                    break

            turn += 1

        print(locale_manager.t("battle_end_summary", turn=turn))
        print(locale_manager.t("battle_end"))

    def save_data(self, player):
        save_data = {
            "nama": player.nama,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack": player.attack,
            "defend": player.defend,
            "inventory": [],
            "weapon": player.weapon.to_dict() if player.weapon else None,
            "armor": player.armor.to_dict() if player.armor else None,
            "boss_pity": player.boss_pity,
            "lang": locale_manager.current_lang,
        }

        for item in player.inventory:
            save_data["inventory"].append(item.to_dict())

        with open(self.save_path, "w") as file:
            json.dump(save_data, file, indent=4)

        print(locale_manager.t("system_saved"))

    def load_data_hero(self):
        if not os.path.exists(self.save_path):
            return None

        with open(self.save_path, "r") as file:
            save_data = json.load(file)

        saved_lang = save_data.get("lang", "id")
        locale_manager.set_language(saved_lang)

        loaded_data = Hero(
            nama=save_data["nama"],
            hp=save_data["hp"],
            max_hp=save_data["max_hp"],
            attack=save_data["attack"],
            defend=save_data["defend"],
        )
        loaded_data.boss_pity = save_data.get("boss_pity", 0)

        w_data = save_data.get("weapon")
        if w_data:
            loaded_data.weapon = Item.create(**w_data)

        a_data = save_data.get("armor")
        if a_data:
            loaded_data.armor = Item.create(**a_data)

        for item in save_data.get("inventory", []):
            item_obj = Item.create(
                nama=item["nama"],
                tipe=item["tipe"],
                efek=item["efek"],
                jenis_efek=item["jenis_efek"],
                rarity=item["rarity"],
            )
            loaded_data.inventory.append(item_obj)

        return loaded_data
