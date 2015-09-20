import os
from configparser import ConfigParser

class WithInfoFileGetter(object):
    """
    Only gets files that have configuration files ending with specific extensions,
    nominally 'yapsy-plugin'
    """
    def __init__(self, extensions=["yapsy-plugin"]):
        self.extensions = extensions

    def set_file_extensions(self, extensions):
        self.extensions = extensions

    def add_file_extensions(self, extensions):
        try:
            self.extensions.extend(extensions)
        except TypeError:
            extensions = list(extensions)
            self.extensions.extend(extensions)
            
    def valid_plugin(self, filepath):
        plugin_validatation = False
        try:
            for extension in self.extensions:
                if filename.endswith(".{}".format(extension)):
                    plugin_validatation = True
                    break
        except TypeError:
            # try to make extensions a list and recurse
            self.extensions = list(self.extensions)
            plugin_validation = self.valid_plugin(filename)

        return plugin_validation

    def get_info_and_filepaths(self, dir_path):
        infos = self.get_plugin_infos(dir_path)
        filepaths = self.get_plugin_filepaths(dir_path, infos)
        return infos, filepaths
    
    def get_plugin_infos(self, dir_path)
        config_parser = ConfigParser()
        try:
            config_parser.read_file(infoFileObject)
        except Exception:
            return (None, None, None)

        if not config_parser.has_section("Core"):
            return (None, None, None)

        if not config_parser.has_option("Core","Name") or not config_parser.has_option("Core","Module"):
            return (None, None, None)
        # check that the given name is valid

        name = config_parser.get("Core", "Name")
        name = name.strip()
        if PLUGIN_NAME_FORBIDEN_STRING in name:
            return (None, None, None)
        return (name, config_parser.get("Core", "Module"), config_parser)

    def _get_filepath_and_info(self, path):
        if self.valid_plugin(path):
            info = self.get_info(path)
            plugin_filepath = info['path']
            return plugin_filepath, info
            
    def get_plugin_filepaths(self, dir_path, infos=None):
        # Enforce uniqueness of filepaths in `PluginLocator`
        filepaths = []
        # if we've already got the infos list, get plugin filepath from those
        # else parse through the dir_path
        if infos is not None:
            for info in infos:
                filepaths.append(info.filepath)
        else:
            for filename in os.listdir(dir_path):
                filepath, info = self._get_filepath_and_info(os.path.join(dir_path, filename))
                if filepath is not None and info is not None:
                    filepaths.append(filepath)

        return filepaths
