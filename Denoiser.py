from pygsp import graphs, filters
import numpy as np


class Denoiser:

    def __init__(self, x, y, clusters):
        self.x = x
        self.y = y
        self.clusters = clusters
        self.num_clusters = len(set(self.clusters))

    def _make_filter(self, tau=10):
        graph = graphs.NNGraph(zip(self.x, self.y), k=self.num_clusters)
        graph.estimate_lmax()
        fn = filters.Heat(graph, tau=tau)  # higher tau, spikier signal, less points
        return fn

    def _filter_in(self):
        n = len(self.x)
        filter_ = self._make_filter()
        signal = np.empty(self.num_clusters * n).reshape(self.num_clusters, n)
        vectors = np.zeros(n * self.num_clusters).reshape(n, self.num_clusters)
        for i, vec in enumerate(vectors):
            vec[self.clusters[i]] = 1
        vectors = vectors.T
        for cluster_num, vec in enumerate(vectors):
            signal[cluster_num] = filter_.analysis(vec)
        return signal

    def denoise(self):
        signal = self._filter_in()
        max_idx_arr = np.argmax(signal, axis=0)
        x_out = []
        y_out = []
        clusters_out = []
        for i in range(len(self.x)):
            if max_idx_arr[i] == self.clusters[i]:
                x_out.append(self.x[i])
                y_out.append(self.y[i])
                clusters_out.append(self.clusters[i])
        return x_out, y_out, clusters_out
