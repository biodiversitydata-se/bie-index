#!/usr/bin/env python3
import os
import sys

def process_taxon(src_dir):
    print('\nProcess taxon')

    destination_path = f'{src_dir}/Taxon.tsv'
    original_path = f'{destination_path}.original'

    if not os.path.isfile(original_path):
        os.rename(destination_path, original_path)

    infile = open(original_path, 'r')
    outfile = open(destination_path, 'w')

    row_count = 0

    for row in infile:

        record = row.replace('\n', '').split('\t')
        scientificName = record[5]
        scientificNameAuthorship = record[6]

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

    if not os.path.isfile(original_path):
        os.rename(destination_path, original_path)

    infile = open(original_path, 'r')
    outfile = open(destination_path, 'w')

    row_count = 0
    keep_count = 0

    for row in infile:

        record = row.split('\t')
        language = record[2]
        source = record[7]

        if row_count == 0 or language in ['sv', 'en']:
            keep_count = keep_count + 1
            outfile.write(row)

        row_count = row_count + 1

    outfile.close()
    infile.close()

    print(f'Done. Processed {row_count} rows. Kept {keep_count} rows.')

def main(argv):

    src_dir = argv[1] if len(argv) > 1 else '/data/bie-index/import/backbone'
    print(f'Using {src_dir} as source directory')

    process_taxon(src_dir)

    process_vernacular_name(src_dir)

    print('\nAll done')

if __name__ == '__main__':
    main(sys.argv)
