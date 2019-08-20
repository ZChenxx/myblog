from django import forms
from .models import Article, Tag, Category

# 定制forms部件widget
# 　　Django 会把部件渲染成 HTML，这个渲染过程只会执行最小的工作量 -- 不会添加类名，或者其它具体的属性。这意味着，例如，所有 TextInput 部件会在你所有的Web页面上具有一样的外观。
# 　　有两种办法可以订制部件：一是定制部件的实例对象（订制 field 属性）；二是继承部件，定义内部类（订制 css 和 js 文件的链接）。

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['author','views','slug','pub_date','summary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        exclude = ['slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

CATEGORY = Category.objects.all()

class CategoryForm(forms.Form):
    name = forms.CharField()
    parent_category = forms.ModelChoiceField(queryset=CATEGORY)

#此 form 包含三个默认的 TextInput 部件，默认没有 CSS 类渲染，没有额外的属性。这意味着每个部件会具有同样的外观。


#form类所做的就是第一步就是快速生成html代码
#数据校验与错误信息提示
# f=ContactForm({'name':'BeginMan','age':100,'email':'x@163.com'})
# >>> f.is_bound    #一旦你对一个Form实体赋值，你就得到了一个绑定form
# True
# >>> f.is_valid()    #调用任何绑定form的is_valid()方法，就可以知道它的数据是否合法
# True
# >>> f = ContactForm({'name':'BeginMan'})
# >>> f.is_valid()
# False

#每一个邦定Form实体都有一个errors属性，它提供了一个字段与错误消息相映射的字典表。
# >>> f.errors
# {'age': [u'This field is required.']}
# >>> f.errors['age']
# [u'This field is required.']
# >>> f['age'].errors
# [u'This field is required.']

# 如果form对象的数据合法，则有cleaned_data属性，一个清理过的提交数据字典。
# 当通过一系列的数据来创建表单对象，并验证通过的时候，就要使用cleaned_data属性进行‘清理工作’，所谓的清理就是对给定的数据对应到python类型。
#
# >>> f.cleaned_data
# {'age': 100, 'name': u'BeginMan', 'email': u'x@163.com'}

# if request.method == 'POST':
#         form = ContactForm(request.POST)    #绑定post数据
#         ....
#  else:
#         form = ContactForm()  #如果表单未被提交，则一个未绑定的表单实例被创建

# Form.initial表单初始化。
#
# 我认为就是给表单绑定一些数据，用于特定显示或处理。当然这些可有可无，如提示等。如果提供，则是包含表单字段的字典类型。如：
#
# f = ContactForm(initial={'name':'Hi,here','email':'@'})
# 可以在表单类中初始化，也可以在表单对象中初始化，对于同一个字段的初始化，后者覆盖前者。