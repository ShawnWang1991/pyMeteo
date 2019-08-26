# coding: utf-8
"""


Created on 2019/8/22 18:00:23 
@author: modabao
"""


from osgeo import gdal, osr


def write_geotiff(tiff_path, data, upper_left_lon, upper_left_lat, step, AREA_OR_POINT='Point'):
    """
    写入geotiff。默认pixel is point，默认WGS84
    """
    rows, columns = data.shape
    bands = 1
    pixel_width = step
    pixel_height = -step
    half_step = step / 2
    upper_left_x = upper_left_lon - half_step
    upper_left_y = upper_left_lat + half_step
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(tiff_path, columns, rows, bands, gdal.GDT_Float32)
    dataset.SetMetadataItem('AREA_OR_POINT', AREA_OR_POINT)
    dataset.SetGeoTransform([upper_left_x, pixel_width, 0,
                             upper_left_y, 0, pixel_height])
    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    sr = osr.SpatialReference()
    sr.SetWellKnownGeogCS('WGS84')
    dataset.SetProjection(sr.ExportToWkt())  # 给新建图层赋予投影信息
    dataset.GetRasterBand(1).WriteArray(data)
    dataset.FlushCache()  # 将数据写入硬盘
    dataset = None
