import re

training_data = []
test_data = []

#optional
#validation_data = []

with open('training_data_1_supported_fact.txt', 'r') as full_file:
    for num, line in enumerate(full_file, 1):

        if '1 ' in line:
            print 'found at line:', num
        training_data.append(line)


occurences = [m.start() for m in re.finditer('1 ', data)]

