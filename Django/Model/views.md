###  Model

- class - A

```python
class A(models.Model):
    name = models.CharField(max_length=50)
```

- class - B

```python
class B(models.Model):
    desc = models.CharField(max_length=50)
    feature = models.CharField(max_length=50)
    # blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填
    a = models.ForeignKey(A, on_delete=models.CASCADE, blank=True, null=True)
```

### 正向查询和反向查询

```python
# Django ForeignKey 正向查询
B.objects.filter(delete=0).select_related('a').select_related('xxx')
B.objects.all().select_related('a').select_related('xxx')

# Django ForeignKey 反向查询
A.objects.filter(delete=0).first().b_set.all()
A.objects.filter(delete=0).first().b_set.filter(desc__contains="xxx")  # 各种条件
A.objects.all().first().b_set.all()
A.objects.get(id=1).b_set.all()

# <比较> 反查性能低与两次filter查询
a = A.objects.get(id=1)
B.objects.filter(a=a)
```



### 批量创建/更新/删除

```python
"""
批量插入数据的时候，首先要创建的列表，然后调用bulk_create方法，一次将列表中的数据插入到数据库中。
"""
product_list_to_insert = list()
for x in range(10):
    product_list_to_insert.append(A(name=str(x), price=x))
A.objects.bulk_create(product_list_to_insert)

"""
批量更新数据时，先进行数据过滤，然后再调用update方法进行一次性地更新。
"""
A.objects.filter(name__contains='XXX').update(name='new XXX')

"""
批量更新数据时，先是进行数据过滤，然后再调用delete方法进行一次性删除。
"""
A.objects.filter(name__contains='XXX').delete()

```



