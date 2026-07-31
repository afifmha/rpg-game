class Item:
    def __init__(self, nama: str, tipe: str, efek: float, jenis_efek: str, rarity: str):
        self.nama = nama
        self.tipe = tipe
        self.efek = efek
        self.jenis_efek = jenis_efek
        self.rarity = rarity


Rarity_drop_chance = {
    "Common": 55,
    "Uncommon": 20,
    "Rare": 15,
    "Legendary": 8,
    "Immortal": 2,
}
