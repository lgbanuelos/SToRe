# Secure Conformance Checking using Token-based Replay and Homomorphic Encryption

This is the implementation of the papaer Secure Conformance Checking using Token-based
Replay and Homomorphic Encryption.

### Prerequisites:

1. Ubuntu 22.04 LTS
2. Python 3.10
3. [Concrete Library](https://github.com/zama-ai/concrete):
  ```
    pip install -U pip wheel setuptools
    pip install concrete-python
  ```

There are four variants of the step function implementation:

1. replay_clear.py - Implementation of the Secure Token-based Replay algorithm (without the computation of mcpr tokens).
2. replay_clear_mcpr.py - Implementation of the Secure Token-based Replay algorithm.
3. replay_cipher.py - Implementation of the encrypted version of Secure Token-based Replay algorithm without the computation of mcpr token.
4. replay_cipher_mcpr.py - Implementation of the encrypted version of Secure Token-based Replay algorithm.

(mcpr = missing, produced, consumed, remainder)

The scripts required a input parameter with the path of the file containing the trace to be checked, one per line.

```
python3 replay_clear.py data/my_runnin_example.dat
python3 replay_clear_mcpr.py data/my_runnin_example.dat
python3 replay_cipher.py data/my_runnin_example.dat
python3 replay_cipher_mcpr.py data/my_runnin_example.dat
```

Example of the `my_runnign_example.dat` file.

```
register request
check ticket
examine casually
decide
reject request
```

We use the data set from the pm4y [Token Replay notebook](https://github.com/process-intelligence-solutions/pm4py/blob/release/notebooks/4_conformance_checking.ipynb)
The data set are preprocessed and stored in:

```
data/running_example/
data/running_example_broken/
```

We include a Makefile (tested on ubuntu 22) to help to run the experiments:

```
  make run_clear
```

```
  make run_clear_mcpr
```
```
  make run_cipher
```
```
  make run_cipher_mcpr
```
