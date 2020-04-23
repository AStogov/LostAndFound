# 失物招领小程序后端
[TOC]   

## 1.服务介绍   

* [x] 用户服务[user](#user)   
* [x] 物品服务[item](#item)    
* [x] 上传服务[upload](#upload)

##  2.部署流程

### 2.1 安装依赖

```shell
pip install -r requirements.txt
apt install nginx uwsgi mysql-server
```

### 2.2 选择数据库

#### 2.2.1 MySQL 数据库: 

在LostAndFound/settings.py文件中<u>**注释掉**</u>

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

在LostAndFound/settings.py文件中<u>**取消以下内容的注释**</u>

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lostandfound',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

在LostAndFound/settings.py 文件夹中填写数据库的地址、用户名和密码。



设置mysql utf-8编码   

>输入下面的命令，打开第一个配置文件
>```
>vim /etc/mysql/conf.d/mysql.cnf
>```
>在 [mysql] 标签的下一行添加下面的配置
>```
>default-character-set=utf8
>```
>输入下面的命令，打开第二个配置文件
>```
>vim /etc/mysql/mysql.conf.d/mysqld.cnf
>```
>找到 [mysqld] 标签，在其下一行添加下面的配置
>```
>character-set-server=utf8
>```
>配置文件修改成功之后，输入下面的命令重启mysql服务
>```
>service mysql restart
>```
>重启之后再去查看数据库的默认编码方式
>```
>show variables like '%character%';
>```
>
>```
>mysql> show variables like '%character%';
>+--------------------------+----------------------------+
>| Variable_name            | Value                      |
>+--------------------------+----------------------------+
>| character_set_client     | utf8                       |
>| character_set_connection | utf8                       |
>| character_set_database   | utf8                       |
>| character_set_filesystem | binary                     |
>| character_set_results    | utf8                       |
>| character_set_server     | utf8                       |
>| character_set_system     | utf8                       |
>| character_sets_dir       | /usr/share/mysql/charsets/ |
>+--------------------------+----------------------------+
>```
创建数据库并设置数据库编码

```mysql
CREATE DATABASE lostandfound DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

#### 2.2.2 SQLite数据库

**默认选择的是这种数据库，不需要更改**

在LostAndFound/settings.py文件中<u>**注释掉**</u>

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lostandfound',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

在LostAndFound/settings.py文件中<u>**取消以下内容的注释**</u>

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### 2.3 设置默认路径

在LostAndFound/settings.py文件中，设置媒体文件media/的位置、静态文件static/的位置

### 2.4 运行服务

将models的改动同步到数据库   

```shell script
python manage.py makemigrations user
python manage.py makemigrations item
python manage.py migrate
```
运行调试(仅调试，上线请勿用此方法)
```shell script
python manage.py runserver
```

## 3.上线流程

需要Nginx，uwsgi支持

### MySQL

创建数据库并设置数据库编码
```mysql
CREATE DATABASE lostandfound DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

在LostAndFound/settings.py 文件夹中填写数据库的用户名和密码。

### SQLite





### 同步数据库接口

```shell script
python manage.py makemigrations user
python manage.py makemigrations item
python manage.py migrate
```
#### 上线：

在LostAndFound/settings.py 文件夹中填写DOMAIN为服务器地址

```shell script
python manage.py collectstatic
```

#### 关于django admin   
创建超级用户

```shell script
python manage.py createsuperuser
```
访问DOMAIN/admin来管理内容



## <a name = "user">user相关接口文档</a>

* [x] <a href='#login'>login</a>   
* [x] <a href='#getOpenid'>getOpenid</a>   
* [x] <a href='#loginByOpenid'>loginByOpenid</a>   
* [x] <a href='#get'>get</a>   
* [x] <a href='#update'>update</a>    

用户交互流程  

**注：用户的openid是所有操作的必须项**

### 数据模型

| 变量名  | 类型   | 变量含义                                  |
| ------- | ------ | :---------------------------------------- |
| id      | int    | 数据模型内部自增索引。前端无需操作。      |
| openid  | string | 前端获取的用户唯一标识                    |
| name    | string | 用户姓名                                  |
| phone   | string | 用户手机号                                |
| cardno    | string | 用户的学号                            |
| wxid | string | 用户微信号                           |
| created_at   | string | 数据创建时间（所有model共有的特性）       |
| modified_at   | string | 数据修改时间（所有model共有的特性）       |

### Token鉴权

[Token账户鉴权系统][https://gogs.itoken.team/634308664/token-sso/src/master]

请前端同学先调用token账户鉴权系统，鉴权成功后再以流程验证登录。

**鉴权成功后，鉴权返回的手机号、姓名、学号可以直接作为login的参数进行注册。**


```mermaid
graph LR
    H(Token鉴权) --> A[获取openid]
    A --> B(loginByOpenid)
    B --> C{数据库存在此openid}
    C -->|是| D(缓存用户信息)
    C -->|否| E[调用login注册]
    E -->D
```

数据库是否存在openid这一过程是依靠返回值判断的。

所有正确操作的返回值都是0

### <a name='login'>login</a> 用户登录（无状态注册）

**如果没有数据库内用户的openid，则用login进行注册**

url = www.example.com/service/user/login   
method = post   
params:   

| 名称    |  类型  | 必须 |                       备注                        |
| ------- | :----: | :--: | :-----------------------------------------------: |
| openid  | string |  是  | 可通过云函数或getOpenid获取，是每个用户的唯一凭证 |
| phone   | string |  是  |                      手机号                       |
| name    | string |  是  |                     用户姓名                      |
| cardno    | string |  是  |                  用户的学号                   |
| wxid | string |  否  |      （可选）用户的其他联系方式，如QQ/微信等      |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "id": 1,
        "openid": "xxxxxxxx",
        "phone": "12345678912",
        "name": "张三",
        "cardno": "0111111111111",
        "wxid": "weixin_id123",
        "created_at": "2020-03-26 11:34:29",
        "modified_at": "2020-03-26 11:34:35"
    }
}
```

错误码：

| code |           含义           |
| ---- | :----------------------: |
| -1   |      提交的参数非法      |
| -2   | 其他错误，详情见错误输出 |

### <a name='getOpenid'>getOpenid</a> 获取用户openid   

url = www.example.com/service/user/getOpenid   
method = post   
params:   

*不建议使用*

| 名称    |  类型  | 必须 | 备注 |
| :------ | :----: | :--: | :--: |
| js_code | string |  是  |      |

**建议使用云函数：   **
https://developers.weixin.qq.com/miniprogram/dev/wxcloud/guide/functions/userinfo.html

### <a name='loginByOpenid'>loginByOpenid</a> 通过openid登陆，获取个人信息  

url = www.example.com/service/user/loginByOpenid   
method = post   
params:   

| 名称   |   类型 | 必须 | 备注 |
| :----- | -----: | :--: | :--: |
| openid | string |  是  |      |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "id": 1,
        "openid": "xxxxxxxx",
        "phone": "12345678912",
        "name": "张三",
        "cardno": "0111111111111",
        "wxid": "weixin_id123",
        "created_at": "2020-03-26 11:34:29",
        "modified_at": "2020-03-26 11:34:35"
    }
}
```

错误码：

| code |                含义                 |
| ---- | :---------------------------------: |
| -1   |           提交的参数非法            |
| -2   | 不存在此用户，此时应该调用login方法 |


### <a name='get'>get</a> 获取用户详情   

url = www.example.com/service/user/get   
method = post   
params:   

| 名称   | 类型 | 必须 | 备注 |
| :----- | :--: | :--: | :--: |
| openid | int  |  是  |      |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "id": 1,
        "openid": "xxxxxxxx",
        "phone": "12345678912",
        "name": "张三",
        "cardno": "0111111111111",
        "wxid": "weixin_id123",
        "created_at": "2020-03-26 11:34:29",
        "modified_at": "2020-03-26 11:34:35"
    }
}
```

错误码：

| code |                    含义                    |
| ---- | :----------------------------------------: |
| -1   |               提交的参数非法               |
| -2   | 返回了多组数据（一个openid对应了多个用户） |
| -3   |          其他错误，详情见错误输出          |
| -4   |                 用户不存在                 |



### <a name='update'>update</a> 更新用户信息   

url = www.example.com/service/user/update   
method = post   
params:   

| 名称    |     类型     | 必须 |                            备注                             |
| :------ | :----------: | :--: | :---------------------------------------------------------: |
| user_id |     int      |  是  |                                                             |
| update  | json(string) |  是  | 如果提交的是字符串格式的json程序会loads，但最好提交json格式 |

e.g.:   
update={"phone":"13333333333"}   

return:   

```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```

错误码：

| code |                含义                |
| ---- | :--------------------------------: |
| -1   |           提交的参数非法           |
| -2   |      其他错误，详情见错误输出      |
| -3   | update参数提交的不是有效的json格式 |
| -4   |            json处理错误            |



  ## <a name = "item">item相关接口</a>

* [x] <a href='#create'>create</a>   
* [x] <a href='#list'>list</a>   
* [x] <a href='#delete'>delete</a>   
* [x] <a href='#update'>update</a>   
* [x] <a href='#recover'>recover</a>   

请注意！：物品在服务端的唯一标识为id。删除、恢复和更新都需要提供id来进行操作。

错误返回值和含义：

| code | 含义                   |
| ---- | ---------------------- |
| -1   | 提供的参数非法         |
| -2   | 其他错误，详见具体输出 |

### 数据模型

| 变量名      | 类型        |                           变量含义                           |
| ----------- | ----------- | :----------------------------------------------------------: |
| id          | int         |           模型内自动生成的自增索引，物品的唯一标识           |
| openid      | string      |                        发布者的openid                        |
| status      | int         |                    1寻找失主；2寻找此物品                    |
| type        | string      |                           物品类型                           |
| area        | int         | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升） |
| address     | string      |                           具体地点                           |
| time        | string      |                       丢失或捡到的时间                       |
| goods       | string      |                           物品名称                           |
| descr       | string      |                           物品描述                           |
| img         | json_string |                           物品图片                           |
| visible     | int         |     是否可见。（用来完成删除和重新发布操作）1可见0不可见     |
| created_at  | string      |             数据创建时间（所有model共有的特性）              |
| modified_at | string      |             数据修改时间（所有model共有的特性）              |
| user_info   | json        |                     发布者的个人用户信息                     |
| name        | string      |                       发布者留下的姓名                       |
| phone       | string      |                       发布者留下的电话                       |
| wxid        | string      |                      发布者留下的微信号                      |

### <a name='create'>create</a> 创建动态   

url = www.example.com/service/item/create   
method = post   
params:   

| 变量名  | 类型        | 必须 | 变量含义                                                     |
| ------- | :---------- | :--: | :----------------------------------------------------------- |
| openid  | string      |  是  | 发布者的openid                                               |
| status  | int         |  是  | 1寻找失主；2寻找此物品                                       |
| type    | string      |  否  | 物品类型                                                     |
| area    | int         |  否  | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升），默认为0 |
| address | string      |  否  | 具体地点，可以为空                                           |
| time    | string      |  否  | 丢失或捡到的时间，可以为空                                   |
| goods   | string      |  否  | 物品名称                                                     |
| descr   | string      |  否  | 物品描述，可以为空                                           |
| img     | json_string |  否  | 物品图片，可以为空                                           |
| visible | int         |  否  | 是否可见。（用来完成删除和重新发布操作）（默认为1，即为可见） |
| name    | string      |  否  | 发布者留下的姓名                                             |
| phone   | string      |  否  | 发布者留下的电话                                             |
| wxid    | string      |  否  | 发布者留下的微信号                                           |

**返回该物品的信息。物品信息格式化输出时中包含了发布者的信息**

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": [{
                "id": 1,
                "openid": "xxxxxxxx",
        		"goods": "XXX的校园卡",
        		"type": "校园卡",
        		"status": 1,
        		"area": 1,
                "img": [],
        		"time": "2020-03-25 14:55:20",
        		"address": "东院教四601",
                "descr": "在教室里丢失了一张校园卡",
                "created_at": "2020-03-26 14:55:20",
                "modified_at": "2020-03-26 14:55:28",
        		"visible": 1,
        		"name": "李四",
        		"phone": "12345678901",
        		"wxid": "wxid_123",
                "user_info": {
                    "id": 1,
        			"openid": "xxxxxxxx",
        			"phone": "12345678912",
        			"name": "张三",
        			"cardno": "012121212121",
        			"wxid": "weixin_id123",
        			"created_at": "2020-03-26 11:34:29",
        			"modified_at": "2020-03-26 11:34:35"
                }
            }]
}
```

