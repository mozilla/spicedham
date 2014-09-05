from unittest import TestCase

from spicedham import Spicedham
from mock import Mock, patch


class TestSpicedHamAPI(TestCase):

    @patch('spicedham.Spicedham._classifier_plugins')
    def test_classify(self, mock_plugins):
        sh = Spicedham()
        plugin0 = Mock()
        plugin0.classify.return_value = .5
        plugin1 = Mock()
        plugin1.classify.return_value = .75   
        plugin2 = Mock()
        plugin2.classify.return_value = None
        mock_plugins.__iter__.return_value = [plugin0, plugin1, plugin2]
        # Test when some plugins return numbers and some return None
        value = sh.classify(['classifying', 'data'])
        self.assertEqual(value, 0.625)
        # Test when all plugins return one
        plugin0.classify.return_value = None
        plugin1.classify.return_value = None   
        value = sh.classify(['classifying', 'data'])
        self.assertEqual(value, 0)

    @patch('spicedham.iter_entry_points')
    @patch('spicedham.Spicedham.backend')
    def test_load_backend(self, mock_backend, mock_iter_entry_points):
        sh = Spicedham()
        mock_backend = None
        mock_django_orm = Mock()
        mock_iter_entry_points = Mock()
        # mock_plugin_class = Mock()
        # mock_plugin_object = Mock()
        # mock_plugin_class.return_value = mock_plugin_object
        # mock_django_orm.load.return_value = mock_plugin_class()
        #h= mock_django_orm.name = 'djangoorm'
        # mock_sqlalchemy_orm = Mock()
        #mock_sqlalchemy_orm.name = 'sqlalchemy'
        #mock_plugin_class.return_value = mock_plugin_object
        #mock_sqlalchemy_orm.load.return_value = mock_plugin_class()
        #mock_iter_entry_points.__iter__.return_value = [mock_django_orm,
        #    mock_sqlalchemy_orm]
        # Test the first run with the django_orm plugin
        
        ret = sh._load_backend()
        print 'mm', mock_iter_entry_points.mock_calls
        self.assertEqual(ret, mock_plugin_object)
        # Test the second run with the django_orm plugin
        ret = sh._load_backend()
        self.assertEqual(ret, mock_plugin_class.return_value)
        # rest the backend for the next test
        mock_backend = None
        mock_iter_entry_points.return_value = [mock_django_orm,
            mock_sqlalchemy_orm]
        # Test the first run with the sqlalchemy plugin
        ret = sh._load_backend()
        self.assertEqual(ret, mock_plugin_class.return_value)
        # Test the second run with the sqlalchemy plugin
        ret = sh._load_backend()
        self.assertEqual(ret, mock_plugin_class.return_value)
        

        
    @patch('spicedham.Spicedham._load_backend')
    @patch('spicedham.iter_entry_points')
    def test_load_plugins(self, mock_iter_entry_points, mock_load_backend):
         #plugin0 = Mock()
         plugin0Object = Mock()
         #plugin0Class = Mock(return_value=plugin0Object)
         #plugin0.load = Mock(return_value=plugin0Class)
         #plugin1 = Mock()
         plugin1Object = Mock()
         #plugin1Class = Mock(return_value=plugin1Object)
         #plugin1.load = Mock(return_value=plugin1Class)
         #plugin2 = Mock()
         plugin2Object = Mock()
         #plugin2Class = Mock(return_value=plugin2Object)
         #plugin2.load = Mock(return_value=plugin2Class)
         input_plugins = [plugin0Object, plugin1Object, plugin2Object]
         expected_plugins = [plugin0Object.load, plugin1Object.load, plugin2Object.load]
         mock_iter_entry_points.return_value = input_plugins
         self.assertEqual(spicedham._plugins, None)
         # now load the plugins
         load_plugins()
         mock_iter_entry_points.assert_called_with(group='spicedham.classifiers', name=None)
         self.assertEqual(spicedham._plugins, expected_plugins)
         # now load the plugins again, they should not change
         mock_iter_entry_points.called = False
         load_plugins()
         self.assertEqual(mock_iter_entry_points.called, False)
         self.assertEqual(spicedham._plugins, input_plugins)
