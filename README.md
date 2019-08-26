# pyNMIC

搞一搞[国家气象信息中心（National Meteorological Information Center）](https://data.cma.cn/)

## 主要文件结构
```
├── FY4A
│   ├── fy4a.py    处理FY4A的AGRI一级数据hdf文件的类
│   ├── demo.py    演示
│   └── gui_tkinter.py    应用fy4a.py的一个简单GUI界面
├── SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10
│   └── reader.py    读取该产品二进制数据为numpy数组
……
└── data    对应的示例数据以及辅助数据
```
详细介绍见各目录下的`README.md`

## 调用示例
见各源文件末尾`if __name__ == "__main__":`中的内容

## 开发环境
```
anaconda
python                    3.7.4
```
### 第三方库
```
netcdf4                   1.4.2
numpy                     1.16.4
matplotlib                3.1.0
cartopy                   0.17.0
```



<center>

![](./data/weixin_qr.png)</center>