# -*- coding: utf-8 -*-
"""
Created on Mon September 23 09:40:53 2026

@author: Ganesh Gajjala
"""
# REFACTORING AND CLASS BASED STRUCTURE IN PROGRESS

import cv2 as cv
from dlisio import dlis
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
from skimage.measure import regionprops_table
from skimage.morphology import area_opening, area_closing, label
from sklearn.cluster import HDBSCAN


class BoreholePorosityClassifier:

    def __init__(
        self,
        file_path,
        bit_range_min=225,
        bit_range_max=255,
        min_cluster_size=25,
    ):
        """Initializes the pipeline with file paths and configuration parameters."""
        self.file_path = file_path
        self.bit_range_min = bit_range_min
        self.bit_range_max = bit_range_max
        self.min_cluster_size = min_cluster_size

        # Data placeholders
        self.depth = None
        self.vertical_resolution = None
        self.depth_size_rounded = 0
        self.im_stat = None
        self.im_dyn = None

        # Processed image placeholders
        self.im_stat_intp = None
        self.im_dyn_intp = None
        self.im_sum = None
        self.im_closed = None
        self.im_opened = None
        self.im_opened_bn = None
        self.im_opened_labels = None
        self.cluster_image = None
        self.cluster_cmap = None

        # Dataframe results
        self.pore_df = None

    def load_and_prepare_data(self):
        """Loads DLIS data, handles depth padding, and initializes empty image matrices."""
        print(f"Loading DLIS file: {self.file_path}...")
        f, *tails = dlis.load(self.file_path)
        image = f.frames[0]

        print("Extracting depth curves and calculating resolution...")
        raw_depth = image.curves()["DEPTH"]
        self.depth_size_rounded = round(len(raw_depth), -3)
        padding_length = self.depth_size_rounded - len(raw_depth)

        # Pad depth vector to a round figure
        last_segment_min = min(raw_depth[-int(str(len(raw_depth))[-3:]) :])
        extended_depth = np.full((padding_length,), last_segment_min, dtype=float)
        self.depth = np.concatenate((raw_depth, extended_depth), axis=0)
        self.vertical_resolution = self.depth[1] - self.depth[0]

        print("Extracting static and dynamic image logs...")
        raw_stat = image.curves()["BHI_STAT"]
        raw_dyn = image.curves()["BHI_DYN"]

        extended_img = np.full(
            (self.depth_size_rounded - len(raw_stat), raw_stat.shape[1]),
            -999,
            dtype=int,
        )
        self.im_stat = np.concatenate((raw_stat, extended_img))
        self.im_dyn = np.concatenate((raw_dyn, extended_img))

        # Initialize global arrays for slice operations
        self.im_stat_intp = np.empty_like(self.im_stat, dtype="uint8")
        self.im_dyn_intp = np.empty_like(self.im_stat, dtype="uint8")
        self.im_sum = np.empty_like(self.im_stat, dtype="uint8")
        self.im_closed = np.empty_like(self.im_stat, dtype="uint8")
        self.im_opened = np.empty_like(self.im_stat, dtype="uint8")

    def process_image_slices(self):
        """Processes the log arrays in optimized memory-efficient chunk blocks."""
        print("Interpolating sensor gaps and performing morphology operations...")

        # Binary mask creation where sensors lack coverage (-999)
        sensor_mask = (self.im_stat == -999).astype("uint8")
        im_stat_uint8 = self.im_stat.astype("uint8")
        im_dyn_uint8 = self.im_dyn.astype("uint8")

        for i in range(0, self.depth_size_rounded, 1000):
            row_from, row_to = i, i + 999

            # Slice current chunk
            stat_slice = im_stat_uint8[row_from:row_to, :]
            dyn_slice = im_dyn_uint8[row_from:row_to, :]
            mask_slice = sensor_mask[row_from:row_to, :]

            # Inpaint gaps using OpenCV Telea
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL

            self.im_stat_intp[row_from:row_to, :] = stat_intp_slice
            self.im_dyn_intp[row_from:row_to, :] = dyn_intp_slice

            # Blending and dynamic threshold filtering
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL

            # Mathematical morphology to extract clean pore candidates
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL

            self.im_closed[row_from:row_to, :] = closed_slice
            self.im_opened[row_from:row_to, :] = opened_slice

        # Compute global binary image thresholding matrix
        _, self.im_opened_bn = cv.threshold(self.im_opened, 0, 1, cv.THRESH_BINARY)

    def extract_features_and_cluster(self):
        """Identifies physical regions and runs fully vectorized HDBSCAN classification."""
        print("Labeling structural components and geomorphic geometries...")
        self.im_opened_labels, num_labels = label(
            self.im_opened_bn, return_num=True, connectivity=2
        )
        print(f"Total isolated regions identified: {num_labels}")

            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
        )
        pore_prpty = regionprops_table(self.im_opened_labels, properties=properties)

        # Feature Engine Construction

            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
        )
        

        # Subset properties for spatial/geometric clustering

            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL

        print("Executing density-based classification (HDBSCAN)...")
        hdb = HDBSCAN(copy=True, min_cluster_size=self.min_cluster_size)
        hdb_labels = hdb.fit_predict(self.pore_df)
        cluster_labels = hdb_labels + 2  # Normalize cluster tags to positive indices
        self.pore_df["cluster"] = cluster_labels

        print("Performing highly optimized array lookup vectorization...")
        region_labels = np.unique(self.im_opened_labels)[1:]  # Exclude background (0)
        label_to_cluster = dict(zip(region_labels, cluster_labels))

        # Vectorized lookup map injection (replaces slow element loops entirely)
        lookup_table = np.zeros(self.im_opened_labels.max() + 1, dtype=np.int32)
        for r_label, c_label in label_to_cluster.items():
            lookup_table[r_label] = c_label

        self.cluster_image = lookup_table[self.im_opened_labels]


            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL
            # CONFIDENTIAL

    def generate_and_save_plots(self):
        """Builds high-resolution QC panels and writes them safely to disk."""
        print("Rendering depth-interval visualization plots...")
        colored_image = self.cluster_cmap(self.cluster_image)

        for i in range(0, self.depth_size_rounded, 1000):
            row_from, row_to = i, i + 999
            depth_slice = self.depth[row_from:row_to]
            depth_min, depth_max = (
                round(depth_slice.min(), 2),
                round(depth_slice.max(), 2),
            )

            fig, ax = plt.subplots(
                ncols=9, figsize=(26, 11.5), sharex=True, sharey=True
            )

            # Map tracking layout
            ax[0].imshow(self.im_stat[row_from:row_to, :].astype("uint8"), cmap="YlOrBr")
            ax[0].set_title("BHI Static", fontsize=13)

            ax[1].imshow(self.im_dyn[row_from:row_to, :].astype("uint8"), cmap="YlOrBr")
            ax[1].set_title("BHI Dynamic", fontsize=13)

            ax[2].imshow(self.im_stat_intp[row_from:row_to, :], cmap="YlOrBr")
            ax[2].set_title("BHI Static\nInterpolated", fontsize=13)

            ax[3].imshow(self.im_dyn_intp[row_from:row_to, :], cmap="YlOrBr")
            ax[3].set_title("BHI Dynamic\nInterpolated", fontsize=13)

            ax[4].imshow(self.im_sum[row_from:row_to, :], cmap="YlOrBr")
            ax[4].set_title("Merged\nStatic*0.5 + Dynamic*0.5", fontsize=13)

            ax[5].imshow(self.im_closed[row_from:row_to, :], cmap="YlOrBr")
            ax[5].set_title("Area Closing\n(skimage)", fontsize=13)

            ax[6].imshow(self.im_opened[row_from:row_to, :], cmap="YlOrBr")
            ax[6].set_title("Area Opening\n(skimage)", fontsize=13)

            ax[7].imshow(self.im_opened_bn[row_from:row_to, :], cmap="binary")
            ax[7].set_title("Binary Mask\n(Pore Slices)", fontsize=13)

            ax[8].imshow(colored_image[row_from:row_to, :])
            ax[8].set_title("HDBSCAN Results\n(Pore Clusters)", fontsize=13)

            title = (
                f"{self.file_path.split('/')[-1]} Index [{depth_min}m to {depth_max}m]\n"
                f"Drill segment processing section length: {round(depth_max - depth_min, 2)}m"
            )
            plt.suptitle(title, fontsize=18, y=0.98)

            for a in ax:
                a.set_axis_off()

            fig.tight_layout(w_pad=2)
            fig.savefig(f"img-{i}.png", format="png", dpi=180)
            plt.close(fig)  # Explicitly closes memory handles to prevent crashes

    def run_pipeline(self):
        """Orchestrator to launch the entire petrophysical sequence sequentially."""
        self.load_and_prepare_data()
        self.process_image_slices()
        self.extract_features_and_cluster()
        self.generate_and_save_plots()
        print("Pipeline sequence executed completely successfully!")


# --- Execution Entry Point ---
if __name__ == "__main__":
    # To run this, simply replace 'my_file_path.dlis' with your path
    pipeline = BoreholePorosityClassifier(file_path="my_file_path.dlis")
    pipeline.run_pipeline()
