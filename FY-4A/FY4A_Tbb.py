# -*- coding: utf-8 -*-
"""
用FY4A的10.8μm通道计算Tbb
先对一级数据最邻近插值
再定标
Created on 2018/11/07 16:59:07
@author: modabao
"""

import h5py
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt


def h5(h5path):
    """
    从4km一级数据hdf中读取10.8um通道数据和定标表
    暂时没有定标
    """
    with h5py.File(h5path, 'r') as h5file:
        NOMChannel12 = h5file["NOMChannel12"][:]  # 10.8um通道4KM图像数据层
        CALChannel12 = h5file["CALChannel12"][:]  # 10.80um通道的定标表
    return NOMChannel12, CALChannel12


def get_mask_grid(gridpath):
    """
    读取4km经纬度查找表
    .gz文件需要事先解压
    """
    samples = 2748
    lines = 2748
    latlon = np.fromfile(gridpath, "<d")  # 大端？？？实际上是小端
    latlon.resize([lines, samples, 2])  # 经，纬？？？实际上是纬，经
    latlon[latlon == 999999.9999] = np.nan
    return latlon


def interp(NOMChannel12, latlon, lat, lon):
    """
    最邻近插值法插值到目标区域
    lat降序
    lon升序
    """
    lines, samples = NOMChannel12.shape
    # 插值目标地区
    lat = np.sort(lat)[::-1]  # lat降序
    lon = np.sort(lon)  # lon升序
    interplon = np.empty((lines, len(lon)), dtype=np.uint16)  # 先对经度插值
    templat = np.empty_like(interplon, dtype=np.float64)  # 对纬度矩阵的经度插值
    for r, row in enumerate(NOMChannel12):  # 每一行对经度插值
        interpf = interp1d(latlon[r, :, 1], row, kind="nearest")
        interplon[r] = interpf(lon)
        interpf = interp1d(latlon[r, :, 1], latlon[r, :, 0], kind="nearest")
        templat[r] = interpf(lon)
    NOMChannel12 = np.empty((len(lat), len(lon)), dtype=np.uint16)
    for c, column in enumerate(interplon.T):  # 每一列对纬度插值
        interpf = interp1d(templat[:, c], column, kind="nearest")
        NOMChannel12[:, c] = interpf(lat)
    return NOMChannel12


if __name__ == "__main__":
    import os
    h5path = r"F:\FY-4A"  # FY-4A一级数据所在路径
    gridpath = r"E:\FY-4A\FullMask_Grid_4000.raw"  # 4km经纬度查找表绝对路径
    h5list = [os.path.join(h5path, x) for x in os.listdir(h5path)
              if "4000M" in x and "FDI" in x]
    lat = np.arange(40, 20-0.05, -0.05)  # 目标纬度范围
    lon = np.arange(110, 130+0.05, 0.05)  # 目标经度范围
    latlon = get_mask_grid(gridpath)
    for h5path in h5list:
        NOMChannel12, CALChannel12 = h5(h5path)
        NOMChannel12 = interp(NOMChannel12, latlon, lat, lon)
        tbb = CALChannel12[NOMChannel12]  # 定标
        np.save(h5path[-45: -31] + "_Tbb", tbb)
        plt.figure(h5path[-45: -31])
        plt.imshow(tbb, cmap="gray")
