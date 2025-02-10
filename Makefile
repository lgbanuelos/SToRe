running_example_dir = data/running_example/
running_example_broken_dir = data/running_example_broken/
#=========================================================================== fiting
run_CLR:
	for number in `seq 6` ; do \
		python3 replay_CLR.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_CLR_plus:
	for number in `seq 6` ; do \
		python3 replay_CLR_plus.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_SEC:
	for number in `seq 6`; do \
		python3 replay_SEC.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_SEC_plus:
	for number in `seq 6`; do \
		python3 replay_SEC_plus.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_SEC_plus_STEP:
	for number in `seq 6`; do \
		python3 replay_SEC_plus_STEP.py ${running_example_dir}/trace_$$number.dat ; \
	done

#=========================================================================== broken
run_CLR_broken:
	for number in `seq 6` ; do \
		python3 replay_CLR.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_CLR_plus_broken:
	for number in `seq 6` ; do \
		python3 replay_CLR_plus.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_SEC_broken:
	for number in `seq 6` ; do \
		python3 replay_SEC.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_SEC_plus_broken:
	for number in `seq 6`; do \
		python3 replay_SEC_plus.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_SEC_plus_STEP_broken:
	for number in `seq 6`; do \
		python3 replay_SEC_plus_STEP.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done
