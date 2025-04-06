"""
# Based on Modmail (https://github.com/modmail-dev/Modmail)
# Copyright (C) [Original Year] Modmail Developers
# Modifications by martinbndr (2025)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
from copy import deepcopy
import os
import typing

class _Default:
    pass

Default = _Default()

class PluginDbManager:
    def __init__(
            self, 
            plugin,
            config_keys
            ):
        self.plugin = plugin
        self.config_keys = config_keys

        self.bot = plugin.bot
        
        self.defaults = {**config_keys}
        self.all_keys = set(self.defaults.keys())

        self._cache = {}

    @property
    def db(self):
        if not hasattr(self, "_db"):
            self._db = self.bot.api.get_plugin_partition(self.plugin)
        return self._db

    async def setup(self) -> dict:
        #self.logger.debug("Setting up PluginDbManager")
        data = deepcopy(self.defaults)
        self._cache = data

        bot_config = await self.db.find_one({"type": "config", "bot_id": str(self.bot.user.id)})
        if not bot_config:
            await self.db.insert_one({"type": "config", "bot_id": str(self.bot.user.id)})
            #self.logger.debug("Configuration collection created as not existing before.")
        await self.refresh()
        return self._cache
    
    async def update(self):
        """Updates the config with data from the cache"""
        default_config = self.filter_default(self._cache)
        toset = self.filter_valid(default_config)
        unset = self.filter_valid({k: 1 for k in self.all_keys if k not in default_config})

        update_query = {}
        if toset:
            update_query["$set"] = toset
        if unset:
            update_query["$unset"] = unset
        if update_query.keys():
            #self.logger.debug("Updated plugin configuration to db.")
            await self.db.update_one({"type": "config", "bot_id": str(self.bot.user.id)}, update_query)
    
    async def refresh(self) -> dict:
        for k, v in (await self.db.find_one({"type": "config", "bot_id": str(self.bot.user.id)})).items():
            k = k.lower()
            if k in self.all_keys:
                self._cache[k] = v
            #self.logger.debug("Successfully fetched configurations from database.")
        return self._cache

    def __getitem__(self, key: str) -> typing.Any:
        return self.get(key)
    
    def __setitem__(self, key: str, item: typing.Any) -> typing.Any:
        key = key.lower()
        if key not in self.all_keys:
            return None
            #self.logger.warning("Invalid configuration key %s", key)
        self._cache[key] = item
        return deepcopy(self._cache[key])

    def __delitem__(self, key: str) -> None:
        return self.remove(key)
    
    def get(self, key: str) -> typing.Any:
        key = key.lower()
        if key not in self.all_keys:
            return None
            #self.logger.warning("Invalid configuration key %s", key)
        if key not in self._cache:
            self._cache[key] = deepcopy(self.defaults[key])
        value = self._cache[key]
        return value
        
    async def set(self, key: str, item: typing.Any) -> None:
        return self.__setitem__(key, item)

    def remove(self, key: str) -> typing.Any:
        key = key.lower()
        #self.logger.info("Removing %s.", key)
        if key not in self.all_keys:
            self.logger.warning("Configuration key %s is invalid.", key)
        if key in self._cache:
            del self._cache[key]
        self._cache[key] = deepcopy(self.defaults[key])
        return self._cache[key]

    def items(self) -> typing.Iterable:
        return self._cache.items()
    
    def filter_valid(self, data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return {
            k.lower(): v
            for k, v in data.items()
            if k.lower() in self.all_keys
        }

    def filter_default(self, data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        filtered = {}
        for k, v in data.items():
            default = self.defaults.get(k.lower(), Default)
            if default is Default:
                #self.logger.error("Unexpected configuration detected: %s.", k)
                continue
            if v != default:
                filtered[k.lower()] = v
        return filtered