import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import shapefile as sf
import wget
import os
import tarfile


shape_dir = os.path.join(os.environ.get("HOME"), ".shape_files")


def DownloadData():
    """ Downloads the shapefiles """
    tar_dir = "./tars"
    for dir in [shape_dir, tar_dir]:
        if not os.path.exists(dir):
            os.makedirs(dir)

    base_url = "http://census.edina.ac.uk/ukborders/easy_download/prebuilt/shape/"
    files_list = ["England_ct_2011_gen_clipped.tar.gz",
                  "England_ol_2011_gen_clipped.tar.gz",
                  "Wales_ct_1991_gen3.tar.gz",
                  "Wales_ol_2011_gen_clipped.tar.gz",
                  "Scotland_dt_1991.tar.gz",
                  "Scotland_ol_1991.tar.gz",
                  "Gb_dt_2009_10.tar.gz",
                  "Gb_wpc_2010_05.tar.gz"
                  ]
    print("Downloading shape files...")
    for f in files_list:
        if not os.path.exists(os.path.join(tar_dir, f)):
            url = base_url + f
            print("Downloading {}".format(url))
            wget.download(url, out=tar_dir)
            print()

        print("Unpacking {}".format(f))
        tar = tarfile.open(os.path.join(tar_dir, f))
        tar.extractall(path=shape_dir)
        tar.close()

    print("Done, all shape-files stored in {}".format(shape_dir))


class GBBasemap(object):
    def __init__(self, ax=None, threshold=None):
        if ax is None:
            ax = plt.subplot(111, aspect="equal")
        self.shape_dir = shape_dir
        self.ax = ax
        self.clipped = True

        if threshold is None:
            if self.clipped:
                self.threshold = 50
            else:
                self.threshold = 500
        else:
            self.threshold = threshold

    # IO Tools to facilitate interaction with shape-files
    def get_shape_file_name(self, request, region):
        """ Interface to stores shape-files """
        key = "_".join([region, request])

        dictionary = {
            'england_country': 'England_ol_2011_gen_clipped.shp',
            'england_counties': 'england_ct_2011_gen_clipped.shp',
            'wales_country':  'Wales_ol_2011_gen_clipped.shp',
            'wales_counties':  'Wales_ct_1991_gen3_area.shp',
            'scotland_country': 'Scotland_ol_1991_area.shp',
            'scotland_counties': 'Scotland_dt_1991_area.shp',
            'gb_constituency': 'gb_dt_2009_10.shp',
            }

        try:
            shape_file = dictionary[key]
        except KeyError:
            raise ValueError(
                ("Error: It appears that we don't have request={} for "
                 "region={}").format(request, region))

        return shape_file

    def read_shape_file(self, shape_file_name):
        """ Takes the name of a shape-file and returns shapes and metadata """
        shape_file_path = os.path.join(self.shape_dir, shape_file_name)
        try:
            map_f = sf.Reader(shape_file_path)
        except sf.ShapefileException:
            raise ValueError(
                "The shape-file {} does not appear to exist".format(
                    shape_file_path) +
                "\nTry running $ python pymapgb.py to download the files"
                )
        metadata = map_f.records()
        shapes = map_f.shapes()

        return metadata, shapes

    # Plotting tools
    def plot_single_shape(self, shape, *args, **kwargs):
        islands = self.split_up_islands(shape.points)
        for isle in islands:
            poly = mpl.patches.Polygon(isle, closed=True, *args, **kwargs)
            self.ax.add_patch(poly)

    def draw_by_shape_file_name(self, shape_file_name, *args, **kwargs):

        metadata, shapes = self.read_shape_file(shape_file_name)
        nshapes = len(shapes)
        for i in range(nshapes):
            self.plot_single_shape(shapes[i], *args, **kwargs)

    def split_up_islands(self, points):
        """ Break a list of points up into individual islands """

        threshold = self.threshold
        diffs = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
        diffs_ave = np.mean(diffs)

        break_idxs = np.arange(len(diffs))[diffs > diffs_ave * threshold]
        break_idxs = np.concatenate(([0], break_idxs, [len(points)]))

        # Remove break_idxs that are next to each other
        #break_idxs = break_idxs[np.roll(break_idxs, -1) - break_idxs != 1]
        islands = [points[break_idxs[i]+1:break_idxs[i+1]-1]
                   for i in range(len(break_idxs)-1)]

        islands = [i for i in islands if len(i) > 10]

        return islands

    def draw_by_request(self, request, region, *args, **kwargs):
        """ Draw the map according to particular request and region

        Paramaters
        ----------
        request: str,
            One of ['country', 'county', 'constituency']
        region: str,
            One of ['england', 'wales', 'scotland', 'gb']

        """

        region = region.lower()
        request = request.lower()

        shape_file_name = self.get_shape_file_name(request, region)
        self.draw_by_shape_file_name(shape_file_name, *args, **kwargs)
