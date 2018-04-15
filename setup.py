from setuptools import setup

setup(
    name='anime-downloader',
    version="1.0",
    description='Anime Downloader - To batch download anime',
    long_description='Anime batch downloader. Can download any anime by searching or pasting link from anime.nowtvshow.com',
    license='MIT',
    author='Programer',
    url='https://github.com/pranjalkansal/anime-downloader',
    scripts=['downloader.py'],
    entry_points={
        'console_scripts': [
        ]
    },
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ]
)
