from datetime import datetime, timezone
from setuptools import setup

version_time = datetime.now(timezone.utc)

setup(
    version=f'{version_time.year}.{version_time.month}.{version_time.day}.{version_time.hour:02d}{version_time.minute:02d}{version_time.second:02d}',
)