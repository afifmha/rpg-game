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
        damage = self.total_attack() - target.total_armor()
        if damage <= 0:
            damage = 1
        target.hp = target.hp - damage
        return round(target.hp, 2)


class Hero(Karakter):
    def __init__(self, nama: str, hp: float, max_hp: float, attack: float, defend: float):
        super().__init__(nama, hp, max_hp, attack, defend)
        self.inventory = []
        self.boss_pity = 0
        self.weapon = None
        self.armor = None

    def total_attack(self):
        bonus = self.weapon.efek if self.weapon else 0.0
        return round(self.attack + bonus, 2)

    def total_armor(self):
        bonus = self.armor.efek if self.armor else 0.0
        return round(self.defend + bonus, 2)

    def tampilkan_status(self):
        print("\n===========================")
        print(locale_manager.t("status_title"))
        print("===========================")
        print(locale_manager.t("status_name", nama=self.nama))
        print(locale_manager.t("status_hp", hp=self.hp, max_hp=self.max_hp))
        print(locale_manager.t("status_atk", attack=self.total_attack()))
        print(locale_manager.t("status_def", defend=self.total_armor()))
        print(locale_manager.t("status_weapon", weapon=self.weapon.nama if self.weapon else "-"))
        print(locale_manager.t("status_armor", armor=self.armor.nama if self.armor else "-"))
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
        print(locale_manager.t("use_potion_success", nama=item.nama, healed=healed))

        if item in self.inventory:
            self.inventory.remove(item)
        return True
