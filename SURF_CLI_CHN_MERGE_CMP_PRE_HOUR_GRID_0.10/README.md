# [中国自动站与CMORPH融合的逐时降水量0.1°网格数据集（1.0版）](http://data.cma.cn/data/cdcdetail/dataCode/SEVP_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10.html)

`SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10`

`reader.py`中的`read()`即为用于读取该产品的函数。

---

根据提供的.ctl文件：
```
DSET ^SEVP_CLI_CHN_MERGE_FY2_PRE_HOUR_GRID_0.10-%y4%m2%d2%h2.grd
*
UNDEF -999.0
*
OPTIONS   little_endian  template
*
TITLE  China Hourly Merged Precipitation Analysis
*
xdef  700 linear  70.05  0.10
*
ydef  440 linear  15.05  0.10 
*
ZDEF     1 LEVELS 1  
*
TDEF 9999 LINEAR 00Z01Aug2010 1hr 
*
VARS 2                           
crain      1 00  CH01   combined analysis (mm/Hour)
gsamp      1 00  CH02   gauge numbers
ENDVARS
```

可直接获得信息：
- 存储方式是小端存储
- 空间范围为：70.05°E\~139.95°E，15.05°N\~58.95°N，间隔0.1°
- 有两个变量：降雨量`crain`和雨量计数量`gsamp`

可推测而得的信息：
- 结合文件的大小为2464000字节，可推测每个数据为`2464000/(700*440*2)`=4字节
- 结合示例图图例可知数据应该是浮点数（没有找到数据类型的描述）

需要注意的是：
- 经过尝试，数组存储顺序是右侧为先（C-like）
- 数据的存储顺序是自西向东、自南向北、自`crain`向`gsamp`，直接读取时矩阵为上南下北，为了方便绘图等操作已经按习惯调整为上北下南

出图如下：

![](../data/SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10/demo.png)

官网原图：
![](../data/SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10/surf_cli_chn_merge_cmp_pre_hour_grid_0.10SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10-2018081707.gif)