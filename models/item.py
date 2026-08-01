class Item:
    def __init__(self, nama: str, tipe: str, efek: float, jenis_efek: str, rarity: str):
        self.nama = nama
        self.tipe = tipe
        self.efek = efek
        self.jenis_efek = jenis_efek
        self.rarity = rarity

    @staticmethod
    def create(nama: str, tipe: str, efek: float, jenis_efek: str, rarity: str):
        tipe_lower = tipe.lower()
        if tipe_lower == "weapon":
            return Weapon(nama, efek, jenis_efek, rarity)
        elif tipe_lower == "armor":
            return Armor(nama, efek, jenis_efek, rarity)
        elif tipe_lower in ["potion", "consumable"]:
            return Potion(nama, efek, jenis_efek, rarity)
        return Item(nama, tipe, efek, jenis_efek, rarity)

    def to_dict(self):
        return {
            "nama": self.nama,
            "tipe": self.tipe,
            "efek": self.efek,
            "jenis_efek": self.jenis_efek,
            "rarity": self.rarity
        }


class Equipment(Item):
    def __init__(self, nama: str, tipe: str, efek: float, jenis_efek: str, rarity: str):
        super().__init__(nama, tipe, efek, jenis_efek, rarity)


class Weapon(Equipment):
    def __init__(self, nama: str, efek: float, jenis_efek: str, rarity: str):
        super().__init__(nama, "weapon", efek, jenis_efek, rarity)


class Armor(Equipment):
    def __init__(self, nama: str, efek: float, jenis_efek: str, rarity: str):
        super().__init__(nama, "armor", efek, jenis_efek, rarity)


class Consumable(Item):
    def __init__(self, nama: str, tipe: str, efek: float, jenis_efek: str, rarity: str):
        super().__init__(nama, tipe, efek, jenis_efek, rarity)

    def use(self, character):
        raise NotImplementedError


class Potion(Consumable):
    def __init__(self, nama: str, efek: float, jenis_efek: str, rarity: str):
        super().__init__(nama, "potion", efek, jenis_efek, rarity)

    def use(self, character):
        if self.jenis_efek == "heal":
            # Potion effects can be absolute or relative (e.g. heal percentage)
            heal_amount = character.max_hp * self.efek if self.efek < 1.0 else self.efek
            old_hp = character.hp
            character.hp = min(character.max_hp, character.hp + heal_amount)
            return round(character.hp - old_hp, 2)
        return 0.0


Rarity_drop_chance = {
    "Common": 55,
    "Uncommon": 20,
    "Rare": 15,
    "Legendary": 8,
    "Immortal": 2,
}
