from typing import List
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import time
import pytest
import os

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
fName = "test_data_5A//CellDataFileTestMJ1.txt"

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
		with open(f"test_data2//{test_file}") as f_in:

			if np.size(self.voltage_array) == 0 and np.size(self.current_array) == 0:
				self.voltage_array, self.current_array = np.loadtxt(itertools.islice(f_in, 3, None), delimiter='\t', usecols=(1,3), unpack=True)
			else:
				temp_voltage, temp_current = np.loadtxt(itertools.islice(f_in, 3, None), delimiter='\t', usecols=(1,3), unpack=True)

				self.voltage_array = np.concatenate((self.voltage_array, temp_voltage))

				self.current_array = np.concatenate((self.current_array, temp_current))

		self.v_ocv = self.voltage_array + (0.085 * self.current_array)

		print(f"Size of test: {len(self.v_ocv)}\n")

		for i in range(len(self.v_ocv)):
			soc = self.SoCOCV.correct_soc(self.v_ocv[i], self.current_array[i])
			if i % 1000 == 0:
				print(f'The actual Open Curuit Voltage is: {self.v_ocv[i]}')
				print(f'The State of Charge Percentage is: {soc}')
				if not isinstance(soc, str):
					print(f'The calculated Open Circuit Voltage for the State of Charge is: {self.SoCOCV.get_cell_ocv(soc)}')
				print('')



if __name__ == '__main__':
	testing = test_SoC_OCV()
	# testing.test()

	n_time = 0

	initial_time = time.time()

	for file_name in os.listdir(f'{os.getcwd()}/test_data2'):
		print(f'testing file: {file_name} -------------------------------------------------------------------------')
		testing.test_multiple_correct_soc(file_name)
		final_time = time.time()
		n_time += 1
		print(f"time taken for {n_time} test: {final_time - initial_time}\n")
		initial_time = final_time
