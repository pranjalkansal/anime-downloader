# anime-downloader

Anime batch downloader for [anime.nowtvshow.com]. Supports downloading with varying qualities and can download episode ranges.


### Features :
1. Search animes.
3. Download using terminal.


### Installation

1. `git clone https://github.com/pranjalkansal/anime-downloader.git`
2. `cd anime-downloader`
3. `python setup.py install`


### Usage :

1. `python downloader.py` from the `anime-downloader` directory.
2. Follow the onscreen instructions. See below for available options -

```
Usage: downloader.py (search | -s) <keyword>
       downloader.py (download | -l) <link>
       downloader.py (interactive)

Options:
    -h --help          Show this help message and exit
    -s, --search       Search anime using keyword.
    -l, --link         Download anime using link.

Arguments:
    keyword           Anime keyword/name to search
    link              Link to anime page on anime.nowtvshow.com
```

#### Dependencies :
1. Requests
2. BeautifulSoup4
3. LXML

Run `pip install -r requirements` for installing dependencies.

## License

MIT © Pranjal Kansal

