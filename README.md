# 🌊 FLO 차트 API: flo-chart.py
![flo](./image.png)

flo-chart.py is a Python API that retrieves the TOP 100 information from the [FLO](https://www.music-flo.com/).

## Installation
```commandline
pip install flo-chart.py
```

## Quickstart
The main usage of flo-chart.py is similar to [billboard.py](https://github.com/guoguo12/billboard-charts).
```commandline
>>> from flo import *
>>> chart = ChartData()
>>> print(chart[0].json())
{
    "artist": "IVE (아이브)",
    "image": "https://cdn.music-flo.com/image/v2/album/763/481/12/04/412481763_6420ff34_s.jpg?1679884086290/dims/resize/256x256/quality/90",
    "isNew": false,
    "lastPos": 1,
    "rank": 1,
    "title": "Kitsch"
}
>>> print(chart.name)
FLO 차트
>>> print(chart.date)
2023-04-09 22:00:00
```

### ChartData Arguments
- `name` – The chart name
- `date` – The chart date
- `imageSize` – The size of cover image for the track. (default: 256)
- `fetch` – A boolean value that indicates whether to retrieve the chart data immediately. If set to `False`, you can fetch the data later using the `fetchEntries()` method.

### Chart entry attributes
`ChartEntry` can be accessed using the `ChartData[index]` syntax. A `ChartEntry` instance has the following attributes:
- `title` – The title of the track
- `artist` – The name of the artist
- `image` – The URL of the cover image for the track
- `lastPos` - The track's last position on the previous period.
- `rank` – The track's current rank position on the chart.
- `isNew` – Whether the track is new to the chart.

### K-Pop music chart Python APIs
- [Melon | melon-chart.py](https://github.com/gold24park/melon-chart.py)
- [Bugs | bugs-chart.py](https://github.com/gold24park/bugs-chart.py)
- [Genie | genie-chart.py](https://github.com/gold24park/genie-chart.py)
- [Vibe | vibe-chart.py](https://github.com/gold24park/vibe-chart.py)
- [Flo | flo-chart.py](https://github.com/gold24park/flo-chart.py)

## Dependencies
- [requests](https://requests.readthedocs.io/en/latest/)

## License
This project is licensed under the MIT License.
