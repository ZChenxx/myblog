import datetime

import unidecode as unidecode
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse


class Article(models.Model):

    STATUS_CHOICES = (
        ('d','草稿'),
        ('p','发表'),
    )

    title = models.CharField('标题',max_length=200,unique=True)
    #Django中的Slug会为每条model记录，自动（当然可以手动）的根据当前记录的每个字段的Value生成一个URL路径（唯一的），
    # 使得你的URL更加的易读（或者也能规避一些额外的问题）
    slug = models.SlugField('slug',max_length=60,blank=True)
    body = models.TextField('正文')
    summary = models.CharField(max_length=200,blank=True,verbose_name="博客摘要")
    pub_date = models.DateTimeField('发布时间',null=True)
    create_date = models.DateTimeField('创建时间',auto_now_add=True) #添加时的时间，更新对象不会有变动
    mod_date = models.DateTimeField('修改时间',auto_now=True) #有修改动作，就会变
    status = models.CharField('文章状态',max_length=1,choices=STATUS_CHOICES,default='p')
    views = models.PositiveIntegerField('浏览量',default=0)
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE,default='')
    category = models.ForeignKey('Category',verbose_name='分类',on_delete=models.CASCADE,blank=False,null=False,default='')
    tags = models.ManyToManyField('Tag',verbose_name='标签集合',blank=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(unidecode.unidecode(self.title))
        self.summary = self.body[:60]
        super().save(*args,**kwargs)

    def clean(self):
        if self.status == 'd' and self.pub_date is not None:
            self.pub_date = None
        if self.status == 'p' and self.pub_date is None:
            self.pub_date = datetime.datetime.now()

    def get_absolute_url(self):
        return reverse('blog:article_detail',args=[str(self.pk),self.slug])

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def published(self):
        self.status = 'p'
        self.pub_date = datetime.datetime.now()
        self.save(update_fields=['status','pub_date'])

    class Meta:
        ordering = ['-pub_date']    ## 按降序排列，-表示降序
        verbose_name = "文章"
        verbose_name_plural = verbose_name   ##复数形式

class Category(models.Model):
    name = models.CharField('分类名',max_length=30,unique=True)
    slug = models.SlugField('slug',max_length=40)
    parent_category = models.ForeignKey('self',verbose_name="父级分类",blank=True,null=True,on_delete=models.CASCADE,default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail',args=[self.slug])

    def has_child(self):
        if self.category_set.all().count() > 0:
            return True



    def save(self,*args,**kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(unidecode.unidecode(self.name))

        super().save(*args,**kwargs)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

class Tag(models.Model):
    name = models.CharField('标签名',max_length=30,unique=True)
    slug = models.SlugField('slug',max_length=40)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail',args=[self.slug])

    def get_article_count(self):
        return Article.objects.filter(tags__slug=self.slug).count()

    def save(self,*args,**kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(unidecode.unidecode(self.name))

        super().save(*args,**kwargs)