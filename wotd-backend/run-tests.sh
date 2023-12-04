#!/bin/bash

echo 'running test suite'
python3 -m unittest -k test_history_stack controller_test.py 

