# MDtools

## 1 Extract_images

问题：

本地的markdown文档中的图片在云端图床，不能一次性全部自动下载到本地备份，只能手动一个一个下载，不方便管理

使用方法：

1. 首先在当前文件夹下新建`old`和`new`文件夹；
2. 将自己需要提取图片的 `md` 文件或者文件夹放在 ` old ` 文件夹下；
3. 然后运行 `Extract_images.py` 文件，运行完后所有的文件都在 `new` 文件夹中。

效果：

1. 该脚本会将`old`中的所有文件复制到`new`文件夹中，`old`文件夹内容不做修改，`new`文件夹中的内容中的图片链接变为本地图片的相对路径；
2. 会根据 markdown 文档中的`http`或者`https`图片链接，将图片下载到与该 `md` 文件路径同级目录的 `asset` 文件夹中。

使用前提：需要对应的图床能够支持 `空 Referer`，同时能够支持批量下载，无额外限制

## 2 transWikiToMD

问题：obdisian文档中的链接如果是 wiki 链接样式，可以通过该代码将其转换为markdown形式

使用方法：

* 将当前`old`文件夹下的所有`md`文件拷贝到新建的`new`文件夹；
* 将自己需要提取图片的 `md` 文件或者文件夹放在 ` old ` 文件夹下；
* 然后运行 `transWikiToMD.py` 文件，运行完后所有的文件都在 `new` 文件夹中。

将`new`文件夹中的图片引用方式更改一下，

* 将 `![[attachments/aaaa.png]] `改为 `![](attachments/aaaa.png)`;
* 将 所有的`attachments`文件夹名称改为 `assets`文件夹
* 将 `![](attachments/aaaa.png) ` 更改为` ![](assets/aaaa.png) `

其中`aaaa.png`为图片，其它格式文件也可以