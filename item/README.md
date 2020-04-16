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
| type        | string      |               物品属性（1是丢失的，2是找到的）               |
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

### <a name='create'>create</a> 创建动态   

url = www.example.com/service/item/create   
method = post   
params:   

| 变量名  | 类型        | 必须 | 变量含义                                                     |
| ------- | :---------- | :--: | :----------------------------------------------------------- |
| openid  | string      |  是  | 发布者的openid                                               |
| status  | int         |  是  | 1寻找失主；2寻找此物品                                       |
| type    | string      |  否  | 物品属性（1是丢失的，2是找到的）                             |
| area    | int         |  否  | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升），默认为0 |
| address | string      |  否  | 具体地点，可以为空                                           |
| time    | string      |  否  | 丢失或捡到的时间，可以为空                                   |
| goods   | string      |  否  | 物品名称                                                     |
| descr   | string      |  否  | 物品描述，可以为空                                           |
| img     | json_string |  否  | 物品图片，可以为空                                           |
| visible | int         |  否  | 是否可见。（用来完成删除和重新发布操作）（默认为1，即为可见） |

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
method = post   
params:   

按照传递的不同参数可实现不同功能。如果是广场则传type=1是列出丢失的物品，type=2是列出找到的物品。

添加page和size的原因是控制一次呈现的物品数量，一面一次性返回过多数据。前端可以用“下一页”之类功能来使size+1来达到翻页效果

| 变量名  | 类型        | 必须 | 变量含义                                                     |
| ------- | :---------- | :--: | :----------------------------------------------------------- |
| openid  | string      |  否  | 以发布者查询                                                 |
| status  | int         |  否  | 1寻找失主；2寻找此物品                                       |
| type    | string      |  否  | 物品属性（1是丢失的，2是找到的）                             |
| area    | int         |  否  | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升） |
| address | string      |  否  | 具体地点                                                     |
| time    | string      |  否  | 丢失或捡到的时间                                             |
| goods   | string      |  否  | 物品名称                                                     |
| descr   | string      |  否  | 物品描述                                                     |
| img     | json_string |  否  | 物品图片                                                     |
| visible | int         |  否  | 显示可见的或已隐藏的动态。默认值为1，即只显示可见的（未被delete操作的）动态。传0时可用来显示用户删除的动态。 |

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
| type    | string      |  否  | 物品属性（1是丢失的，2是找到的）                             |
| area    | int         |  否  | 校区（自行定义校区对应序号，例如： 0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升） |
| address | string      |  否  | 具体地点                                                     |
| time    | string      |  否  | 丢失或捡到的时间                                             |
| goods   | string      |  否  | 物品名称                                                     |
| descr   | string      |  否  | 物品描述                                                     |
| img     | json_string |  否  | 物品图片                                                     |
| visible | int         |  否  | 是否可见。（用来完成删除和重新发布操作）（默认为1，即为可见） |

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


