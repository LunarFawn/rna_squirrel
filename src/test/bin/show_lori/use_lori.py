
from pathlib import Path
import sys
sys.path.append("/home/rnauser/repo/rna_squirrel/src/test/bin/show_lori/")
from loris_api import Lori

new_lori:Lori = Lori(var_name='new_lori',
                    working_folder='/home/rnauser/repo/rna_squirrel/src/test/bin/show_lori/data')
new_lori.sexy.boobs_names = "boobs"
new_lori.favorites.favorite_show.show_name = "TNG"
new_lori.favorites.education.date = "always"

print(f'{new_lori.sexy.boobs_names} are the returned name of loris boobs')
print(f'{new_lori.favorites.favorite_show.show_name} is loris favorite show')
print(f'{new_lori.favorites.education.date} is when to learn')


