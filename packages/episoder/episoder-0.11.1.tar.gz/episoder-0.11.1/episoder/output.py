# episoder, https://code.ott.net/episoder
#
# Copyright (C) 2004-2025 Stefan Ott. All rights reserved.
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
from email.message import EmailMessage
from smtplib import SMTP
from sys import stdout
from typing import Optional

from .database import Episode


# pylint: disable=too-few-public-methods
class EpisodeRenderer:
    def __init__(self, episode_format: str, date_format: str) -> None:
        self._format = episode_format
        self._date_format = date_format

    def format(self, episode: Episode) -> str:
        string = self._format

        airdate = episode.airdate.strftime(self._date_format)
        string = string.replace("%airdate", airdate)
        string = string.replace("%show", str(episode.show.name))
        string = string.replace("%season", str(episode.season))
        string = string.replace("%epnum", f"{episode.episode:02d}")
        string = string.replace("%eptitle", str(episode.title))
        string = string.replace("%totalep", str(episode.totalnum))
        string = string.replace("%prodnum", str(episode.prodnum))

        return string


class ColorfulRenderer(EpisodeRenderer):
    RED = "\033[31;1m"
    CYAN = "\033[36;1m"
    GREY = "\033[30;0m"
    GREEN = "\033[32;1m"
    YELLOW = "\033[33;1m"

    def __init__(self, fmt: str, date_format: str, dest=stdout) -> None:
        super().__init__(fmt, date_format)
        self._dest = dest

    def _color(self, episode: Episode, yesterday: date, today: date,
               tomorrow: date) -> str:
        if episode.airdate == yesterday:
            return ColorfulRenderer.RED
        if episode.airdate == today:
            return ColorfulRenderer.YELLOW
        if episode.airdate == tomorrow:
            return ColorfulRenderer.GREEN
        if episode.airdate > tomorrow:
            return ColorfulRenderer.CYAN

        return ColorfulRenderer.GREY

    def render(self, episodes: list[Episode], today: date) -> None:
        yesterday = today - timedelta(1)
        tomorrow = today + timedelta(1)

        for episode in episodes:
            text = self.format(episode)
            color = self._color(episode, yesterday, today, tomorrow)
            self._dest.write(f'{color}{text}{ColorfulRenderer.GREY}\n')


class ColorlessRenderer(EpisodeRenderer):
    def __init__(self, fmt: str, date_format: str, dest=stdout) -> None:
        super().__init__(fmt, date_format)
        self._dest = dest

    def render(self, episodes: list[Episode], _: date) -> None:
        for episode in episodes:
            text = self.format(episode)
            self._dest.write(f'{text}\n')


class EmailNotifier:
    def __init__(self, server: str, port: int, smtp=SMTP) -> None:
        self._server = server
        self._port = port
        self._smtp = smtp
        self._user: Optional[str] = None
        self._password: Optional[str] = None

        self.use_tls = False

    def __str__(self) -> str:
        return "EmailNotifier"

    def __repr__(self) -> str:
        fmt = 'EmailNotifier("%s", %d, %s)'
        return fmt % (self._server, self._port, str(self._smtp))

    def login(self, user: str, password: str) -> None:
        self._user = user
        self._password = password

    def _dump(self, msg: EmailMessage) -> None:
        print(f'From: {msg["to"]}')
        print(f'To: {msg["to"]}')
        print(f'Subject: {msg["Subject"]}')
        print(msg.get_content())

    def send(self, body: str, to: str, pretend: bool = False) -> None:
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = 'Upcoming TV episodes'
        message['From'] = to
        message['To'] = to

        if pretend:
            self._dump(message)
            return

        server = self._smtp(self._server, self._port)

        if self.use_tls:
            server.starttls()
        if self._user:
            server.login(self._user, self._password)

        server.send_message(message)
        server.quit()


class NewEpisodesNotification(EpisodeRenderer):
    def __init__(self, episodes: list[Episode], fmt: str,
                 date_format: str) -> None:
        super().__init__(fmt, date_format)
        self._episodes = episodes

    def __str__(self) -> str:
        return f'Notification: {len(self._episodes)} new episode(s)'

    def __repr__(self) -> str:
        eps = f"<({len(self._episodes)} x Episode)"
        fmt = 'NewEpisodesNotification(%s, "%s", "%s")'
        return fmt % (eps, self._format, self._date_format)

    def get(self) -> str:
        return ''.join(f'{self.format(e)}x\n' for e in self._episodes)

    def send(self, notifier: EmailNotifier, to: str,
             pretend: bool = False) -> None:
        body = "Your upcoming episodes:\n\n"

        for episode in self._episodes:
            body += f"{self.format(episode)}\n"

            if not pretend:
                episode.notified = date.today()

        notifier.send(body, to, pretend)
