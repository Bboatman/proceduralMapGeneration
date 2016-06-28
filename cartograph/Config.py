import ConfigParser

class Config:
    def __init__(self):
        self.FILE_NAME_WIKIBRAIN_VECS = "./data/labdata/vecs.tsv"
        self.FILE_NAME_WIKIBRAIN_NAMES = "./data/labdata/names.tsv"
        self.FILE_NAME_NUMBERED_VECS = "./data/labdata/numberedVecs.tsv"
        self.FILE_NAME_NUMBERED_NAMES = "./data/labdata/numberedNames.tsv"
        self.FILE_NAME_ARTICLE_COORDINATES = "./data/labdata/tsne_cache.tsv"
        self.FILE_NAME_WATER_AND_ARTICLES = "./data/tsv/water_and_article_coordinates.tsv"
        self.FILE_NAME_WATER_CLUSTERS = "./data/tsv/clusters_with_water_pts.tsv"
        self.FILE_NAME_NUMBERED_CLUSTERS = "./data/tsv/numberedClusters.tsv"
        self.FILE_NAME_KEEP = "./data/tsv/keep.tsv"
        self.FILE_NAME_POPULARITY = "./data/labdata/article_popularity.tsv"
        self.FILE_NAME_NUMBERED_POPULARITY = "./data/tsv/popularity_with_id.tsv"
        self.FILE_NAME_SCALE_DENOMINATORS = "./data/labdata/scale_denominators.tsv"

        self.NUM_CLUSTERS = 10  # number of clusters to generate from K-means
        self.TSNE_THETA = 0.5  # lower values = more accurate maps, but take (much) longer
        self.TSNE_PCA_DIMENSIONS = None  # None indicates not to use PCA first
        self.PERCENTAGE_WATER = 0.1

        # ========== BorderFactory ==========
        self.MIN_NUM_IN_CLUSTER = 30  # eliminates noise
        self.BLUR_RADIUS = 5  # defines size of neighborhood for blurring

        # ========== mapGenerator ==========
        self._localTiles = "./data/tiles/"
        self._serverTiles = "/var/www/html/tiles/"
        self.DIRECTORY_NAME_TILES = self._localTiles
        self.FILE_NAME_REGION_NAMES = "./data/labdata/top_categories.tsv"
        self.FILE_NAME_IMGNAME = "./data/images/world"
        self.FILE_NAME_IMGDOT = "./data/labdata/blackDot.png"
        self.FILE_NAME_COUNTRIES = "./data/geojson/countries.geojson"
        self.FILE_NAME_CONTOUR_DATA = "./data/geojson/contourData.geojson"
        self.FILE_NAME_MAP = "map.xml"
        self.FILE_NAME_REGION_CLUSTERS = "./data/tsv/region_clusters.tsv"
        self.FILE_NAME_REGION_BORDERS = "./data/tsv/region_borders.tsv"
        self.FILE_NAME_TOP_TITLES = "./data/geojson/top_100_articles.geojson"
        self.FILE_NAME_LINK_TITLES = "./data/labdata/simple_links.txt"

        # ========== road information ==========
        self.FILE_NAME_LINKS = "./data/tsv/links.txt"
        self.FILE_NAME_EDGES = "./data/tsv/edges.txt"
        self.FILE_NAME_EDGE_BUNDLES = "./data/tsv/bundle_edges.txt"
        self.FILE_NAME_NODE_BUNDLES = "./data/tsv/bundle_nodes.txt"


__config = Config()


def BAD_GET_CONFIG():
    """
        TODO: Remove all calls to this,
        replace with intiailization from a config file.
    """
    return __config
