from distutils.core import setup

try:
  from subprocess import Popen, PIPE
except ImportError:
  from popen2 import popen2

NAME = "satellite_sanity"
VERSION = "REPLACE_ME_WITH_VERSION"
SHORT_DESC = "Red Hat Satellite health check"
LONG_DESC = "Red Hat Satellite health check tool"

setup (
    name = NAME,
    version = VERSION,
    author = "Jan Hutar",
    author_email = "jhutar@redhat.com",
    maintainer = "Jan Hutar",
    maintainer_email = "jhutar@redhat.com",
    url = "https://github.com/SatelliteQE/satellite-sanity",
    license = "GPLv3",
    packages = ["satellite_sanity", "satellite_sanity/checks", "satellite_sanity/rules"],
    package_data={
        'satellite_sanity': ['config.ini'],
    },
    description = SHORT_DESC,
    long_description = LONG_DESC
)
