class Karakter:
    def __init__(
        self, nama: str, hp: float, max_hp: float, attack: float, defend: float
    ):
        self.nama = nama
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defend = defend

    def TotalAttack(self):
        damage_output = self.attack
        return round(damage_output, 2)

    def TotalArmor(self):
        damage_absord = self.defend
        return round(damage_absord, 2)

    def Serang(self, target):
        damage = self.TotalAttack() - target.TotalArmor()
        if damage <= 0:
            damage = 1
        target.hp = target.hp - damage
        return round(target.hp, 2)


class Hero(Karakter):
    def __init__(
        self,
        nama: str,
        hp: float,
        max_hp: float,
        attack: float,
        defend: float,
    ):
        super().__init__(nama, hp, max_hp, attack, defend)
        self.inventory = []
        self.boss_pity = 0
        self.weapon = None
        self.armor = None

    def TotalAttack(self):
        if self.weapon is not None:
            damage_output = self.attack + self.weapon.efek
            return round(damage_output, 2)
        else:
            damage_output = self.attack
        return round(damage_output, 2)

    def TotalArmor(self):
        if self.armor is not None:
            damage_absord = self.defend + self.armor.efek
            return round(damage_absord, 2)
        else:
            damage_absord = self.defend
        return round(damage_absord, 2)

    def TampilkanStatus(self):
        print("\n===========================")
        print("   STATUS KARAKTER ANDA   ")
        print("===========================")
        print(f"Nama Karakter: {self.nama}")
        print(f"HP : {self.hp:.2f} / {self.max_hp}")
        print(f"ATK : {self.attack}")
        print(f"DEF : {self.defend}")
        print("----------------------------")

    def TampilkanInventory(self):
        print("\n===========================")
        print("         INVENTORY        ")
        print("===========================")
        print(f"Weapon: {self.weapon.nama if self.weapon else '-'}")
        print(f"Armor: {self.armor.nama if self.armor else '-'}")

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

                print(
                    f"{no}. {item.nama} (x{qty} pcs) - Jenis: {item.tipe} (Efek: +{item.efek} {item.jenis_efek})"
                )
                no += 1
        else:
            print("\nInventory Anda Kosong\n")
        print("----------------------------")

    def EquipItem(self, item):
        tipe_item = item.tipe.lower()
        if tipe_item == "weapon":
            if self.weapon is not None:
                self.inventory.append(self.weapon)
                print(f"{self.weapon.naam} berhasil dilepas")

            self.weapon = item
            if item in self.inventory:
                self.inventory.remove(item)
            print(
                f"⚔️ Berhasil memakai Senjata: {item.nama} (+{item.efek} {item.jenis_efek})!"
            )
            return True
        elif tipe_item == "armor":
            if self.armor is not None:
                self.inventory.append(self.armor)
                print(f"{self.armor.nama} berhasil dilepas")

            self.armor = item
            if item in self.inventory:
                self.inventory.remove(item)
            print(
                f"🛡️ Berhasil memakai Armor: {item.nama} (+{item.efek} {item.jenis_efek})!"
            )
            return True

        else:
            print(f"❌ {item.nama} bukan equipment yang bisa dipasang!")
            return False

    def UseConsumable(self, item):
        if item.tipe.lower() != "potion":
            print(f"❌ {item.nama} bukan item consumable atau potion!")
            return False

        if item.jenis_efek == "heal":
            # Jumlah Heal persen karena potionnya heal Persen
            jumlah_heal = self.max_hp * item.efek if item.efek < 1.0 else item.efek
            hp_lama = self.hp
            self.hp = min(self.max_hp, self.hp + jumlah_heal)
            healed = round(self.hp - hp_lama, 2)
            print(f"🧪 Memakai {item.nama}, memulihkan {healed} HP!")

        # HAPUS DARI INVENTORY KARNEA SUDAH DIPAKAI
        if item in self.inventory:
            self.inventory.remove(item)

        return True
