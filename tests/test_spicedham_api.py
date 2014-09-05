from unittest import TestCase

from spicedham import Spicedham, NoBackendFoundError
from spicedham.sqlalchemywrapper import SqlAlchemyWrapper
from mock import Mock, patch


class TestSpicedHamAPI(TestCase):

    @patch('spicedham.Spicedham.all_subclasses')
    def test_classify(self, mock_all_subclasses):
        plugin0 = Mock()
        plugin0obj = Mock()
        plugin0.return_value = plugin0obj
        plugin0.__name__ = "SqlAlchemyWrapper"
        plugin0obj.classify.return_value = .5
        plugin1 = Mock()
        plugin1obj = Mock()
        plugin1.return_value = plugin1obj
        plugin1.__name__ = "NotSqlAlchemyWrapper"
        plugin1obj.classify.return_value = .75
        plugin2 = Mock()
        plugin2obj = Mock()
        plugin2.return_value = plugin2obj
        plugin2.__name__ = "StillNotSqlAlchemyWrapper"
        plugin2obj = Mock()
        plugin2.return_value = plugin2obj
        plugin2obj.classify.return_value = None
        mock_all_subclasses.return_value = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        # Test when some plugins return numbers and some return None
        value = sh.classify(['classifying', 'data'])
        self.assertEqual(value, 0.625)
        # Test when all plugins return one
        plugin0obj.classify.return_value = None
        plugin1obj.classify.return_value = None   
        value = sh.classify(['classifying', 'data'])
        self.assertEqual(value, 0)

    @patch('spicedham.Spicedham.all_subclasses')
    def test_load_backend(self, mock_all_subclasses):
        plugin0 = Mock()
        plugin0obj = Mock()
        plugin0.return_value = plugin0obj
        plugin0.__name__ = "SqlAlchemyWrapper"
        plugin0obj.classify.return_value = .5
        plugin1 = Mock()
        plugin1obj = Mock()
        plugin1.return_value = plugin1obj
        plugin1.__name__ = "NotSqlAlchemyWrapper"
        plugin1obj.classify.return_value = .75
        plugin2 = Mock()
        plugin2obj = Mock()
        plugin2.return_value = plugin2obj
        plugin2.__name__ = "StillNotSqlAlchemyWrapper"
        plugin2obj = Mock()
        plugin2.return_value = plugin2obj
        plugin2obj.classify.return_value = None
        mock_all_subclasses.return_value = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        # Test when some plugins return numbers and some return None
        value = sh.train(['classifying', 'data'], True)
        self.assertTrue(plugin0obj.train.called)
       

        
    @patch('spicedham.Spicedham._load_backend')
    def test_load_plugins(self, mock_load_backend):
        plugin0 = Mock()
        plugin0obj = Mock()
        plugin0.return_value = plugin0obj
        plugin0.__name__ = "SqlAlchemyWrapper"
        plugin0obj.classify.return_value = .5
        plugin1 = Mock()
        plugin1obj = Mock()
        plugin1.return_value = plugin1obj
        plugin1.__name__ = "NotSqlAlchemyWrapper"
        plugin1obj.classify.return_value = .75
        plugin2 = Mock()
        plugin2obj = Mock()
        plugin2.return_value = plugin2obj
        plugin2.__name__ = "StillNotSqlAlchemyWrapper"
        plugin2obj = Mock()
        plugin2.return_value = plugin2obj
        plugin2obj.classify.return_value = None
        mock_all_subclasses.return_value = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        # Test when some plugins return numbers and some return None
        value = sh.train(['classifying', 'data'], True)
        self.assertTrue(plugin0obj.train.called)

    @patch('spicedham.Spicedham.all_subclasses')
    @patch('spicedham.Spicedham._load_backend')
    def test_load_plugins(self, mock_all_subclasses, mock_load_backend):
        mock_load_backend = None
        plugin0 = Mock()
        plugin1 = Mock()
        plugin2 = Mock()
        mock_all_subclasses.return_value = [plugin0, plugin1, plugin2]
        sh = Spicedham()
        result = sh._load_backend()
        self.assertIn(plugin0, result)
        self.assertIn(plugin1, result)
        self.assertIn(plugin2, result)
        

    @patch('spicedham.Spicedham.all_subclasses')
    def test_load_backend(self, mock_all_subclasses):
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


    def test_all_subclasses(self):
        class parent(object):
            pass
        class child0(parent):
            pass
        class child1(parent):
            pass
        sh = Spicedham()
        result = sh.all_subclasses(parent)
        self.assertIn(child0, result)
        self.assertIn(child1, result)
        self.assertEqual(2, len(result))
