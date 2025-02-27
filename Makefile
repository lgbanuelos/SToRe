running_example_dir = data/BPI_challenge_2012
#===========================================R=============================== fiting
run_CLR:
	#for number in `seq 6` ; do \
		#python3 replay_CLR.py ${running_example_dir}/trace_$$number.dat ; \
	#done
	python3 replay_CLR.py ${running_example_dir}/my_running_example.dat

run_CLR_plus:
	#for number in `seq 6` ; do \
		#python3 replay_CLR_plus.py ${running_example_dir}/trace_$$number.dat ; \
	#done
	python3 replay_CLR_plus.py ${running_example_dir}/my_running_example.dat

run_SEC:
	#for number in `seq 6`; do \
		#python3 replay_SEC.py ${running_example_dir}/trace_$$number.dat ; \
	#done
	python3 replay_SEC.py ${running_example_dir}/my_running_example.dat

run_SEC_plus:
	#for number in `seq 6`; do \
		#python3 replay_SEC_plus.py ${running_example_dir}/trace_$$number.dat ; \
	#done
	python3 replay_SEC_plus.py ${running_example_dir}/my_running_example.dat

run_SEC_plus_STEP:
	#for number in `seq 6`; do \
		#python3 replay_SEC_plus_STEP.py ${running_example_dir}/trace_$$number.dat ; \
	#done
	python3 replay_SEC_plus_STEP.py ${running_example_dir}/my_running_example.dat

#=========================================================================== broken
run_CLR_all:
	 for number in `seq 10` ; do \
		 python3 replay_CLR.py ${running_example_dir}/output/$$number.txt; \
	 done


#=========================================================================== broken
# run_CLR_broken:
# 	for number in `seq 6` ; do \
# 		python3 replay_CLR.py ${running_example_broken_dir}/trace_$$number.dat ; \
# 	done
# 
# run_CLR_plus_broken:
# 	for number in `seq 6` ; do \
# 		python3 replay_CLR_plus.py ${running_example_broken_dir}/trace_$$number.dat ; \
# 	done
# 
# run_SEC_broken:
# 	for number in `seq 6` ; do \
# 		python3 replay_SEC.py ${running_example_broken_dir}/trace_$$number.dat ; \
# 	done
# 
# run_SEC_plus_broken:
# 	for number in `seq 6`; do \
# 		python3 replay_SEC_plus.py ${running_example_broken_dir}/trace_$$number.dat ; \
# 	done
# 
# run_SEC_plus_STEP_broken:
# 	for number in `seq 6`; do \
# 		python3 replay_SEC_plus_STEP.py ${running_example_broken_dir}/trace_$$number.dat ; \
# 	done
