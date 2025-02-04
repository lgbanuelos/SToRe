running_example_dir = data/running_example/
running_example_broken_dir = data/running_example_broken/
#=========================================================================== fiting
run_clear:
	for number in `seq 6` ; do \
		python3 replay_clear.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_clear_mcpr:
	for number in `seq 6` ; do \
		python3 replay_clear_mcpr.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_cipher:
	for number in `seq 6`; do \
		python3 replay_cipher.py ${running_example_dir}/trace_$$number.dat ; \
	done

run_cipher_mcpr:
	for number in `seq 6`; do \
		python3 replay_cipher_new.py ${running_example_dir}/trace_$$number.dat ; \
	done
#=========================================================================== broken
run_clear_broken:
	for number in `seq 6` ; do \
		python3 replay_clear.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_clear_mcpr_broken:
	for number in `seq 6` ; do \
		python3 replay_clear_mcpr.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_cipher_broken:
	for number in `seq 6` ; do \
		python3 replay_cipher.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done

run_cipher_mcpr_broken:
	# for number in 1 ; do \
	for number in `seq 6`; do \
		python3 replay_cipher_new.py ${running_example_broken_dir}/trace_$$number.dat ; \
	done
