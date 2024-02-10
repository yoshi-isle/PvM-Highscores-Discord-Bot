import wom
from dataclasses import dataclass
from typing import List

@dataclass()
class HiscoreBossGroup:
    name: str
    url: str
    bosses: List[wom.Bosses]

gwd = HiscoreBossGroup(name="God Wars Dungeon",
    url="https://oldschool.runescape.wiki/images/General_Graardor.png?4dd90",
    bosses=[
    wom.Bosses.CommanderZilyana,
    wom.Bosses.GeneralGraardor,
    wom.Bosses.Kreearra,
    wom.Bosses.KrilTsutsaroth,
    wom.Bosses.Nex,
    ])

wilderness= HiscoreBossGroup(name="Wilderness",
    url="https://oldschool.runescape.wiki/images/Calvar%27ion_%28enraged%29.png?6268f",
    bosses=[
    wom.Bosses.Callisto,
    wom.Bosses.Vetion,
    wom.Bosses.Venenatis,
    wom.Bosses.Artio,
    wom.Bosses.Calvarion,
    wom.Bosses.Spindel,
    wom.Bosses.Scorpia,
    wom.Bosses.ChaosElemental,
    wom.Bosses.KingBlackDragon,
    wom.Bosses.CorporealBeast,
    wom.Bosses.ChaosFanatic,
    wom.Bosses.CrazyArchaeologist,
])

slayer =  HiscoreBossGroup(name="Slayer",
    url="https://oldschool.runescape.wiki/images/Cerberus.png?47f4c",
    bosses=[
    wom.Bosses.GrotesqueGuardians,
    wom.Bosses.AbyssalSire,
    wom.Bosses.Kraken,
    wom.Bosses.Cerberus,
    wom.Bosses.ThermonuclearSmokeDevil,
    wom.Bosses.AlchemicalHydra,
    wom.Bosses.Skotizo,
    wom.Bosses.DagannothSupreme,
    wom.Bosses.DagannothPrime,
    wom.Bosses.DagannothRex,
])

raids =  HiscoreBossGroup(name="Raids",
    url="https://oldschool.runescape.wiki/images/Verzik_Vitur_%28final_form%29.png?f9733",
    bosses=[
    wom.Bosses.ChambersOfXeric,
    wom.Bosses.ChambersOfXericChallenge,
    wom.Bosses.TheatreOfBlood,
    wom.Bosses.TheatreOfBloodHard,
    wom.Bosses.TombsOfAmascut,
    wom.Bosses.TombsOfAmascutExpert,
])

money_bosses =  HiscoreBossGroup(name="Money Bosses",
    url="https://oldschool.runescape.wiki/images/Zulrah_%28tanzanite%29.png?fd984",
    bosses=[
    wom.Bosses.Zulrah,
    wom.Bosses.Vorkath,
    wom.Bosses.PhantomMuspah,
    wom.Bosses.Nightmare,
    wom.Bosses.PhosanisNightmare,
])

tzhaar =  HiscoreBossGroup(name="Tzhaar",
    url="https://oldschool.runescape.wiki/images/TzHaar-Ket-Rak%27s_Challenges.png?53c80",
    bosses=[
    wom.Bosses.TzTokJad,
    wom.Bosses.TzKalZuk,
])

gauntlet =  HiscoreBossGroup(name="Gauntlet",
    url="https://oldschool.runescape.wiki/images/Crystalline_Hunllef.png?7737a",
    bosses=[
    wom.Bosses.TheGauntlet,
    wom.Bosses.TheCorruptedGauntlet,
])

dt2 =  HiscoreBossGroup(name="Desert Treasure 2",
    url="https://oldschool.runescape.wiki/images/The_Leviathan.png?d588a",
    bosses=[
    wom.Bosses.DukeSucellus,
    wom.Bosses.TheLeviathan,
    wom.Bosses.Vardorvis,
    wom.Bosses.TheWhisperer
])

other =  HiscoreBossGroup(name="Other",
    url="https://oldschool.runescape.wiki/images/The_Mimic.png?b45f4",
    bosses=[
    wom.Bosses.BarrowsChests,
    wom.Bosses.GiantMole,
    wom.Bosses.DerangedArchaeologist,
    wom.Bosses.Sarachnis,
    wom.Bosses.KalphiteQueen,
    wom.Bosses.Obor,
    wom.Bosses.Bryophyta,
    wom.Bosses.Mimic,
    wom.Bosses.Hespori,
    wom.Bosses.Zalcano,
])



all_boss_groups = [
    gwd,
    wilderness,
    slayer,
    raids,
    money_bosses,
    tzhaar,
    gauntlet,
    dt2,
    other,
]
