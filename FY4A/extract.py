# -*- coding: utf-8 -*-
"""
从FY-4A标称数据提取指定范围指定通道
Created on 2018/11/14 12:46:47
@author: modabao
"""

from h5py import File as h5File
import numpy as np
from numpy import arange, rint
from matplotlib import pyplot as plt
from projection import latlon2lc


# 各分辨率文件包含的通道号
CHANNELNUMS = {"0500M": ('02',),
               "1000M": tuple([f"{x:02d}" for x in range(1, 4)]),
               "2000M": tuple([f"{x:02d}" for x in range(1, 8)]),
               "4000M": tuple([f"{x:02d}" for x in range(1, 15)])}
# 各分辨率行列数
SIZES = {"0500M": 21984,
         "1000M": 10992,
         "2000M": 5496,
         "4000M": 2748}


def get_channelnums(resolution, channelnums):
    """
    判断要提取的通道名（两位数字字符串序列）
    """
    if channelnums:
        # 若有指定通道则只提取指定通道
        return channelnums
    else:
        # 若无指定通道则提取全部
        return CHANNELNUMS[resolution]


def extract(h5name, l=None, c=None, channelnums=None, method='nearest'):
    """
    提取
    l：行号
    c：列号
    channelnums：提取的通道名（两位数字字符串序列）
    返回字典
    暂时没有处理缺测值（异常）
    REGC超出范围未解决
    """
    channelnums = get_channelnums(h5name, channelnums)  # 获得目标通道号
    channels = {}
    if l is None and c is None:
        with h5File(h5name, 'r') as h5file:
            for channelnum in channelnums:
                NOMChannelname = "NOMChannel" + channelnum
                CALChannelname = "CALChannel" + channelnum
                channel = h5file[NOMChannelname].value[:]
                channels["Channel" + channelnum] = channel
        return channels
    if method == 'nearest':
        l = rint(l).astype(np.uint16)
        c = rint(c).astype(np.uint16)
    with h5File(h5name, 'r') as h5file:
        l_begin = h5file.attrs["Begin Line Number"]
        l_end = h5file.attrs["End Line Number"]
        for channelnum in channelnums:
            NOMChannelname = "NOMChannel" + channelnum
            CALChannelname = "CALChannel" + channelnum
            # DISK全圆盘数据和REGC中国区域数据区别在起始行号和终止行号
            channel = (h5file[NOMChannelname].value[l - l_begin, c] if l_begin
                       else h5file[NOMChannelname].value[l, c])
            CALChannel = h5file[CALChannelname].value  # 定标表
            channels["Channel" + channelnum] = CALChannel[channel]  # 缺测值！？
    return channels


# 演示导出指定范围数据到一个.nc文件
if __name__ == "__main__":
    from os import listdir
    from os.path import join
    from datetime import datetime
    from netCDF4 import Dataset as ncDataset
    h5path = r"F:\FY-4A"  # FY-4A一级数据所在路径
    ncname = r"F:\FY-4A\nc\test.nc"
    h5list = [join(h5path, x) for x in listdir(h5path)
              if "4000M" in x and "FDI" in x]
    step = 50  # 0.050°
    lat = np.arange(40000, 20000-1, -step) / 1000  # 40~20°N
    lon = np.arange(110000, 130000+1, step) / 1000  # 110~130°E
    channelnums = ("02", "04", "05", "06", "12", "14")
    ncfile = ncDataset(ncname, 'w', format="NETCDF4")
    ncfile.createDimension("lat", len(lat))
    ncfile.createDimension("lon", len(lon))
    ncfile.createDimension("time")  # 不限长
    nclat = ncfile.createVariable("lat", "f4", ("lat",))
    nclon = ncfile.createVariable("lon", "f4", ("lon",))
    nctime = ncfile.createVariable("time", "f8", ("time",))
    nctime.units = "minutes since 0001-01-01 00:00:00.0"
    t = 0
    for channelnum in channelnums:
        channelname = "Channel" + channelnum
        ncfile.createVariable(channelname, "f4", ("time", "lat", "lon"))
    ncfile.set_auto_mask(False)
    nclat[:] = lat
    nclon[:] = lon
    lon, lat = np.meshgrid(lon, lat)
    l, c = latlon2lc(lat, lon, "4000M")  # 求标称全圆盘行列号
    for h5name in h5list:
        channels = extract(h5name, l, c, channelnums=channelnums)
        time = datetime.strptime(h5name[-45: -33], "%Y%m%d%H%M%S")
        plt.figure(h5name[-45: -31])
        plt.imshow(channels["Channel12"], cmap="gray")
        for channelnum in channelnums:
            channelname = "Channel" + channelnum
            ncfile[channelname][t, :, :] = channels[channelname]
            nctime[t] = nc.date2num(time, nctime.units)
        t += 1
        ncfile.sync()
    ncfile.close()