### <a name='list'>list</a> 查询动态列表   

url = www.example.com/service/item/list   
method = post   s
params:   

按照传递的不同参数可实现不同功能。如果是广场则传status=1是列出寻找失主，status=2是列出寻找此物品。

添加page和size的原因是控制一次呈现的物品数量，以免一次性返回过多数据。前端可以用“下一页”之类功能来使page+1来达到翻页效果

| 变量名  | 类型        | 必须 | 变量含义                                                     |
| ------- | :---------- | :--: | :----------------------------------------------------------- |
| openid  | string      |  否  | 以发布者查询                                                 |
| status  | int         |  否  | 1寻找失主；2寻找此物品                                       |
| type    | string      |  否  | 物品类型                                                     |
| area    | int         |  否  | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升） |
| address | string      |  否  | 具体地点                                                     |
| time    | string      |  否  | 丢失或捡到的时间                                             |
| goods   | string      |  否  | 物品名称                                                     |
| descr   | string      |  否  | 物品描述                                                     |
| page    | int         |  否  | 呈现第几页（默认是0，为了控制一次返回的物品数量以免爆页）    |
| size    | int         |  否  | 每页物品数量（默认是10，为了控制一次返回的物品数量以免爆页） |
| img     | json_string |  否  | 物品图片                                                     |
| visible | int         |  否  | 显示可见的或已隐藏的动态。默认值为1，即只显示可见的（未被delete操作的）动态。传0时可用来显示用户删除的动态。 |
| name    | string      |  否  |                                                              |
| phone   | string      |  否  |                                                              |
| wxid    | string      |  否  |                                                              |

