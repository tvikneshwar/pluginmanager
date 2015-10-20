import os
import sys
import unittest
import tempfile
from pluginmanager.module_manager import ModuleManager


class TestClass:
    pass


class TestModuleManager(unittest.TestCase):
    def setUp(self):
        self.module_manager = ModuleManager()

    def test_set_module_filters(self):
        test_obj = TestClass()
        previous_module = self.module_manager.module_filters[0]
        self.module_manager.set_module_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_filters)
        self.assertNotIn(previous_module, self.module_manager.module_filters)

    def test_add_module_filter(self):
        test_obj = TestClass()
        self.module_manager.add_module_filters(test_obj)
        self.assertIn(test_obj, self.module_manager.module_filters)

    def test_add_blacklisted_filepaths(self):
        test_filepath = 'fancy/dir'
        self.module_manager.add_blacklisted_filepaths(test_filepath)
        test_filepaths = ['dir/d', 'dir/b']
        self.module_manager.add_blacklisted_filepaths(test_filepaths)
        blacklisted = self.module_manager.get_blacklisted_filepaths()
        self.assertIn(test_filepath, blacklisted)
        self.assertIn(test_filepaths[0], blacklisted)

    def test_set_blacklist_filepaths(self):
        removed_dir = 'test/dir'
        self.module_manager.add_blacklisted_filepaths(removed_dir)
        single_dir = 'dir/b'
        self.module_manager.set_blacklisted_filepaths(single_dir)
        self.assertIn(single_dir, self.module_manager.blacklisted_filepaths)
        mulitple_dirs = ['dir/a', 'dir/b']
        self.module_manager.set_blacklisted_filepaths(mulitple_dirs)
        self.assertIn(mulitple_dirs[0],
                      self.module_manager.blacklisted_filepaths)

    def test_valid_filepath(self):
        blacklist_filepath = 'dir/blacklist'
        processed_filepath = 'dir/processed'
        test_filepath = 'dir/test'
        self.module_manager.add_blacklisted_filepaths(blacklist_filepath)
        self.module_manager.processed_filepaths['test'] = processed_filepath
        # test blacklisted filepath
        valid = self.module_manager._valid_filepath(blacklist_filepath)
        self.assertFalse(valid)
        # test processed_filepath
        valid = self.module_manager._valid_filepath(processed_filepath)
        self.assertFalse(valid)
        # test regular dir
        valid = self.module_manager._valid_filepath(test_filepath)
        self.assertTrue(valid)

    def test_process_filepath(self):
        test_dir = os.path.dirname(__file__)
        expected_filepath = os.path.join(test_dir, '__init__.py')
        processed_file = self.module_manager._process_filepath(test_dir)
        self.assertEqual(expected_filepath, processed_file)
        no_ext = expected_filepath[:-3]
        processed_ext = self.module_manager._process_filepath(no_ext)
        self.assertEqual(processed_ext, expected_filepath)

    def _load_modules(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            code = 'PLUGINS = []\nfive = 5.0'
            filename = os.path.join(temp_dir, "mod_test.py")
            f = open(filename, 'w+')
            f.write(code)
            f.close()
            module = self.module_manager.load_modules(filename)
            module = module.pop()
        return module, filename

    def test_get_modules(self):
        module, _ = self._load_modules()
        name = module.__name__
        name = [name]
        got_modules = self.module_manager._get_modules(name)
        self.assertIn(module, got_modules)
        loaded_modules = self.module_manager.get_loaded_modules()
        self.assertIn(module, loaded_modules)
    """
    def test_collect_plugins(self):
        self.module_manager.module_filters = []
        module, _ = self._load_modules()
        plugins = self.module_manager.collect_plugins(module)
    """

    def test_load_modules(self):
        module, filename = self._load_modules()

        self.assertIn(filename,
                      self.module_manager.processed_filepaths.values())
        self.assertEqual(module.PLUGINS, [])
        self.assertEqual(module.five, 5.0)

    def test_update_internal_state(self):
        module, filename = self._load_modules()
        module_name = module.__name__
        processed_fps = self.module_manager.processed_filepaths
        self.assertIn(module_name, processed_fps.keys())
        del module
        del sys.modules[module_name]
        self.module_manager._update_internal_state()
        self.assertNotIn(module_name, processed_fps.keys())