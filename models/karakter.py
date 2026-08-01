import random
from engine.locale_manager import locale_manager
from models.item import Weapon, Armor, Potion

class Karakter:
    def __init__(self, nama: str, hp: float, max_hp: float, attack: float, defend: float):
        self.nama = nama
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defend = defend

    def total_attack(self):
        return round(self.attack, 2)

    def total_armor(self):
        return round(self.defend, 2)

    def serang(self, target):
        # Dodge Check
        if hasattr(target, "get_dodge_chance"):
            dodge_chance = target.get_dodge_chance()
            if random.random() * 100 < dodge_chance:
                print(locale_manager.t("battle_dodge_msg", attacker=self.nama, defender=target.nama))
                return round(target.hp, 2)

        damage = self.total_attack() - target.total_armor()
        if damage <= 0:
            damage = 1

        # Critical Hit Check
        if hasattr(self, "get_crit_chance"):
            crit_chance = self.get_crit_chance()
            if random.random() * 100 < crit_chance:
                print(locale_manager.t("battle_crit_msg"))
                damage *= 2

        target.hp = target.hp - damage
        return round(target.hp, 2)


class Hero(Karakter):
    def __init__(self, nama: str, hp: float, max_hp: float, attack: float, defend: float):
        super().__init__(nama, hp, max_hp, attack, defend)
        self.inventory = []
        self.boss_pity = 0
        self.weapon = None
        self.armor = None

        # Progression Attributes
        self.level = 1
        self.exp = 0
        self.next_level_exp = 100
        self.stat_points = 0

        # Basic Stats
        self.str_attr = 0
        self.dex_attr = 0
        self.con_attr = 0
        self.int_attr = 0
        self.wis_attr = 0
        self.cha_attr = 0

        # Mana / MP tracking
        self.mp = 10
        self.max_mp = 10

    def total_attack(self):
        bonus = self.weapon.efek if self.weapon else 0.0
        return round(self.attack + self.str_attr + bonus, 2)

    def total_armor(self):
        bonus = self.armor.efek if self.armor else 0.0
        return round(self.defend + (self.con_attr * 0.5) + bonus, 2)

    def get_dodge_chance(self):
        return round(self.dex_attr * 0.5, 2)

    def get_crit_chance(self):
        return round(self.cha_attr * 0.5, 2)

    def tampilkan_status(self):
        print("\n===========================")
        print(locale_manager.t("status_title"))
        print("===========================")
        print(locale_manager.t("status_name", nama=self.nama))
        print(locale_manager.t("status_level", level=self.level))
        print(locale_manager.t("status_exp", exp=self.exp, next_level_exp=self.next_level_exp))
        print(locale_manager.t("status_hp", hp=self.hp, max_hp=self.max_hp))
        print(locale_manager.t("status_mp", mp=self.mp, max_mp=self.max_mp))
        print(locale_manager.t("status_atk", attack=self.total_attack()))
        print(locale_manager.t("status_def", defend=self.total_armor()))
        print(locale_manager.t("status_dodge", dodge=self.get_dodge_chance()))
        print(locale_manager.t("status_crit", crit=self.get_crit_chance()))
        print(locale_manager.t("status_weapon", weapon=self.weapon.nama if self.weapon else "-"))
        print(locale_manager.t("status_armor", armor=self.armor.nama if self.armor else "-"))
        print("----------------------------")
        print(locale_manager.t("status_points", points=self.stat_points))

        # Basic RPG stats
        print(f"STR: {self.str_attr} | DEX: {self.dex_attr} | CON: {self.con_attr}")
        print(f"INT: {self.int_attr} | WIS: {self.wis_attr} | CHA: {self.cha_attr}")
        print("----------------------------")

    def alokasi_stat_points(self):
        while self.stat_points > 0:
            print("\n" + locale_manager.t("allocate_menu_title"))
            print(locale_manager.t("allocate_menu_points", points=self.stat_points))
            print(locale_manager.t("allocate_menu_str", val=self.str_attr))
            print(locale_manager.t("allocate_menu_dex", val=self.dex_attr))
            print(locale_manager.t("allocate_menu_con", val=self.con_attr))
            print(locale_manager.t("allocate_menu_int", val=self.int_attr))
            print(locale_manager.t("allocate_menu_wis", val=self.wis_attr))
            print(locale_manager.t("allocate_menu_cha", val=self.cha_attr))
            print(locale_manager.t("allocate_menu_done"))

            pilihan = input(locale_manager.t("allocate_menu_choice")).strip()
            if pilihan == "0" or pilihan.lower() in ["batal", "cancel", ""]:
                break
            
            if pilihan in ["1", "2", "3", "4", "5", "6"]:
                max_pts = self.stat_points
                qty_input = input(locale_manager.t("allocate_qty_prompt", max_pts=max_pts)).strip().lower()
                if qty_input == "0" or qty_input in ["batal", "cancel", ""]:
                    continue
                
                qty_to_add = 1
                if qty_input.isdigit():
                    qty_to_add = min(max_pts, max(1, int(qty_input)))

                if pilihan == "1":
                    self.str_attr += qty_to_add
                elif pilihan == "2":
                    self.dex_attr += qty_to_add
                elif pilihan == "3":
                    self.con_attr += qty_to_add
                    self.max_hp += qty_to_add * 10
                    self.hp += qty_to_add * 10
                elif pilihan == "4":
                    self.int_attr += qty_to_add
                    self.max_mp += qty_to_add * 5
                    self.mp += qty_to_add * 5
                elif pilihan == "5":
                    self.wis_attr += qty_to_add
                elif pilihan == "6":
                    self.cha_attr += qty_to_add

                self.stat_points -= qty_to_add
            else:
                print(locale_manager.t("invalid_selection"))

    def tampilkan_inventory(self):
        print("\n===========================")
        print(locale_manager.t("inventory_title"))
        print("===========================")
        print(locale_manager.t("inventory_weapon", weapon=self.weapon.nama if self.weapon else "-"))
        print(locale_manager.t("inventory_armor", armor=self.armor.nama if self.armor else "-"))

        if len(self.inventory) != 0:
            grouped_inventory = {}
            for item in self.inventory:
                if item.nama in grouped_inventory:
                    grouped_inventory[item.nama]["qty"] += 1
                else:
                    grouped_inventory[item.nama] = {"item_object": item, "qty": 1}
            no = 1
            for nama_item, data in grouped_inventory.items():
                item = data["item_object"]
                qty = data["qty"]
                print(locale_manager.t("inventory_item_line", no=no, nama=item.nama, qty=qty, tipe=item.tipe.upper(), efek=item.efek, jenis_efek=item.jenis_efek))
                no += 1
        else:
            print(locale_manager.t("inventory_empty"))
        print("----------------------------")

    def unequip_weapon(self):
        if self.weapon:
            weapon = self.weapon
            self.weapon = None
            self.inventory.append(weapon)
            print(locale_manager.t("unequip_success", nama=weapon.nama))
            return True
        return False

    def unequip_armor(self):
        if self.armor:
            armor = self.armor
            self.armor = None
            self.inventory.append(armor)
            print(locale_manager.t("unequip_success", nama=armor.nama))
            return True
        return False

    def equip_item(self, item):
        if isinstance(item, Weapon):
            if self.weapon is not None:
                self.inventory.append(self.weapon)
                print(locale_manager.t("unequip_success", nama=self.weapon.nama))
            self.weapon = item
            if item in self.inventory:
                self.inventory.remove(item)
            print(locale_manager.t("equip_weapon_success", nama=item.nama, efek=item.efek, jenis_efek=item.jenis_efek))
            return True
        elif isinstance(item, Armor):
            if self.armor is not None:
                self.inventory.append(self.armor)
                print(locale_manager.t("unequip_success", nama=self.armor.nama))
            self.armor = item
            if item in self.inventory:
                self.inventory.remove(item)
            print(locale_manager.t("equip_armor_success", nama=item.nama, efek=item.efek, jenis_efek=item.jenis_efek))
            return True
        else:
            print(locale_manager.t("equip_invalid", nama=item.nama))
            return False

    def use_consumable(self, item):
        if not isinstance(item, Potion):
            print(locale_manager.t("consumable_invalid", nama=item.nama))
            return False

        healed = item.use(self)
        base_hp = self.hp - healed
        healed_bonus = round(healed * (1 + self.wis_attr / 100.0), 2)
        self.hp = min(self.max_hp, base_hp + healed_bonus)
        final_healed = round(self.hp - base_hp, 2)

        print(locale_manager.t("use_potion_success", nama=item.nama, healed=final_healed))

        if item in self.inventory:
            self.inventory.remove(item)
        return True
