# pyNMIC

搞一搞[国家气象信息中心（National Meteorological Information Center）](https://data.cma.cn/)

## 主要文件结构
```
├── FY4A
│   ├── fy4a.py    处理FY4A的AGRI一级数据hdf文件的类
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
anaconda                  5.3.1
python                    3.7.2
```
### 第三方库
```
h5py                      2.9.0
numpy                     1.16.2
matplotlib                3.0.2
astropy                   3.1.2
```



<center>

![](./data/weixin_qr.png)</center>