# -*- coding: utf-8 -*-
import numpy as np
import cv2

def fix_mask(bin_mask, bin_mask_split, bin_mask_labels):
    for cluster in np.unique(bin_mask_labels)[1:]:
        bin_cluster = np.where(bin_mask_labels == cluster, 255, 0).astype(np.uint8)
        print(bin_mask_split.shape, bin_cluster.shape)

        bin_cluster = cv2.bitwise_and(bin_mask_split, bin_cluster)
        contours, _ = cv2.findContours(bin_cluster, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        print(len(contours))

        cv2.imshow("debug", bin_cluster.astype(np.uint8))
        cv2.waitKey(0)

    return bin_mask_split
