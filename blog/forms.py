from django import forms
from .models import Article, Tag, Category

# 定制forms部件widget
# 　　Django 会把部件渲染成 HTML，这个渲染过程只会执行最小的工作量 -- 不会添加类名，或者其它具体的属性。这意味着，例如，所有 TextInput 部件会在你所有的Web页面上具有一样的外观。
# 　　有两种办法可以订制部件：一是定制部件的实例对象（订制 field 属性）；二是继承部件，定义内部类（订制 css 和 js 文件的链接）。

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['author','views','slug','pub_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),    ##多对多字段
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