ccob
=======

简介
------

用于快速搭建 `Obsidian` 项目的 `Cookiecutter <https://www.cookiecutter.io/>`_ 模板.

**主要特性:**

- 支持 ``Python >= 3.8`` 环境
- 支持 ``uv`` 构建项目
- 支持 ``sphinx`` 文档构建工具
- 支持 ``alabaster`` / ``sphinx_rtd_theme`` / ``classic`` 等多种文档风格
- 支持 ``Typer`` / ``Argparse`` 命令行项目

快速开始
----------

安装 ``ccob``: ::

    $ pip install ccob  # 通过 pip
    $ uv tool install ccob  # 通过 uv

使用 ``ccob`` 创建 `Python` 项目模板: ::

    $ ccob  # 直接使用
    $ uvx ccob  # 通过 uv

也可使用以下方式: ::

    $ uvx cookiecutter https://gitee.com/gooker_young/ccob.git


离线模式运行
--------------

下载本项目源代码 ``zip`` 文件: ::

    $ wget https://gitee.com/gooker_young/ccob/repository/archive/develop.zip

解压到文件夹:

- windows: ``C:\Users\xxx\.cookiecutters\ccob``
- linux: ``/home/xxx/.cookiecutters/ccob``

运行命令: ::

    $ ccob --offline
