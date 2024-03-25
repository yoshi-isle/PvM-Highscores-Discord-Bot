import typing
from enum import Enum

import discord
from discord import app_commands

import constants.forum_data.bosses as bosses
import constants.forum_data.chambers_of_xeric as chambers_of_xeric
import constants.forum_data.dt2bosses as dt2bosses
import constants.forum_data.misc_activities as misc_activities
import constants.forum_data.theatre_of_blood as theatre_of_blood
import constants.forum_data.tombs_of_amascut as tombs_of_amascut
import constants.forum_data.trials as trials


class AutoComplete:
    TOB_MODES = Enum("TOB_MODES", ["Normal", "Hard"])
    COX_MODES = Enum("COX_MODES", ["Normal", "Challenge"])
    TOA_MODES = Enum("TOA_MODES", ["Normal", "Expert"])
    TOB_GROUPSIZES = Enum("TOB_GROUPSIZES", ["1", "2", "3", "4", "5"])
    COX_GROUPSIZES = Enum("COX_GROUPSIZES", ["1", "2", "3", "5"])
    TOA_GROUPSIZES = Enum("TOA_GROUPSIZES", ["1", "2", "3", "5"])

    async def submit_tob_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in theatre_of_blood.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]

    async def submit_cox_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in chambers_of_xeric.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]

    async def submit_toa_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in tombs_of_amascut.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]

    async def submit_trial_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in trials.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]

    async def submit_dt2_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in dt2bosses.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]

    async def submit_boss_pb_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in bosses.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]

    # Submit misc activities
    async def submit_misc_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> typing.List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=boss_name["boss_name"], value=boss_name["boss_name"])
            for boss_name in misc_activities.INFO
            if current.lower() in boss_name["boss_name"].lower()
        ]
