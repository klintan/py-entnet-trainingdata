#!/usr/bin/env bash
csplit training_data_1_supported_fact.txt $(( $(wc -l < training_data_1_supported_fact.txt) * 2 / 10 + 1))