# -*- coding: utf-8 -*-
import noise
import numpy as np
# import matplotlib.pyplot as plt
import cv2


def generate_input(shape):
    scale = .2
    octaves = 4
    persistence = 0.5
    lacunarity = 2.0
    seed = np.random.randint(0, 100)

    world = np.zeros(shape)

    # make coordinate grid on [0,1]^2
    x_idx = np.linspace(0, 1, shape[0])
    y_idx = np.linspace(0, 1, shape[1])
    world_x, world_y = np.meshgrid(x_idx, y_idx)

    # apply perlin noise, instead of np.vectorize, consider using itertools.starmap()
    world = np.vectorize(noise.pnoise2)(world_x / scale,
                                        world_y / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=1024,
                                        repeaty=1024,
                                        base=seed)

    img = np.floor((world + .5) * 255).astype(np.uint8)  # <- Normalize world first
    img_bin = img > 150
    # print(np.max(img_bin))
    # plt.imshow(img)
    # plt.show()

    # keep only five largest connected components
    nbcc, labels, stats, _ = cv2.connectedComponentsWithStats(img_bin.astype(np.uint8), connectivity=8)

    idxes = np.argsort(stats[:, cv2.CC_STAT_AREA])[::-1]
    if 0 in idxes:
        idxes = np.delete(idxes, np.argmax(idxes == 0))
    bin_mask = np.zeros_like(img_bin)
    bin_mask_split = np.zeros_like(img_bin)
    bin_mask_labels = np.zeros_like(img_bin).astype(np.uint8)
    bin_mask_nbcc = min(nbcc - 1, 5)
    for i in range(bin_mask_nbcc):
        # print("cc nb", i + 1)
        cc_mask = labels == idxes[i]
        bin_mask[cc_mask] = 1
        bin_mask_labels[cc_mask] = i + 1
        # print(np.max(bin_mask_labels))
        nb_split_cc = np.random.randint(1, 6)  # one CC is split into up to 5 CCs
        # print("nb_split", nb_split_cc)
        thresholds = np.zeros(nb_split_cc + 1)
        thresholds[0] = 150
        for j in range(151, 256, 1):  # ok this is brute force, not smart, but this is still fast enough
            nbcc_cc, _ = cv2.connectedComponents(((img > j) * cc_mask).astype(np.uint8))
            # print(thresholds, nbcc_cc, j)
            if nbcc_cc == nb_split_cc + 1:
                thresholds[nb_split_cc] = j
                bin_mask_split += (img > j) * cc_mask
                # print("found threshold", j)
                break
            elif 1 <= nbcc_cc < nb_split_cc + 1 and thresholds[nbcc_cc - 1] == 0:
                thresholds[nbcc_cc - 1] = j
        if thresholds[nb_split_cc] == 0:
            # print("not found threshold", thresholds, np.argmax(np.nonzero(thresholds)[0]))
            bin_mask_split += (img > thresholds[np.argmax(np.nonzero(thresholds)[0])]) * cc_mask
    return bin_mask, bin_mask_labels, bin_mask_split
