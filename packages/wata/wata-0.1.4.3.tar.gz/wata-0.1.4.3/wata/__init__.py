from wata.image.img import ImageProcess
from wata.pointcloud.pcd import PointCloudProcess
from wata.file.file import FileProcess
from wata.mathematics.mathematics import Maths
from wata.display.display import Display
from wata.geo.geo import GeoProcess
import os


def __version__():
    return "0.1.2.19"

def obtain_wata_path():
    return os.path.dirname(os.path.abspath(__file__))

def obtain_cur_path_cmd():
    return "os.path.dirname(os.path.abspath(__file__))"


def check_version(library, version):
    import pkg_resources
    installed_version = pkg_resources.get_distribution(library).version
    if pkg_resources.parse_version(installed_version) > pkg_resources.parse_version(version):
        return True
    else:
        return False
