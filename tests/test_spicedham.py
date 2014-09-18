from unittest import TestCase

from spicedham import Spicedham, NoBackendFoundError, NoTokenizerFoundError
from mock import Mock, patch


class TestSpicedHam(TestCase):

    def test_classify(self):
        plugin0 = Mock()
        plugin1 = Mock()
        plugin2 = Mock()
        plugin0.classify.return_value = None
        plugin1.classify.return_value = .5
        plugin2.classify.return_value = .75
        mock_classifier_plugins = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        sh._classifier_plugins = mock_classifier_plugins
        # Test when some plugins return numbers and some return None
        value = sh.classify('classification data')
        self.assertEqual(value, 0.625)
        # Test when all plugins return one
        plugin1.classify.return_value = None
        plugin2.classify.return_value = None
        value = sh.classify('classification data')
        self.assertEqual(value, 0)

    def test_explain(self):
        plugin0 = Mock()
        plugin1 = Mock()
        plugin2 = Mock()
        plugin0.explain.return_value = None, 'test'
        plugin1.explain.return_value = .5, 'test'
        plugin2.explain.return_value = .75, 'test'
        mock_classifier_plugins = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        sh._classifier_plugins = mock_classifier_plugins
        # Test when some plugins return numbers and some return None
        value, explanation = sh.explain('classification data')
        self.assertEqual(value, 0.625)
        self.assertEqual(type(explanation), list)
        self.assertEqual(len(explanation), 3)
        # Test when all plugins return one
        plugin1.explain.return_value = None, 'test'
        plugin2.explain.return_value = None, 'test'
        value, explanation = sh.explain('classification data')
        self.assertEqual(type(explanation), list)
        self.assertEqual(len(explanation), 3)
        self.assertEqual(value, 0)

    def test_train(self):
        plugin0 = Mock()
        plugin1 = Mock()
        plugin2 = Mock()
        mock_classifier_plugins = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        sh._classifier_plugins = mock_classifier_plugins
        # Test when some plugins return numbers and some return None
        sh.train('classification data', True)
        self.assertTrue(plugin0.train.called)
        self.assertTrue(plugin1.train.called)
        self.assertTrue(plugin2.train.called)

    @patch('spicedham.Spicedham._load_backend')
    @patch('spicedham.Spicedham.all_subclasses')
    @patch('spicedham.Spicedham._load_tokenizer')
    def test_load_plugins(self, mock_load_backend, mock_all_subclasses,
                          mock_load_tokenizer):
        # Make _load_backend a Nop
        mock_load_backend = Mock()  # noqa
        mock_load_tokenizer = Mock()  # noqa
        plugin0 = Mock()
        plugin1 = Mock()
        plugin2 = Mock()
        mock_all_subclasses.return_value = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        sh._load_plugins()
        self.assertEqual(plugin0.called, True)
        self.assertEqual(plugin1.called, True)
        self.assertEqual(plugin2.called, True)

    @patch('spicedham.Spicedham._load_tokenizer')
    @patch('spicedham.Spicedham.all_subclasses')
    def test_load_backend(self, mock_all_subclasses, mock_load_tokenizer):
        backend0 = Mock()
        backend0.__name__ = 'SqlAlchemyWrapper'
        backend0Returns = Mock()
        backend0.return_value = backend0Returns
        backend1 = Mock()
        backend1.__name__ = 'NotSqlAlchemyWrapper'
        backend2 = Mock()
        backend2.__name__ = 'StillNotSqlAlchemyWrapper'
        mock_all_subclasses.return_value = [backend0, backend1, backend2]
        sh = Spicedham()
        sh._load_backend()
        self.assertEqual(sh.backend, backend0Returns)
        sh = Spicedham()
        mock_all_subclasses.return_value = []
        self.assertRaises(NoBackendFoundError, sh._load_backend)

    @patch('spicedham.Spicedham._load_backend')
    @patch('spicedham.Spicedham.all_subclasses')
    def test_load_tokenizer(self, mock_all_subclasses, mock_load_backend):
        tokenizer0 = Mock()
        tokenizer0.__name__ = 'SplitTokenizer'
        tokenizer0Returns = Mock()
        tokenizer0.return_value = tokenizer0Returns
        tokenizer1 = Mock()
        tokenizer1.__name__ = 'NotSqlAlchemyWrapper'
        tokenizer2 = Mock()
        tokenizer2.__name__ = 'StillNotSqlAlchemyWrapper'
        mock_all_subclasses.return_value = [tokenizer0, tokenizer1, tokenizer2]
        sh = Spicedham()
        sh._load_tokenizer()
        self.assertEqual(sh.tokenizer, tokenizer0Returns)
        sh = Spicedham()
        mock_all_subclasses.return_value = []
        self.assertRaises(NoTokenizerFoundError, sh._load_tokenizer)

    def test_all_subclasses(self):

        class parent(object):
            pass

        class child0(parent):
            pass

        class child1(parent):
            pass
        sh = Spicedham()
        result = sh.all_subclasses(parent)
        self.assertTrue(child0 in result)
        self.assertTrue(child1 in result)
        self.assertEqual(2, len(result))
