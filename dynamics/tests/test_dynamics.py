import sys
import os.path
my_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(sys.path[0]))
from CdACrrCalculator import *
import filecmp
path_to_csv = os.path.join(my_path, 'rolldowndata/test.csv') 

# Test that the generator works as expected
def test_generate_test_datas():
    data = clean(path_to_csv)
    x = data['time']
    y = data['average_velocity']
    CdAmin = 0
    CdAmax = 1
    Crrmin = 0.001
    Crrmax = 0.1
    precision = 300
    list_data = generate_test_datas()
    open('test_data_file.txt', 'w').close()
    with open('test_data_file.txt', 'w') as f:
        for listitem in list_data:
           f.write('%s\n' % listitem)
    
    assert(filecmp.cmp('test_data_file.txt', sys.path[0] + '/baseline.txt')) 
    os.remove('test_data_file.txt')

# Test our diff function
def test_diff():
    l1 = [2, 3, 4]
    l2 = [4, 3, 2]
    assert(diff(l1,l2)) == 8

# Test that clean gives us our expected columns
def test_clean():
    data = clean(path_to_csv)
    # check the columns exist
    len_time = len(data['time'])
    len_velo = len(data['average_velocity'])
    assert(len_velo > 0 and len_time > 0) 
