import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import shapefile as sf
import wget
import os
import tarfile


def DownloadData():
    """ Downloads the shapefiles """
    shape_dir = "./shape_files"
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

    for f in files_list:
        if not os.path.exists(os.path.join(tar_dir, f)):
            url = base_url + f
            print "Downloading {}".format(url)
            wget.download(url, out=tar_dir)

        print "\nUnpacking.."
        tar = tarfile.open(os.path.join(tar_dir, f))
        tar.extractall(path=shape_dir)
        tar.close()


class GBBasemap(object):
    def __init__(self, ax=None, threshold=None):
        if ax is None:
            ax = plt.subplot(111, aspect="equal")
        self.shape_dir = "shape_files"
        self.ax = ax
        self.clipped = True

        if threshold is None:
            if self.clipped:
                self.threshold = 50
            else:
                self.threshold = 500
        else:
            self.threshold = threshold

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

    def add_shape_collection(self, shape_file_name, color=None, **kwargs):

        shape_file_path = os.path.join(self.shape_dir, shape_file_name)
        try:
            map_f = sf.Reader(shape_file_path)
        except sf.ShapefileException:
            raise ValueError(
                "The shape-file {} does not appear to exist".format(
                    shape_file_path) +
                "\nTry running $ python pycountrygb.py to download the files"
                )
        metadata = map_f.records()
        shapes = map_f.shapes()

        if color is None:
            colors = np.random.uniform(0, 1, (len(shapes), 3))
        elif type(color) == str:
            colors = color * len(shapes)

        for i, s in enumerate(shapes):
            islands = self.split_up_islands(s.points)
            for isle in islands:
                poly = mpl.patches.Polygon(isle, facecolor=colors[i],
                                           closed=True, **kwargs)
                self.ax.add_patch(poly)

    def draw_country(self, country, *args, **kwargs):
        if type(country) != list:
            country = [country]

        for c in country:
            shape_file = self.get_shape_file_name(c, "outline")
            self.add_shape_collection(shape_file, *args, **kwargs)

    def draw_counties_for_country(self, country, *args, **kwargs):
        if type(country) != list:
            country = [country]

        for c in country:
            shape_file = self.get_shape_file_name(c, "counties")
            self.add_shape_collection(shape_file, *args, **kwargs)

    def draw_by_file_name(self, file_name, *args, **kwargs):
        self.add_shape_collection(file_name, *args, **kwargs)

    def get_shape_file_name(self, country, spec):
        key = "_".join([country, spec])

        dictionary = {
            'england_outline': 'England_ol_2011_gen_clipped.shp',
            'england_counties': 'england_ct_2011_gen_clipped.shp',
            'wales_outline':  'Wales_ol_2011_gen_clipped.shp',
            'wales_counties':  'Wales_ct_1991_gen3_area.shp',
            'scotland_outline': 'Scotland_ol_1991_area.shp',
            'scotland_counties': 'Scotland_dt_1991_area.shp',
            'scotland_counties': 'Scotland_dt_1991_area.shp',
            'gb_counties': 'gb_dt_2009_10.shp',
            }

        try:
            shape_file = dictionary[key]
        except KeyError:
            raise ValueError(
                "Error: Something is wrong with country={}, spec={}".format(
                    country, spec))

        return shape_file

if __name__ == "__main__":
    DownloadData()
