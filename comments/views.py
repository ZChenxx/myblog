from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from blog.models import Article
from comments.forms import CommentForm
from comments.models import Comment


def article_comment(request,pk):
    article = get_object_or_404(Article,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = request.POST
            Comment(user=request.user,text=data['text'],article=article).save()
            return reverse('blog:article_detail',kwargs={'pk':article.pk,'slug':article.slug})
        else:
            return render(request,'blog/article_detail.html',context={'article':article})

    return reverse('blog:article_detail',kwargs={'pk':article.pk,'slug':article.slug})