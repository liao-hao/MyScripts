## [ExportGUI.py](ExportGUI.py) 是一个用于导出数据库表结构和数据的图形工具

### 使用方法
1. 创建环境
```shell
conda create -n mysql_export_env python=3.11
conda activate mysql_export_env
pip install -r requirements.txt
```
2. 安装依赖
```shell
pip install -r requirements.txt
```

3. 运行 `ExportGUI.py`
```shell
python ExportGUI.py
```

4. 打包
```shell
pyinstaller --onefile --noconsole  ExportGUI.py
```



## [MysqlExport.py](MysqlExport.py) 是一个用于导出数据库表结构和数据的命令行工具

