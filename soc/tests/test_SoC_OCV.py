import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import time
import pytest

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__)))
fName = "test_data//CellDataFileTestMJ1.txt"

from SoC_OCV import SoC_OCV

class test_SoC_OCV:
	def __init__(self):
		self.SoCOCV = SoC_OCV()
		self.voltage_array = np.array([])
		self.current_array = np.array([])
		self.v_ocv = np.array([])
	
	def test(self):
		ocv1 = self.SoCOCV.get_cell_ocv(100)
		ocv2 = self.SoCOCV.get_cell_ocv(75)
		ocv3 = self.SoCOCV.get_cell_ocv(25)
		ocv4 = self.SoCOCV.get_cell_ocv(0)
		print("Get OCV test:")
		print(f"soc = 100, ocv = {ocv1}")
		print(f"soc = 75, ocv = {ocv2}")
		print(f"soc = 25, ocv = {ocv3}")
		print(f"soc = 0, ocv = {ocv4}")
		print('')
		print("Correct SOC test:")
		print(f"ocv = {ocv1}, soc = {self.SoCOCV.correct_soc(ocv1, 1)}")
		print(f"ocv = {ocv2}, soc = {self.SoCOCV.correct_soc(ocv2, 1)}")
		print(f"ocv = {ocv3}, soc = {self.SoCOCV.correct_soc(ocv3, 1)}")
		print(f"ocv = {ocv4}, soc = {self.SoCOCV.correct_soc(ocv4, 1)}")

	def test_plot_graph(self):
		self.SoCOCV.plot_graph()
	
	def test_multiple_correct_soc(self, test_file: str):
		with open(test_file) as f_in:
			if np.size(self.voltage_array) == 0 and np.size(self.current_array) == 0:
				self.voltage_array, self.current_array = np.loadtxt(itertools.islice(f_in, 3, None), delimiter='\t', usecols=(1,3), unpack=True)
			else:
				temp_voltage, temp_current = np.loadtxt(itertools.islice(f_in, 3, None), delimiter='\t', usecols=(1,3), unpack=True)
				self.voltage_array = np.concatenate((self.voltage_array, temp_voltage))
				self.current_array = np.concatenate((self.current_array, temp_current))
		
		self.v_ocv = self.voltage_array + (0.085 * self.current_array)
		print(f"Size of test: {len(self.v_ocv)}")

		for i in range(len(self.v_ocv)):
			soc = self.SoCOCV.correct_soc(self.v_ocv[i], self.current_array[i])


if __name__ == '__main__':
	testing = test_SoC_OCV()
	# testing.test()

	test_file1 = "test_data//LGMJ1_1_1P_Discharge.txt"
	test_file2 = "test_data//LGMJ1_2_1P_Discharge.txt"
	test_file3 = "test_data//LGMJ1_3_1P_Discharge.txt"
	test_file4 = "test_data//LGMJ1_4_1P_Discharge.txt"
	test_file5 = "test_data//LGMJ1_5_1P_Discharge.txt"

	start_time = time.time()
	testing.test_multiple_correct_soc(test_file1)
	first_test_time = time.time()
	print(f"time taken for first test: {first_test_time - start_time}\n")
	testing.test_multiple_correct_soc(test_file2)
	second_test_time = time.time()
	print(f"time taken for second test: {second_test_time - first_test_time}\n")
	testing.test_multiple_correct_soc(test_file3)
	third_test_time = time.time()
	print(f"time taken for third test: {third_test_time - second_test_time}\n")
	testing.test_multiple_correct_soc(test_file4)
	fourth_test_time = time.time()
	print(f"time taken for fourth test: {fourth_test_time - third_test_time}\n")
	testing.test_multiple_correct_soc(test_file5)
	fifth_test_time = time.time()
	print(f"time taken for final test: {fifth_test_time - fourth_test_time}\n")

	testing.test_multiple_correct_soc(test_file1)
	testing.test_multiple_correct_soc(test_file2)
	testing.test_multiple_correct_soc(test_file3)
	testing.test_multiple_correct_soc(test_file4)
	testing.test_multiple_correct_soc(test_file5)
	sixth_test_time = time.time()
	print(f"time taken for final test: {sixth_test_time - fifth_test_time}\n")

	testing.test_multiple_correct_soc(test_file1)
	testing.test_multiple_correct_soc(test_file2)
	testing.test_multiple_correct_soc(test_file3)
	testing.test_multiple_correct_soc(test_file4)
	testing.test_multiple_correct_soc(test_file5)
	testing.test_multiple_correct_soc(test_file1)
	testing.test_multiple_correct_soc(test_file2)
	testing.test_multiple_correct_soc(test_file3)
	testing.test_multiple_correct_soc(test_file4)
	testing.test_multiple_correct_soc(test_file5)
	testing.test_multiple_correct_soc(test_file1)
	testing.test_multiple_correct_soc(test_file2)
	testing.test_multiple_correct_soc(test_file3)
	testing.test_multiple_correct_soc(test_file4)
	testing.test_multiple_correct_soc(test_file5)
	testing.test_multiple_correct_soc(test_file1)
	testing.test_multiple_correct_soc(test_file2)
	testing.test_multiple_correct_soc(test_file3)
	testing.test_multiple_correct_soc(test_file4)
	testing.test_multiple_correct_soc(test_file5)
	seventh_test_time = time.time()
	print(f"time taken for final test: {seventh_test_time - sixth_test_time}\n")