# on_delete参数的各个值的含义

分类专栏： [python](https://blog.csdn.net/ldq_sd/category_9627601.html) [编程](https://blog.csdn.net/ldq_sd/category_228239.html)

on_delete参数的各个值的含义：

1. `# 删除关联表中的数据时,当前表与其关联的field的行为`

```python
on_delete=None,
```

2. `# 删除关联数据,与之关联也删除`

```python
on_delete=models.CASCADE,
```

3. `# 删除关联数据,什么也不做`

 ```python
on_delete=models.DO_NOTHING,
 ```

4. `# 删除关联数据,引发错误ProtectedError`

```pyhton
on_delete=models.PROTECT,
```

5. `# 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）`

 ```python
# models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
on_delete=models.SET_NULL,
 ```

6. `# 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）`

 ```python
# models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
on_delete=models.SET_DEFAULT,
 ```

7. `# 删除关联数据,`

```python
# 与之关联的值设置为指定值,设置：models.SET(值)
# 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
on_delete=models.SET,
```

**注意：**

```python
# 多对多不需要on_delete。
```

