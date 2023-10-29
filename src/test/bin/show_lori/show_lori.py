from pathlib import Path

from rna_squirrel.make_single_api_file import GenerateSingleApifile
new_generator:GenerateSingleApifile = GenerateSingleApifile()
new_generator.run(nut_struct_name="LoriStructure",
                      yaml_config_path=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/show_lori/lori_config.yaml'),
                      dst_save_filename=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/show_lori/loris_api.py'))