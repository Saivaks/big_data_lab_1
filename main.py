import os 
import subprocess
import pred_procces
import process_data
import train_model
import test_model

import test_cat
import test_len
import test_type

if __name__ == '__main__':
	pred_procces.create_env()
	process_data.procces()
	train_model.train()
	test_model.test()
	
	test_cat.test1()
	test_len.test2()
	test_type.test3()