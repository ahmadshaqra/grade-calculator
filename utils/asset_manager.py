"""
    asset_manager.py

    Contains the asset manager utility class.
"""

import os
import sys


class AssetManager:
    """
        Manages all assets in the program.
    """

    @classmethod
    def get_asset(cls, filename: str) -> str:
        """
            Returns the filepath of the desired asset.

            Args:
                filename (str): the name of the asset to retrieve.

            Returns:
                str: the absolute path of the asset.
        """

        # attempts to get base path from pyinstaller
        try:
            base = sys._MEIPASS

        # falls back to absolute path of current directory
        except AttributeError:
            base = os.path.abspath(".")

        # returns absolute path of the asset
        return os.path.join(base, "assets", filename)
