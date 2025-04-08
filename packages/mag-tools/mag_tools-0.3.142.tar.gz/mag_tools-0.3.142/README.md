# 基本库 Mag_Tools

## 安装依赖库
  ```
- 安装 twine
  ```Bash
    which python
    which python3
    open /Applications/Python\ 3.x/Install\ Certificates.command
    pip install twine
  ```
  其中 3.x为python版本号

## 发布库

- 创建虚拟环境
    ```Bash
      python -m venv .venv
    ```
- 激活虚拟环境
    ```Bash
      .venv\Scripts\activate
    ```
- 安装依赖项
    ```Bash
      pip install -r requirements.txt
    ```
- 编辑打包
    ```Bash
      python setup.py sdist bdist_wheel
    ```
- 本地安装库
    ```Bash
       pip install dist/mag_tools-0.1.x-py3-none-any.whl 
    ```
- 上传包
  ```Bash
    twine upload dist/*
  ```

## 配置 API Token

- 获取API Token
- 配置.pypirc 文件： 在用户主目录下创建 .pypirc 文件，并添加以下内容(请用真实的token替代)
  ```Plaintext
  [distutils]
  index-servers =
      pypi

  [pypi]
  username = __token__
  password = pypi-AgENdGVzdC5weXBpLm9yZwIkZjM2YzQ2Y2QtY2Y2OS00YjY3LWE4YzUtY2Y2OTY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3Yj
  ```

## 配置USB支持库
- 下载libusb:
  从 libusb 官方网站 下载适用于 Windows 的 libusb 库
- 解压文件到本地目录
- 配置环境变量：
  确保路径指向包含 libusb-1.0.dll 文件的目录
- 安装 PyUSB
  ```Bash
    pip install pyusb
  ```