**列表返回的物品都是以id降序排序的，也就是指按发布时间降序排序，越新越靠前**

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "cnt": 2,
        "items": [
            {
                "id": 1,
                "openid": "xxxxxxxx",
        		"goods": "XXX的校园卡",
        		"type": "校园卡",
        		"status": 1,
        		"area": 1,
                "img": [],
        		"time": "2020-03-25 14:55:20",
        		"address": "东院教四601",
                "descr": "在教室里丢失了一张校园卡",
                "created_at": "2020-03-26 14:55:20",
                "modified_at": "2020-03-26 14:55:28",
        		"visible": 1,
        		"name": "李四",
        		"phone": "12345678901",
        		"wxid": "wxid_123",
                "user_info": {
                    "id": 1,
        			"openid": "xxxxxxxx",
        			"phone": "12345678912",
        			"name": "张三",
        			"cardno": "012121212121",
        			"wxid": "weixin_id123",
        			"created_at": "2020-03-26 11:34:29",
        			"modified_at": "2020-03-26 11:34:35"
                }
            },
            {
                "id": 2,
                "openid": "xxxxxxxx",
        		"goods": "XXX的校园卡",
        		"type": "校园卡",
        		"status": 2,
        		"area": 3,
                "img": [],
        		"time": "2020-03-25 14:55:20",
        		"address": "南湖新食堂",
                "descr": "在越苑食堂里捡到了一张校园卡",
                "created_at": "2020-03-26 14:55:20",
                "modified_at": "2020-03-26 14:55:28",
        		"visible": 1,
                "user_info": {
                    "id": 1,
        			"openid": "xxxxxxxx",
        			"phone": "12345678912",
        			"name": "张三",
        			"cardno": "012121212121",
        			"wxid": "weixin_id123",
        			"created_at": "2020-03-26 11:34:29",
        			"modified_at": "2020-03-26 11:34:35"
                }
            }
        ]
    }
}
```


### <a name='delete'>delete</a> 删除动态   

url = www.example.com/service/item/delete
method = post   
params:   


| 名称   | 类型 | 必须 |                  备注                  |
| :----- | ---: | :--: | :------------------------------------: |
| id     |  int |  是  |                 动态id                 |
| openid |  int |  是  | 用户openid，用户只能删除自己发布的信息 |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```


