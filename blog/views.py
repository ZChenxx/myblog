from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import ArticleForm, TagForm, CategoryForm
from blog.models import Article, Tag, Category


class ArticleListView(ListView):  #当我们使用Django自带的ListView展示所有对象列表时，ListView默认会返回Model.objects.all()。
    template_name = "blog/published_article_list.html"
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(status='p').order_by('-pub_date')

@method_decorator(login_required,name='dispatch')
class PublishedArticleListView(ListView):
    template_name = "blog/published_article_list.html"
    paginate_by = 3

    def get_queryset(self):     #可以通过更具体的get_queryset方法来返回一个我们想要显示的对象列表。
        return Article.objects.filter(author=self.request.user).filter(status='p').order_by('-pub_date')

@method_decorator(login_required,name='dispatch')
class ArticleDraftListView(ListView):
    template_name = "blog/published_article_list.html"
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).filter(status='d').order_by('-pub_date')


class ArticleDetailView(DetailView): # DetailView和EditView都是从URL根据pk或其它参数调取一个对象来进行后续操作。
    model = Article
    template_name = "blog/article_detail.html"
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.viewed()                                          #
        return obj

@method_decorator(login_required,name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_create_form.html'

    def form_valid(self, form):                             #
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required,name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author !=self.request.user:
            raise Http404()
        return obj

@method_decorator(login_required,name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj

@method_decorator(login_required,name='dispatch')
def article_publish(request,pk,slug1):
    article = get_object_or_404(Article,pk=pk,author=request.user)
    article.published()




@login_required
def TagCreate(request):
    tag = Tag.objects.all()
    form = TagForm
    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("blog:tag_add"))

    return render(request,'blog/tag_create_form.html',{'tag':tag,'form':form})


@login_required
def CategoryCreate(request):
    if request.method == 'GET':
        category = Category.objects.all()
        form = CategoryForm()
        return render(request, 'blog/category_create_form.html', {'category': category, 'form': form})
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            parent_category = form.cleaned_data['parent_category']
            Category(name=name,parent_category=parent_category).save()
            return HttpResponseRedirect(reverse("blog:category_add"))

