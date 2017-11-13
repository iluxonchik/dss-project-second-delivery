#!/usr/bin/env python
import csv
import sys
import random

def write_ordereddict_list_to_file(odict_lst, file_name):
    keys, values = [], []

    keys = odict_lst[0].keys()

    with open(file_name, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(keys)
        for odict in odict_lst:
            writer.writerow(odict.values())

if len(sys.argv) < 4:
    prog_name = sys.argv[0]
    print('Usage: {}: <noshows_path> <total_set_size> <tranining_set_percentage>'.format(prog_name))
    print('\tThe tool dynamically computes the No-Shows percentage.')
    print('\tNOTE: the tool selects a RANDOM sample from each one of the subsets, so different runs will produce different outputs.')
    print('Example: {}: ~/home/iluoxchik/Documents/noshows.csv 1000 70'.format(prog_name))
    sys.exit(1)

csv_path = sys.argv[1]
total_set_size = int(sys.argv[2])
tranining_set_percentage = int(sys.argv[3])
testing_set_percentage = 100 - tranining_set_percentage

trainig_set_size = int((total_set_size * tranining_set_percentage) / 100)
testing_set_size = int((total_set_size * testing_set_percentage) / 100)

print('Parsed options:')
print('\tTotal Set Size: {}'.format(total_set_size))
print('\tTraining Set Percentage: {}'.format(tranining_set_percentage))
print('\tTesting Set Percentage: {}'.format(testing_set_percentage))
print('\tTraining Set Size: {}'.format(trainig_set_size))
print('\tTesting Set Size: {}'.format(testing_set_size))

with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)

    num_rows = 0
    num_no_shows = 0
    no_show_no_row = []
    no_show_yes_row = []

    for row in reader:
        num_rows += 1
        if row['No-show'] == 'Yes':
            num_no_shows += 1
            no_show_yes_row += [row]
        else:
            no_show_no_row += [row]

    no_shows_yes_percentage = (num_no_shows * 100)/num_rows
    no_shows_no_percentage = ((num_rows - num_no_shows) * 100)/num_rows
    random.shuffle(no_show_no_row)
    random.shuffle(no_show_yes_row)

    print('No-Shows Statistical Results:')
    print('\tRows: {} | No-Shows: {}'.format(num_rows, num_no_shows))
    print('\tNo-Shows Yes percentage: {}%'.format(no_shows_yes_percentage))
    print('\tNo-Shows No percentage: {}%'.format(no_shows_no_percentage))

    # Let's generate the traning set
    trainig_set_file_name = '{}_{}_{}_training.csv'.format(total_set_size, tranining_set_percentage, testing_set_percentage)
    num_no_shows_yes = int((trainig_set_size * no_shows_yes_percentage) / 100)
    num_no_shows_no = trainig_set_size - num_no_shows_yes  # to make sure that we get exactly the set size in total
    print('Training Set Size = {} | No-Shows Yes: {} | No-Shows No: {}'.format(trainig_set_size, num_no_shows_yes, num_no_shows_no))

    training_no_show_yes_rows = no_show_yes_row[:num_no_shows_yes]
    no_show_yes_row = no_show_yes_row[num_no_shows_yes:]

    training_no_show_no_rows = no_show_no_row[:num_no_shows_no]
    no_show_no_row = no_show_no_row[num_no_shows_no:]

    final_training_set_rows = training_no_show_yes_rows + training_no_show_no_rows

    write_ordereddict_list_to_file(final_training_set_rows, trainig_set_file_name)

    # Let's generate the testing set
    testing_set_file_name = '{}_{}_{}_testing.csv'.format(total_set_size, tranining_set_percentage, testing_set_percentage)
    num_no_shows_yes = int((testing_set_size * no_shows_yes_percentage) / 100)
    num_no_shows_no = testing_set_size - num_no_shows_yes  # to make sure that we get exactly the set size in total
    print('Testing Set Size = {} | No-Shows Yes: {} | No-Shows No: {}'.format(testing_set_size, num_no_shows_yes, num_no_shows_no))

    testing_no_show_yes_rows = no_show_yes_row[:num_no_shows_yes]
    testing_no_show_no_rows = no_show_no_row[:num_no_shows_no]
    final_testing_set_rows = testing_no_show_yes_rows + testing_no_show_no_rows

    write_ordereddict_list_to_file(final_testing_set_rows, testing_set_file_name)
