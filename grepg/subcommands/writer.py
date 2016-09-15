import os
import yaml
from grepg.util import create_file

class ConfigFileWriter(object):
    def update_config(self, new_values, config_filename):
        """Update config file with new values.
        This method will update the config file with
        new key value pairs.

        * If the ``config_filename`` does not exist, it will
          be created.  Any parent directories will also be created.
        * Any existing lines that are specified by ``new_values``
          **will not be touched**.  This ensures that commented out
          values are left unaltered.
        :type new_values: dict
        :param new_values: The values to update
        :type config_filename: str
        :param config_filename: The config filename where we will write values
        """
        if not os.path.isfile(config_filename):
            create_file(config_filename)
        with open(config_filename, 'w') as outfile:
            yaml.dump(new_values, outfile, default_flow_style=False)




