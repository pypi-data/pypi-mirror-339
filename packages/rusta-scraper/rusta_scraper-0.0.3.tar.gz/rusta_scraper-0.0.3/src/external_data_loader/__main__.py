import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import opti_api as opti
import pim_api as pim  

pim.load_pim_data()
opti.load_opti_missing_prices()
opti.load_prices()