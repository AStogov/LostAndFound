  ## item相关接口   
* [x] <a href='#categories'>0categories</a>   
* [x] <a href='#create'>create</a>   
* [x] <a href='#list'>list</a>   
* [x] <a href='#delete'>delete</a>   
* [x] <a href='#update'>update</a>   
* [x] <a href='#apply'>apply</a>   
* [x] <a href='#confirm'>confirm</a>    
* [x] <a href='#reject'>reject</a>    
* [x] <a href='#ocrPrintedText'>ocrPrintedText</a>    
* [x] <a href='#search'>search</a>    

## 接口文档      
请注意！：用户在服务端的唯一标识为openid   

错误返回值和含义：

| code | 含义                   |
| ---- | ---------------------- |
| -1   | 提供的参数非法         |
| -2   | 其他错误，详见具体输出 |



### <a name='create'>create</a> 创建动态   
url = www.example.com/service/item/create   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|openid | int | 是 | 用户标识，用来指明是谁发的 |
|type | int | 是 | 1:丢失了(lost) 2:找到了(found) |
|desc | string | 是 | 物品描述 |
|title | string | 否 | 物品名称（保留字段，可只传""） |
| images | json_string |  否  | 建议先调用接口上传图片(upload/itemImg)，成功填此接口；或者先创建，再上传图片，再更新此字段（不建议） |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```

### <a name='list'>list</a> 查询动态列表   
url = www.example.com/service/item/list   
method = post   
params:   

按照传递的不同参数可实现不同功能。如果是广场则传type=1是列出丢失的物品，type=2是列出找到的物品。

添加page和size的原因是控制一次呈现的物品数量，一面一次性返回过多数据。前端可以用“下一页”之类功能来使size+1来达到翻页效果


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | 否 | 以物品id来查询 |
|openid | int | 否 | 以openid来查询（用来查看用户发布的所有消息） |
|type | int | 否 | 以类型来查询，1丢失的2找到的 |
| desc   | string |  否  |                           物品描述                           |
| page   |    int |  否  | 显示第几页，如果无参数则默认显示第0页（防止一下载入太多数据） |
| size   |    int |  否  |              每页几个物品，如果无参数则默认10个              |
| title  | string |  否  |                物品名称（保留字段，可只传""）                |

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
                "openid": "1321321231"
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
                "openid": "1321321231"
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
url = {domain}/service/item/delete   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | 是 | 动态id|
|openid | int | 是 | 用户openid，用户只能删除自己发布的信息 |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```


### <a name='apply'>update</a> 更新动态   
url = {domain}/service/item/update   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | 是 | 物品的id |
|openid | int | 是 |  |
|type | int | 否 |  |
| images | json_string |  否  | 建议先调用接口上传图片(upload/itemImg)，成功填此接口；或者先创建，再上传图片，再更新此字段（不建议） |
|title | string | 否 | 物品名称（保留字段，可只传""） |
|desc | string | 否 |  物品描述|

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```
