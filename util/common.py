import typing
from typing import Dict, Literal, Tuple
import numpy as np
from .sampler import StatSampler


def to_stat(stat_inp: dict):
    stats = np.zeros(len(statnames))
    for k, v in stat_inp.items():
        stats[statmap[k]] += v
    return stats


SetKey = Literal["Adventurer", "ArchaicPetra", "Berserker", "BlizzardStrayer",
                 "BloodstainedChivalry", "BraveHeart", "CrimsonWitchOfFlames",
                 "DefendersWill", "EmblemOfSeveredFate", "Gambler",
                 "GladiatorsFinale", "HeartOfDepth", "HuskOfOpulentDreams",
                 "Instructor", "Lavawalker", "LuckyDog", "MaidenBeloved",
                 "MartialArtist", "NoblesseOblige", "OceanHuedClam",
                 "PaleFlame", "PrayersForDestiny", "PrayersForIllumination",
                 "PrayersForWisdom", "PrayersToSpringtime", "ResolutionOfSojourner",
                 "RetracingBolide", "Scholar", "ShimenawasReminiscence",
                 "TenacityOfTheMillelith", "TheExile", "ThunderingFury",
                 "Thundersoother", "TinyMiracle", "TravelingDoctor",
                 "ViridescentVenerer", "WanderersTroupe"]

StatKey = Literal["hp", "hp_", "atk", "atk_", "def", "def_", "eleMas", "enerRech_",
                  "heal_", "critRate_", "critDMG_", "physical_dmg_", "anemo_dmg_",
                  "geo_dmg_", "electro_dmg_", "hydro_dmg_", "pyro_dmg_", "cryo_dmg_",
                  'base_hp', 'base_atk', 'base_def']
statnames: Tuple[str] = typing.get_args(StatKey)
statmap: Dict[StatKey, int] = {n: i for i, n in enumerate(statnames)}

SlotKey = Literal["flower", "plume", "sands", "goblet", "circlet"]
slotnames = typing.get_args(SlotKey)
slotmap = {n: i for i, n in enumerate(slotnames)}

mainstat = (
    StatSampler({'hp': 1}),
    StatSampler({'atk': 1}),
    StatSampler({'hp_': 80, 'atk_': 80, 'def_': 80,
                 'eleMas': 30, 'enerRech_': 30}),
    StatSampler({'hp_': 85, 'atk_': 85, 'def_': 80, 'eleMas': 10, 'physical_dmg_': 20,
                 'hydro_dmg_': 20, 'pyro_dmg_': 20, 'cryo_dmg_': 20, 'electro_dmg_': 20,
                 'anemo_dmg_': 20, 'geo_dmg_': 20}),
    StatSampler({'hp_': 22, 'atk_': 22, 'def_': 22,
                 'eleMas': 4, 'critRate_': 10, 'critDMG_': 10, 'heal_': 10}),
)
substat = StatSampler({
    'hp': 6, 'def': 6, 'atk': 6,
    'hp_': 4, 'def_': 4, 'atk_': 4, 'enerRech_': 4, 'eleMas': 4,
    'critRate_': 3, 'critDMG_': 3
})
main_vals: Dict[StatKey, float] = {
    'hp': 4780, 'atk': 311, 'def': -1,
    'hp_': .466, 'atk_': .466, 'def_': .583,
    'eleMas': 187, 'enerRech_': 518,
    'critRate_': .311, 'critDMG_': .622,
    'heal_': .359, 'physical_dmg_': .583, 'hydro_dmg_': .466, 'pyro_dmg_': .466,
    'cryo_dmg_': .466, 'electro_dmg_': .466, 'anemo_dmg_': .466, 'geo_dmg_': .466
}
sub_vals: Dict[StatKey, float] = {
    'hp': 298.75, 'atk': 19.45, 'def': 23.15, 'hp_': .0583, 'atk_': .0583, 'def_': .0729,
    'eleMas': 23.31, 'enerRech_': .0648, 'critRate_': .0389, 'critDMG_': .0777
}
