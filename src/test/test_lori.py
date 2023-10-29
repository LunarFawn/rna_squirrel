import pytest

from pathlib import Path

from test.bin.show_lori.loris_api import Lori

def test_lori():
    new_lori:Lori = Lori(var_name='new_lori',
                     working_folder='/home/rnauser/repo/rna_squirrel/src/test/bin/show_lori/data')
    new_lori.sexy.boobs_names = "boobs"
    new_lori.favorites.favorite_show.show_name = "TNG"

    print(f'{new_lori.sexy.boobs_names} are the returned name of loris boobs')
    print(f'{new_lori.favorites.favorite_show.show_name} is loris favorite show')