import json
import re
import sys
from datetime import datetime, timedelta

import requests

_APP_VERSION = ""
_APP_NAME = "FLO"
_USER_AGENT = "okhttp/4.9.2"
_CHART_API_URL = "https://api.music-flo.com/display/v1/browser/chart/1/list?mixYn=N"


class FloChartRequestException(Exception):
    pass


class FloChartParseException(Exception):
    pass


class ChartEntry:
    """Represents an entry on a chart.
    Attributes:
        title: The title of the track
        artist: The name of the artist.
        image: The URL of the cover image for the track
        lastPos: The track's last position on the previous period.
        rank: The track's current rank position on the chart.
        isNew: Whether the track is new to the chart.
    """

    def __init__(self, title: str, artist: str, image: str, lastPos: int, rank: int, isNew: bool):
        self.title = title
        self.artist = artist
        self.image = image
        self.lastPos = lastPos
        self.rank = rank
        self.isNew = isNew

    def __repr__(self):
        return "{}.{}(title={!r}, artist={!r})".format(
            self.__class__.__module__, self.__class__.__name__, self.title, self.artist
        )

    def __str__(self):
        """Returns a string of the form 'TITLE by ARTIST'."""
        if self.title:
            s = u"'%s' by %s" % (self.title, self.artist)
        else:
            s = u"%s" % self.artist

        if sys.version_info.major < 3:
            return s.encode(getattr(sys.stdout, "encoding", "") or "utf8")
        else:
            return s

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)


class ChartData:
    """Represents a particular Bugs chart by a particular period.
    Attributes:
        name: The chart name.
        date: The chart date.
        imageSize: The size of cover image for the track. (default: 256)
        fetch: A boolean value that indicates whether to retrieve the chart data immediately. If set to `False`, you can fetch the data later using the `fetchEntries()` method.
    """

    def __init__(self, imageSize: int = 256, fetch: bool = True):
        self.imageSize = imageSize
        self.entries = []

        if fetch:
            self.fetchEntries()

    def __getitem__(self, key):
        return self.entries[key]

    def __len__(self):
        return len(self.entries)

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def fetchEntries(self):
        headers = {
            "User-Agent": _USER_AGENT,
            "x-gm-app-name": _APP_NAME,
            "x-gm-app-version": _APP_VERSION
        }

        res = requests.get(
            _CHART_API_URL,
            headers=headers,
        )

        if res.status_code != 200:
            message = f"Request is invalid. response status code={res.status_code}"
            raise FloChartRequestException(message)

        data = res.json()

        self._parseEntries(data)

    def _parseEntries(self, data):
        try:
            self.name = data['data']['name']
            self.date = self._getDate()
            for index, item in enumerate(data['data']['trackList']):
                entry = ChartEntry(
                    title=item['name'],
                    artist=item['representationArtist']['name'],
                    image=self._getResizedImage(item['album']['imgList'][0]['url']),
                    rank=index + 1,
                    lastPos=int(item['rank']['rankBadge']) + index + 1,
                    isNew=item['rank']['newYn'] == "Y"
                )
                self.entries.append(entry)
        except Exception as e:
            raise FloChartParseException(e)

    def _getDate(self):
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, 22, 0, 0)
        if now.hour < 22:
            target_time -= timedelta(days=1)
        return target_time

    def _getResizedImage(self, url):
        return re.sub(r"/dims/resize/(\d+)x(\d+)", f"/dims/resize/{self.imageSize}x{self.imageSize}", url)