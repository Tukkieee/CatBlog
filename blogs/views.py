from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView,DetailView,UpdateView, View
# from .models import Blog
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Blog, Comment
from accounts.models import UserAccount
from .forms import CommentForm, BlogForm
from django.urls import reverse_lazy, reverse
from accounts.form import UpdateUserForm
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
class HomePage(ListView):
    model = Blog
    template_name = "index.html"
    # context_object_name= "posts"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add your first context variable
        context['categories'] = Category.objects.all()

        # Add your second context variable
        context['latest_posts'] = Blog.objects.filter(publish=True).order_by('-date_published')[:5]
        context['posts'] = Blog.objects.filter(publish=True)

        return context

class DetailPage(DetailView):
    template_name = "blogs/detail.html"
    model = Blog
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        # print(self.kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        # print(context)
        context['categories'] = Category.objects.all()
        context['latest_posts'] = Blog.objects.filter(publish=True).order_by('-date_published')[:5]
      
        context['comments'] = Comment.objects.filter(blog__slug=self.kwargs.get('slug'))

        context['comment_form'] = CommentForm(user=self.request.user)
        return context
    
    def handle_comment_submission(self, form, blog_post):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user = None

        form.instance.blog = blog_post
        form.save()

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        blog_post = self.get_object()

        if form.is_valid():
            self.handle_comment_submission(form, blog_post)
            return redirect('detail', slug=self.kwargs.get('slug'))
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = form
            return self.render_to_response(context)
   
            
    
class CategoryPage(ListView):
    model = Blog
    template_name = "blogs/category.html"
    context_object_name= "posts"

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return Blog.objects.filter(category__slug=category_slug).filter(publish=True) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['latest_posts'] = Blog.objects.filter(publish=True).order_by('-date_published')[:5]

        return context


    

class UserDetailView(DetailView):
    model = UserAccount
    template_name = 'blogs/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['posts'] = Blog.objects.filter(user=user)
        return context
    
class ProfilePage(DetailView):
    model = UserAccount
    template_name = 'blogs/profile.html'
    context_object_name = 'user'
    # slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['posts'] = Blog.objects.filter(user=user)
        return context
    
    
class ProfileUpdateView(UpdateView):
    form_class = UpdateUserForm
    model = UserAccount
    template_name = 'blogs/profile.html'
    success_message = "Update successful."

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.object.pk})
    
class PublishedListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogs/publishedpost.html'
    context_object_name = 'published'
    ordering = ['-date_published']
    

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, publish=True)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            post_id = request.POST.get('delete')
            print(post_id)
            post = Blog.objects.get(id=post_id)
            post.delete()
        elif 'unpublish' in request.POST:
            post_id = request.POST.get('unpublish')
            post = Blog.objects.get(id=post_id)
            post.unpublish_post()
            post.save()
        # return redirect(reverse('user_profile'))
            
class UnpublishedListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogs/unpublishedpost.html'
    context_object_name = 'unpublished'
    ordering = ['-date_published']
    

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, publish=False)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            post_id = request.POST.get('delete')
            print(post_id)
            post = Blog.objects.get(id=post_id)
            post.delete()
        elif 'unpublish' in request.POST:
            post_id = request.POST.get('unpublish')
            post = Blog.objects.get(id=post_id)
            post.publish_post()
            post.save()
        # return redirect(reverse('user_profile'))
            
class CreateBlogView(LoginRequiredMixin, CreateView):
    template_name = "blogs/create_blog.html"
    form_class = BlogForm
    success_message = "New blog created successfully"
    success_url= reverse_lazy('home')
    

    # def get_success_url(self):
    #     return reverse_lazy('user_profile',  kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
            

# class CreateBlogView(View):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.object
#         context['posts'] = Blog.objects.filter(user=user)
#         context['blog_form'] = BlogForm(instance=user)
#         return context  

#     def post(self, request, *args, **kwargs):
#         form = BlogForm(request.POST)
#         if form.is_valid():
#             blog = form.save(commit=False)
#             blog.user = request.user
#             blog.save()
#             form_html = render_to_string('blogs/create_blog.html', {'form': form}, request=request)
#             return JsonResponse({'form_html': form_html})
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)