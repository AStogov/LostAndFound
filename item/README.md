  ## <a name = "item">item相关接口</a>

* [x] <a href='#create'>create</a>   
* [x] <a href='#list'>list</a>   
* [x] <a href='#delete'>delete</a>   
* [x] <a href='#update'>update</a>   
* [x] [recover][#recover]     

请注意！：物品在服务端的唯一标识为id。删除、恢复和更新都需要提供id来进行操作。

错误返回值和含义：

| code | 含义                   |
| ---- | ---------------------- |
| -1   | 提供的参数非法         |
| -2   | 其他错误，详见具体输出 |

### 数据模型

| 变量名    | 类型        | 变量含义                                 |
| --------- | ----------- | :--------------------------------------- |
| id        | int         | 模型内自动生成的自增索引，物品的唯一标识 |
| openid    | string      | 发布者的openid                           |
| type      | int         | 物品属性（1是丢失的，2是找到的）         |
| title     | string      | 用户头像(url)，一般是微信头像            |
| desc      | string      | 物品描述                                 |
| images    | json_string | 物品图片                                 |
| visible   | int         | 是否可见。（用来完成删除和重新发布操作） |
| ctime     | string      | 数据创建时间（所有model共有的特性）      |
| mtime     | string      | 数据修改时间（所有model共有的特性）      |
| user_info | json        | 发布者的个人用户信息                     |

### <a name='create'>create</a> 创建动态   

url = www.example.com/service/item/create   
method = post   
params:   


| 名称   |        类型 | 必须 |                             备注                             |
| :----- | ----------: | :--: | :----------------------------------------------------------: |
| openid |         int |  是  |                  用户标识，用来指明是谁发的                  |
| type   |         int |  是  |                1:丢失了(lost) 2:找到了(found)                |
| desc   |      string |  是  |                           物品描述                           |
| title  |      string |  否  |                物品名称（保留字段，可只传""）                |
| images | json_string |  否  | 建议先调用接口上传图片(upload/itemImg)，成功填此接口；或者先创建，再上传图片，再更新此字段（不建议） |

**返回该物品的信息。物品信息格式化输出时中包含了发布者的信息**

return:

```json
{
    "code": 0,
    "msg": "success",
    "data": [{
                "id": 1,
                "openid": "1321321231",
                "ctime": "2020-03-26 14:55:20",
                "mtime": "2020-03-26 14:55:28",
                "type": 1,
                "title": "",
                "desc": "丢失",
                "images": [],
                "user_info": {
                    "openid": "xxxxxxxx",
        			"ctime": "2020-03-26 11:34:29",
        			"mtime": "2020-03-26 11:34:35",
        			"nick_name": "张三",
        			"avatar": "http://www.example/media/avatar/1_20200401184953.jpg",
			        "gender": "1",
        			"phone": "12312312312"
                }
            }]
}
```

### <a name='list'>list</a> 查询动态列表   

url = www.example.com/service/item/list   
method = post   
params:   

按照传递的不同参数可实现不同功能。如果是广场则传type=1是列出丢失的物品，type=2是列出找到的物品。

添加page和size的原因是控制一次呈现的物品数量，一面一次性返回过多数据。前端可以用“下一页”之类功能来使size+1来达到翻页效果


| 名称    |   类型 | 必须 |                             备注                             |
| :------ | -----: | :--: | :----------------------------------------------------------: |
| id      |    int |  否  |                        以物品id来查询                        |
| openid  |    int |  否  |         以openid来查询（用来查看用户发布的所有消息）         |
| type    |    int |  否  |                 以类型来查询，1丢失的2找到的                 |
| desc    | string |  否  |                           物品描述                           |
| page    |    int |  否  | 显示第几页，如果无参数则默认显示第0页（防止一下载入太多数据） |
| size    |    int |  否  |              每页几个物品，如果无参数则默认10个              |
| title   | string |  否  |                物品名称（保留字段，可只传""）                |
| visible |    int |  否  | 显示可见的或已隐藏的动态。默认值为1，即只显示可见的（未被delete操作的）动态。传0时可用来显示用户删除的动态。 |

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
                "openid": "1321321231",
                "ctime": "2020-03-26 14:55:20",
                "mtime": "2020-03-26 14:55:28",
                "type": 1,
                "title": "",
                "desc": "丢失",
                "images": [],
                "user_info": {
                    "openid": "xxxxxxxx",
        			"ctime": "2020-03-26 11:34:29",
        			"mtime": "2020-03-26 11:34:35",
        			"nick_name": "张三",
        			"avatar": "http://www.example/media/avatar/1_20200401184953.jpg",
			        "gender": "1",
        			"phone": "12312312312"
                }
            },
            {
                "id": 2,
                "openid": "1321321231",
                "ctime": "2020-03-26 16:53:28",
                "mtime": "2020-03-26 16:53:28",
                "type": 1,
                "title": "",
                "desc": "丢失",
                "images": [],
                "user_info": {
                    "openid": "xxxxxxxx",
        			"ctime": "2020-03-26 11:34:29",
        			"mtime": "2020-03-26 11:34:35",
        			"nick_name": "张三",
        			"avatar": "http://www.example/media/avatar/1_20200401184953.jpg",
			        "gender": "1",
        			"phone": "12312312312"
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


| 名称   |        类型 | 必须 |                             备注                             |
| :----- | ----------: | :--: | :----------------------------------------------------------: |
| id     |         int |  是  |                           物品的id                           |
| openid |         int |  是  |                                                              |
| type   |         int |  否  |                                                              |
| images | json_string |  否  | 建议先调用接口上传图片(upload/itemImg)，成功填此接口；或者先创建，再上传图片，再更新此字段（不建议） |
| title  |      string |  否  |                物品名称（保留字段，可只传""）                |
| desc   |      string |  否  |                           物品描述                           |

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


### 