from django import forms
from .models import Article, Tag, Category


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

