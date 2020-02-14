import setuptools
import re

# Version info:
VERSIONFILE="ape2/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="Sentera Multiband Splitting Tool",
    version=verstr,
    description="Script, with bundled executable, to split 5-band multi-spectral .TIF files from the Sentera 6X into "
                "individual single band .TIFs.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/SenteraLLC/py-multiband-tif-splitter",
)