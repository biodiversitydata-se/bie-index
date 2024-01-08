#!/usr/bin/env python3
#
# This script pre-processes the GBIF Backbone taxonomy before loading it into the bie-index.
#
# The original files are renamed (eg. Taxon.tsv -> Taxon.tsv.original) and the processed file
# is saved with the original name (eg. Taxon.tsv).
#
# The following procsessing is done:
#
# Taxon
# -----
# - Remove scientificNameAuthorship from scientificName (if included) because the bie-index
#   expects the scientificName to be without authorship.
#   Eg: Capreolus capreolus (Linnaeus, 1758) -> Capreolus capreolus
#
# VernacularName
# --------------
# - Only include Swedish and English names
# - Exclude names from some sources of bad quality
#

import os
import sys

ALLOWED_LANGUAGES = [
    'sv',
    'en',
]
DISALLOWED_SOURCES = [
    'Belgian Species List', # Contains comma-seprated lists of names
    # All of these have names in various languages wrongly tagged as English
    'Abrocomidae',
    'Acrobatidae',
    'Ailuridae',
    'Alpheidae',
    'Annelida',
    'Anomaluridae',
    'Antilocapridae',
    'Aotidae',
    'Aplodontiidae',
    'Atelidae',
    'Balaenidae',
    'Balaenopteridae',
    'Bathyergidae',
    'Bovidae',
    'Bradypodidae',
    'Burramyidae',
    'Caenolestidae',
    'Calomyscidae',
    'Camelidae',
    'Canidae',
    'Castoridae',
    'Caviidae',
    'Cebidae',
    'Cercopithecidae',
    'Cervidae',
    'Cheirogaleidae',
    'Chinchillidae',
    'Chlamyphoridae',
    'Chrysochloridae',
    'Cnidaria',
    'Cricetidae',
    'Ctenodactylidae',
    'Ctenomyidae',
    'Cuniculidae',
    'Cyclopedidae',
    'Cynocephalidae',
    'Dasypodidae',
    'Dasyproctidae',
    'Dasyuridae',
    'Daubentoniidae',
    'Delphinidae',
    'Diatomyidae',
    'Didelphidae',
    'Dinomyidae',
    'Dipodidae',
    'Dugongidae',
    'Echimyidae',
    'Echinoderms',
    'Elephantidae',
    'Equidae',
    'Erethizontidae',
    'Erinaceidae',
    'Eschrichtiidae',
    'Eupleridae',
    'Felidae',
    'Galagidae',
    'Geomyidae',
    'Giraffidae',
    'Gliridae',
    'Herpestidae',
    'Heterocephalidae',
    'Heteromyidae',
    'Hippopotamidae',
    'Hipposideridae',
    'Hominidae',
    'Hyaenidae',
    'Hylobatidae',
    'Hypsiprymnodontidae',
    'Hystricidae',
    'Indriidae',
    'Iniidae',
    'Lemuridae',
    'Lepilemuridae',
    'Leporidae',
    'Lipotidae',
    'Lorisidae',
    'Macropodidae',
    'Macroscelididae',
    'Manidae',
    'Megalonychidae',
    'Mephitidae',
    'Molossidae',
    'Monodontidae',
    'Mormoopidae',
    'Moschidae',
    'Muridae',
    'Mustelidae',
    'Myriatrix',
    'Myrmecobiidae',
    'Myrmecophagidae',
    'Mystacinidae',
    'Myzopodidae',
    'Nandiniidae',
    'Natalidae',
    'Nayades',
    'Neobalaenidae',
    'Nesomyidae',
    'Noctilionidae',
    'Notoryctidae',
    'Nycteridae',
    'Ochotonidae',
    'Octodontidae',
    'Odobenidae',
    'Orycetropodidae',
    'Otariidae',
    'Pedetidae',
    'Peracarida',
    'Peramelidae',
    'Petromuridae',
    'Phalangeridae',
    'Phitheciidae',
    'Phocidae',
    'Phocoenidae',
    'Phyllostomidae',
    'Physeteridae',
    'Platacanthomyidae',
    'Platanistidae',
    'Pontoporiidae',
    'Porifera',
    'Potamogalidae',
    'Potoroidae',
    'Procaviidae',
    'Procyonidae',
    'Pseudocheiridae',
    'Pteropodidae',
    'Ptilocercidae',
    'Rhinocerotidae',
    'Rhinolophidae',
    'Rhinonycteridae',
    'Rhinopomatidae',
    'Sciuridae',
    'Sminthidae',
    'Solenodontidae',
    'Soricidae',
    'Spalacidae',
    'Suidae',
    'Talpidae',
    'Tapiridae',
    'Tarsiidae',
    'Tarsipedidae',
    'Tayassuidae',
    'Tenrecidae',
    'Thryonomyidae',
    'Thylacomyidae',
    'Thyropteridae',
    'Tragulidae',
    'Trichechidae',
    'Tupaiidae',
    'Ursidae',
    'Vespertilionidae',
    'Viverridae',
    'Vombatidae',
    'Zapodidae',
    'Ziphiidae',
]

def process_taxon(src_dir):
    print('\nProcess taxon')

    destination_path = f'{src_dir}/Taxon.tsv'
    original_path = f'{destination_path}.original'

    # Rename original file (if not already done)
    if not os.path.isfile(original_path):
        os.rename(destination_path, original_path)

    infile = open(original_path, 'r')
    outfile = open(destination_path, 'w')

    row_count = 0

    for row in infile:

        record = row.replace('\n', '').split('\t')
        scientificName = record[5]
        scientificNameAuthorship = record[6]

        # Remove scientificNameAuthorship from scientificName
        if scientificNameAuthorship and scientificName.endswith(scientificNameAuthorship):
            record[5] = scientificName[:-len(scientificNameAuthorship)].strip()

        outfile.write('\t'.join(record) + '\n')

        row_count = row_count + 1

        if row_count % 1000000 == 0:
            print(f'Processed {row_count} rows')

    outfile.close()
    infile.close()

    print(f'Done. Processed {row_count} rows')

def process_vernacular_name(src_dir):
    print('\nProcess vernacular name')

    destination_path = f'{src_dir}/VernacularName.tsv'
    original_path = f'{destination_path}.original'

    # Rename original file (if not already done)
    if not os.path.isfile(original_path):
        os.rename(destination_path, original_path)

    infile = open(original_path, 'r')
    outfile = open(destination_path, 'w')

    row_count = 0
    keep_count = 0

    for row in infile:

        record = row.replace('\n', '').split('\t')
        language = record[2]
        source = record[7]

        if (row_count == 0 or # Header row
                (language in ALLOWED_LANGUAGES and
                 source not in DISALLOWED_SOURCES)):
            keep_count = keep_count + 1
            outfile.write(row)

        row_count = row_count + 1

    outfile.close()
    infile.close()

    print(f'Done. Processed {row_count} rows. Kept {keep_count} rows')

def main(argv):

    src_dir = argv[1] if len(argv) > 1 else '/data/bie-index/import/backbone'
    print(f'Using {src_dir} as source directory')

    process_taxon(src_dir)

    process_vernacular_name(src_dir)

    print('\nAll done')

if __name__ == '__main__':
    main(sys.argv)