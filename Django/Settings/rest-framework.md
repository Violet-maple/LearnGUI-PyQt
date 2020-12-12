### rest_framework settings 统一设置：

```python
"""
设置返回结果响应统一格式 
{
  "code": 0, 
  "msg": "success", 
  "results": "XXX",
  "data": {
      "id": 1,
      ... ...
  }
}
"""
REST_FRAMEWORK = {
  	# 重写响应结果
    'DEFAULT_RENDERER_CLASSES':(
        'utils.ReturnRenderer.JSONRender',
    ),
  
  	# 定义分页
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
  
    # 配置过滤
    'DEFAULT_FILTER_BACKENDS': (
      	'rest_framework.filters.DjangoFilterBackend',
      	'rest_framework.filters.SearchFilter'
    ),

}
```

### 响应重写文件

```python
# coding: utf-8

from rest_framework.renderers import JSONRenderer


class JSONRender(JSONRenderer):

    # 重写响应
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 返回来的数据中包含了code和msg，可以通过pop拿出来
        if isinstance(data, dict):
            code = data.pop('code', 200)
            msg = data.pop('msg', 'success')
        else:
            code = 0
            msg = 'success'
        # 返回结果
        res = {
            'code': code,
            'msg': msg,
          	# 'results': 'XXX',
            'data': data
        }
        
        return super().render(res, accepted_media_type=None, renderer_context=None)
```

### rest_framework mixins, viewsets

```python
class ApiStudent(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet,):
    queryset = Student.objects.filter(delete=0)
    
    serializer_class = StudentSerializer
    
    # 过滤 filter_class = StudentFilter
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
        except Exception as e:
            data = {
                'code': 1001,
                'mag': str(e)
            }
        return Response(data)
    
    def perform_destroy(self, instance):
        instance.delete = True
        instance.save()
```

### rest_framework serializer

```python
class StudentSerializer(serializers.ModelSerializer):
    date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    
    class Meta:
        model = Student
        # fields = ("id", "name")
    	fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['g_name'] = str(instance.g)
        data['c_name'] = str(instance.c)
        data['sex'] = instance.get_sex_display()
        # choices (("male", "男"), ("female", "女"))
        # 1.get_sex_display() "男"
        # 2. shirt_size  --> "male"
        
        return data
    
    def update(self, instance, validated_data):
        instance.g_name = validated_data['g_name']
        instance.save()
        
        data = self.to_representation(instance)
        
        return data 
```

### rest_framework URL

```python
# 实例化一个router
router = SimpleRouter()
router.register('student', ApiStudent)

# 添加进url
urlpatterns += router.urls
```

### rest_framework APIView

```python
"""
继承APIView 接口响应及Paginator分页
"""
querySets = Student.objects.filter(delete=0).select_related('g').select_related('c')
page = request.GET.get('page')
limit = request.GET.get('limit')
if page:
  	limit_data = Paginator(querySets, limit).get_page(page)
    serializer = StudentSerializer(limit_data, many=True)
else:
    serializer = StudentSerializer(querySets, many=True)
    
# 前段框架分页构造数据结构
data = {
    'code': 0, 
    'msg': 'success',
    'count': querySets.count(),
    'data': serializer.data,
}

Response(data)

```







