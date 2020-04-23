## <a name = "upload">upload相关接口</a>


* [x] <a href='#itemImg'>itemImg</a>  


### <a name='itemImg'>itemImg</a> 上传物品头像

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