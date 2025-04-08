# episoder, https://code.ott.net/episoder
# -*- coding: utf8 -*-
# # Copyright (C) 2004-2024 Stefan Ott. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import date, timedelta
from unittest import TestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from episoder.database import Show, Episode
from episoder.output import ColorfulRenderer, ColorlessRenderer


class TestOutput(TestCase):
    def setUp(self):
        self.show = Show("Test show 36")
        self.show.show_id = 36
        self.io = StringIO()

        then = date(2008, 1, 1)
        self.episode = Episode("Episode 41", 2, 5, then, "NX01", 3)
        self.episode.show = self.show

    def test_render_airdate_colorless(self):
        renderer = ColorlessRenderer("%airdate", "%Y%m%d", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "20080101\n")

        self.episode.airdate = date(2015, 2, 3)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "20080101\n20150203\n")

    def test_render_show_name(self):
        renderer = ColorlessRenderer("%show", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "Test show 36\n")

        self.show.name = "Test 55"
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "Test show 36\nTest 55\n")

    def test_render_show_name_none(self):
        renderer = ColorlessRenderer("%show", "", self.io)

        self.show.name = None
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "None\n")

    def test_render_season_number(self):
        renderer = ColorlessRenderer("%season", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "2\n")

        self.episode.season = 12
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "2\n12\n")

    def test_render_episode_number(self):
        renderer = ColorlessRenderer("%epnum", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "05\n")

        self.episode.episode = 22
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "05\n22\n")

    def test_render_episode_title(self):
        renderer = ColorlessRenderer("%eptitle", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "Episode 41\n")

        self.episode.title = "Episode 8"
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "Episode 41\nEpisode 8\n")

    def test_render_episode_without_title(self):
        renderer = ColorlessRenderer("%eptitle", "", self.io)
        self.episode.title = None
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "None\n")

    def test_render_total_episode_number(self):
        renderer = ColorlessRenderer("%totalep", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "3\n")

        self.episode.totalnum = 90
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "3\n90\n")

    def test_render_prodnum(self):
        renderer = ColorlessRenderer("%prodnum", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "NX01\n")

        self.episode.prodnum = "ABCD"
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "NX01\nABCD\n")

    def test_render_episode_without_prodnum(self):
        renderer = ColorlessRenderer("%prodnum", "", self.io)
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "NX01\n")

        self.episode.prodnum = None
        renderer.render([self.episode], date.today())
        self.assertEqual(self.io.getvalue(), "NX01\nNone\n")

    def test_render_combined(self):
        self.show.name = "Frasier"
        self.episode.airdate = date(1998, 9, 24)
        self.episode.season = 6
        self.episode.episode = 1
        self.episode.title = "Good Grief"

        fmt = "%airdate: %show %seasonx%epnum - %eptitle"
        renderer = ColorlessRenderer(fmt, "%Y-%m-%d", self.io)
        renderer.render([self.episode], date.today())

        out = self.io.getvalue()
        self.assertEqual(out, "1998-09-24: Frasier 6x01 - Good Grief\n")

    def test_render_colors(self):
        today = date.today()

        # Two days ago -> grey
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        then = today - timedelta(2)
        self.episode.airdate = then
        expect = f"\033[30;0m{then.strftime('%Y')}\033[30;0m\n"
        renderer.render([self.episode], today)
        self.assertEqual(expect, io.getvalue())

        # Yesterday -> red
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        then = today - timedelta(1)
        self.episode.airdate = then
        expect = f"\033[31;1m{then.strftime('%Y')}\033[30;0m\n"
        renderer.render([self.episode], today)
        self.assertEqual(expect, io.getvalue())

        # Today -> yellow
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        then = today
        self.episode.airdate = then
        expect = f"\033[33;1m{then.strftime('%Y')}\033[30;0m\n"
        renderer.render([self.episode], today)
        self.assertEqual(expect, io.getvalue())

        # Tomorrow -> green
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        then = today + timedelta(1)
        self.episode.airdate = then
        expect = f"\033[32;1m{then.strftime('%Y')}\033[30;0m\n"
        renderer.render([self.episode], today)
        self.assertEqual(expect, io.getvalue())

        # The future -> cyan
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        then = today + timedelta(2)
        self.episode.airdate = then
        expect = f"\033[36;1m{then.strftime('%Y')}\033[30;0m\n"
        renderer.render([self.episode], today)
        self.assertEqual(expect, io.getvalue())

    def test_render_colors_different_date(self):
        today = date(2001, 7, 10)

        # Two days ago -> grey
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        self.episode.airdate = date(2001, 7, 8)
        renderer.render([self.episode], today)
        self.assertEqual("\033[30;0m2001\033[30;0m\n", io.getvalue())

        # Yesterday -> red
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        self.episode.airdate = date(2001, 7, 9)
        renderer.render([self.episode], today)
        self.assertEqual("\033[31;1m2001\033[30;0m\n", io.getvalue())

        # Today -> yellow
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        self.episode.airdate = date(2001, 7, 10)
        renderer.render([self.episode], today)
        self.assertEqual("\033[33;1m2001\033[30;0m\n", io.getvalue())

        # Tomorrow -> green
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        self.episode.airdate = date(2001, 7, 11)
        renderer.render([self.episode], today)
        self.assertEqual("\033[32;1m2001\033[30;0m\n", io.getvalue())

        # The future -> cyan
        io = StringIO()
        renderer = ColorfulRenderer("%airdate", "%Y", io)
        self.episode.airdate = date(2001, 7, 12)
        renderer.render([self.episode], today)
        self.assertEqual("\033[36;1m2001\033[30;0m\n", io.getvalue())
