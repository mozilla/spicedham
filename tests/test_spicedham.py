#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_spicedham
----------------------------------

Tests for `spicedham` module.
"""
import os
import json
import tarfile
import unittest

from spicedham import SpicedHam


class TestSpicedham(unittest.TestCase):

    def setUp(self, tarball='corpus.tar.gz', test_data_dir='corpus'):
        if os.path.exists(test_data_dir):
            pass
        elif os.path.exists(tarball) :
            tr = tarfile.open(tarball)
            tr.extractall()
            tr.close()
        else:
            raise 'No test data found'
        self.sh = SpicedHam()
        dir_name = os.path.join(test_data_dir, 'train', 'ham')
        for file_name in os.listdir(dir_name):
            data = json.load(open(os.path.join(dir_name, file_name)))
            self.sh.train(data, False)

    def test_on_training_data(self, test_data_dir='corpus'):
        self._test_all_files_in_dir(os.path.join(test_data_dir, 'train', 'spam'), True)
        self._test_all_files_in_dir(os.path.join(test_data_dir, 'train', 'ham'), False)
        
    def test_on_control_data(self, test_data_dir='corpus'):
        self._test_all_files_in_dir(os.path.join(test_data_dir, 'control', 'spam'), True)
        self._test_all_files_in_dir(os.path.join(test_data_dir, 'control', 'ham'), False)

    def _test_all_files_in_dir(self, data_dir, should_be_spam):
        tuning_factor = 0.5
        for filename in os.listdir(data_dir):
            f = open(os.path.join(data_dir,  filename), 'r')
            probability = self.sh.is_spam(json.load(f))
            self.assertGreaterEqual(probability, 0.0)
            self.assertLessEqual(probability, 1.0)
            if should_be_spam:
                self.assertGreaterEqual(tuning_factor, 0.5)
            else:
                self.assertLessEqual(tuning_factor, 0.5)

if __name__ == '__main__':
    unittest.main()
