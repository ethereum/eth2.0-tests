all:
	python eth2_testgen/shuffling/tgen_shuffling.py test_vectors/test_vector_shuffling.yml
	python eth2_testgen/bls/tgen_bls.py test_vectors/test_bls.yml
