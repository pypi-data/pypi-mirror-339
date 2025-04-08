from gypsum_dl import GypsumDL

for smiles in [
    'Oc1ccccc1',
    'CCC=O',
    'ClC(C[C@@](Cl)(C)F)(F)C(C(C)C)=O',
    'FC(C(I)=C(CC(I)(Cl)C)CC)=C(Cl)C',
    'CC(CC)=C(C/C(I)=C(C)/F)Cl',
    'CC([C@@H]1CC[C@H](C(C)(C)C)CC1)(C)C',
    ]:

    print(f"example {smiles}")
    
    st = GypsumDL(smiles, 
                  min_ph=6.4, 
                  max_ph=8.4, 
                  pka_precision=1.0,
                  thoroughness=3,
                  max_variants_per_compound=5,
                  second_embed=False,
                  skip_optimize_geometry=False,
                  skip_alternate_ring_conformations=False,
                  skip_adding_hydrogen=False,
                  skip_making_tautomers=False,
                  skip_enumerate_chiral_mol=False,
                  skip_enumerate_double_bonds=False,
                  let_tautomers_change_chirality=False,
                  use_durrant_lab_filters=True,
                  job_manager='serial',
                  num_processors=1,
                 )
    
    for i, smiles in enumerate(st, start=1):
        print(f"  [{i}] {smiles}")
    print()