### <a name='apply'>update</a> 更新动态   

url = www.example.com/service/item/update   
method = post   
params:   

| 变量名  | 类型        | 必须 | 变量含义                                                     |
| ------- | :---------- | :--: | :----------------------------------------------------------- |
| id      | int         |  是  | 物品id                                                       |
| openid  | string      |  是  | 发布者的openid                                               |
| status  | int         |  否  | 1寻找失主；2寻找此物品                                       |
| type    | string      |  否  | 物品类型                                                     |
| area    | int         |  否  | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升） |
| address | string      |  否  | 具体地点                                                     |
| time    | string      |  否  | 丢失或捡到的时间                                             |
| goods   | string      |  否  | 物品名称                                                     |
| descr   | string      |  否  | 物品描述                                                     |
| img     | json_string |  否  | 物品图片                                                     |
| visible | int         |  否  | 是否可见。（用来完成删除和重新发布操作）（默认为1，即为可见） |
| name    | string      |  否  |                                                              |
| phone   | string      |  否  |                                                              |
| wxid    | string      |  否  |                                                              |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```

### <a name='recover'>recover</a> 恢复动态   

**用于重新发布**

url = www.example.com/service/item/recover  
method = post   
params:   


| 名称   | 类型 | 必须 |                  备注                  |
| :----- | ---: | :--: | :------------------------------------: |
| id     |  int |  是  |                 动态id                 |
| openid |  int |  是  | 用户openid，用户只能恢复自己发布的信息 |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```






## <a name = "upload">upload相关接口</a>

* [x] <a href='#itemImg'>itemImg</a>  


### <a name='itemImg'>itemImg</a> 上传物品图片

**这个接口上传的是图片文件，用来在物品描述中上传图片用。**

url = www.example.com/service/upload/itemImg      
method = post   
params:   

| 名称   | 类型 | 必须 |                    备注                     |
| :----- | :--: | :--: | :-----------------------------------------: |
| img | file |  是  | 可传多个、要将input标签中的name设置为img |

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": ["https://www.example.com/media/item/2020/3/27/011216_59730.jpg", "https://www.example.com/media/item/2020/3/27/011216_89864.jpg"]
}
```

| code |             含义             |
| ---- | :--------------------------: |
| -1   | 提交的参数非法或文件不是图片 |
| -2   |   其他错误，详情见错误输出   |
