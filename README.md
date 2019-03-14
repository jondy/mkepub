# 延安红云编辑辅助工具使用说明

延安红云编辑辅助工具用于处理各种素材，主要包括

* 转换文本 .txt 为 .epub 文件
* 分割大的 pdf 文件为 10M 的小文件

## 安装

下载安装包

    http://www.yancloud.red/downloads/yanhong-editor.exe

双击运行安装包，安装好之后会有桌面快捷方式 `延安红云编辑工具` ，双击即
可打开工具。

## 转换 EPUB

本工具只能对特定的文本格式进行转换。

### 文本格式

封面必须和文本文件在同一个目录下面，且名称增加后缀 `-封面.jpg`

文本的作者等信息应该在前 100 行之内，支持的关键字包括:

    书名：
    作者： 多个作者使用空格分开
    出版者：
    出版时间：
    ISBN：

文本的基本格式为使用 `#` 来标识一个章节的开始。

第一个包含 `#` 的行如果不是在第一行，其前的所有行会被忽略，不会写入到
输出文件中。

注释行以 `!#` 开始，这样的行也会被忽略。

### 使用方法

批量转换一个目录下的所有文本文件：

* 点击 `选择目录` , 然后选择需要转换的目录，目录下面的所有文本文件会出
  现在列表中
* 点击 `开始转换` ，开始依次转换文件，转换完成之后状态变为 `转换完成`
* 全部转换完成之后，会提示是否查看输出的结果文件，点击 `确定` 会打开一
  个 Excel 文件`upload-epub.xlsx` ，这个文件可以用来上传 EPUB 文件到红
  云网。

生成的 EPUB 文件默认保存在当前目录下面的 `output` 下面，使用 FTP 可以
批量上传所有的文件到红云网。

转换多个文件：

* 点击 `选择文件` , 然后选择需要转换的文件，可以多选，选中的文本文件会
  出现在列表中
* 点击 `开始转换`，后面的步骤和批量转换相同。

## 分割 PDF

点击工具栏按钮 `分割 PDF` ,选择一个PDF文件，会分割成为 10M 大小的多个
PDF 文件，存放在和原文件相同的目录下面。
