# -*- coding: utf-8 -*-
import numpy as np
import cv2

def closest_point(point, array):
     diff = array - point
     distance = np.einsum('ij,ij->i', diff, diff)
     return np.argmin(distance), distance

def find_bridge_line(contour_1, contour_2, bin_mask_labels):
    min_dist = np.max(bin_mask_labels.shape)
    chosen_point_c2 = None
    chosen_point_c1 = None

    # iterate through each point in contour c1
    for point in contour_1:
        t = point[0][0], point[0][1]
        index, dist = closest_point(t, contour_2[:,0])
        if dist[index] < min_dist :
            min_dist = dist[index]
            chosen_point_c2 = contour_2[index]
            chosen_point_c1 = t     

    return chosen_point_c1, chosen_point_c2q

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
