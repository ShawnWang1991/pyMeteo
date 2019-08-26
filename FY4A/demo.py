# -*- coding: utf-8 -*-
"""
fy4a等模块的使用方法

Created on 2019/8/25 20:31:55
@author: modabao
"""


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.io.shapereader as shpreader

from fy4a import FY4A_AGRI_L1


# %% 指定经纬度范围和间隔读取第12波段并绘图
# 读取
h5name = (r'..\data\FY4A\FY4A-_AGRI--_N_REGC_1047E_L1-_FDI-_MULT_NOM_'
          '20180726051500_20180726051916_4000M_V0001.HDF')
fy4a_agri_l1 = FY4A_AGRI_L1(h5name)
geo_range = '10, 54, 70, 140, 0.1'
fy4a_agri_l1.extract('Channel12', geo_range)
channel12 = fy4a_agri_l1.channels['Channel12']
# 绘图
PlateCarree = ccrs.PlateCarree()
plt.figure('Tbb云顶亮温（Channel12）')
ax = plt.axes(projection=PlateCarree)
shpname = r'..\data\map\China_province'
provinces_records = list(shpreader.Reader(shpname).records())
provinces_geometrys = [x.geometry for x in provinces_records]
ax.add_geometries(provinces_geometrys, PlateCarree,
                  edgecolor='black', facecolor='None')
lat_S, lat_N, lon_W, lon_E, step = eval(geo_range)
extent=[lon_W - 0.05, lon_E + 0.05, lat_S - 0.05, lat_N + 0.05]
ax.imshow(channel12, cmap='gray', transform=PlateCarree, origin='upper',
          extent=extent)
ax.set_xticks(list(range(lon_W, lon_E+1, 10)), PlateCarree)
ax.set_yticks(list(range(lat_S, lat_N+1, 10)), PlateCarree)
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
ax.coastlines()
# plt.show()
plt.savefig(r'..\data\FY4A\Tbb云顶亮温（Channel12）')

# %% 将上一步读取的数据写入geotiff
from tools import write_geotiff
write_geotiff(r'..\data\FY4A\Tbb云顶亮温（Channel12）.tif',
              channel12, lon_W, lat_N, step)



# # %%
# from skimage.measure import find_contours
# fy4a_agri_l1.extract('Channel12')
# channel12 = fy4a_agri_l1.channels['Channel12']
# begin = []
# end = []
# for l, line in enumerate(channel12):
#     for c, pixel in enumerate(line):
#         if pixel < 65534:
#             begin.append((l, c))
#             for c1, pixel1 in enumerate(line[c:]):
#                 if pixel1 >= 65534:
#                     end.append((l, c+c1-1))
#                     break
#             break
# southline = [(begin[-1][0], x) for x in range(begin[-1][1], end[-1][1]+1)]
# northline = [(begin[0][0], x) for x in range(begin[0][1], end[0][1]+1)]
# temp = begin + southline + end[::-1] + northline[::-1]
# temp = np.array(temp)
# l = temp[:, 0] + 183
# c = temp[:, 1]
# plt.figure('REGC大致范围')
# ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=100))
# ax.plot(lon, lat, 'b-', transform=PlateCarree)
# ax.add_geometries(provinces_geometrys, PlateCarree,
#                   edgecolor='black', facecolor='None')
# ax.set_xticks(list(range(20, 180+1, 20)), PlateCarree)
# ax.set_yticks(list(range(0, 70+1, 10)), PlateCarree)
# lon_formatter = LongitudeFormatter(zero_direction_label=True)
# lat_formatter = LatitudeFormatter()
# ax.xaxis.set_major_formatter(lon_formatter)
# ax.yaxis.set_major_formatter(lat_formatter)
# ax.coastlines()
# ax.set_xlim((-80, 90))
# # plt.show()
# plt.savefig(r'.\data\REGC大致范围_')

