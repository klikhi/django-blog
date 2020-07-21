from django.shortcuts import render, get_object_or_404,redirect
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users.models import Profile
from .models import Post, Likes,Comment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
# from .forms import CommentForm
def home(request):
    context={
        'posts':Post.objects.filter(draft=0)
    }
    return render(request,'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name='blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(draft=0)

# def like_post(request):
#     user = request.user
#     if request.method=='POST':
#         print(1)
#         if "ajax" in request.POST:
#             print(2)
#             post_id = request.POST.get('post_id')
#             print(post_id)
#             post_obj = Post.objects.get(id=post_id)
#             if "like" in request.POST:
#                 print(3)
#                 post_obj.liked.add(user)
#             elif "unlike" in request.POST:
#                 print(4)
#                 post_obj.liked.remove(user)

#             like, created = Likes.objects.get_or_create(author=user,post_id=post_id)
#             if not created:
#                 if like.value == 'Like':
#                     like.value = 'Unlike'
#                 else:
#                     like.value = 'Like'

#             else(like.save()):
#                 print("Hurrah")

#             return JsonResponse({"count":post_obj.liked.all().count(),"status":1})
#     return render(request,"blog/home.html",{})

# @login_required
def like_post(request):
    user=request.user
    # print(user)
    if request.method=="POST":
        if user.is_authenticated:
            post_id = request.POST.get("post_id")
            # print(post_id)
            post_obj= Post.objects.get(id=post_id)
            if user in post_obj.liked.all():
                post_obj.liked.remove(user)
            else:
                post_obj.liked.add(user)
            return JsonResponse({'count':post_obj.liked.all().count(),'status':1})
            # return JsonResponse({'count':post_obj.liked.all().count()})
        else:
            return JsonResponse({'status':0})
            # return render(request,"users/login.html",{})
    return HttpResponse()

def post_serialized(request):
    data = list(Post.objects.values())
    return JsonResponse(data,safe=False)


class UserPostListView(ListView):
    model = Post
    template_name='blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    paginate_by = 5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model=Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    template_name="blog/post_form.html"
    # form_class=postForm
    # def get_success_url(self):
    #     return reverse('blog-home')
    # success_url = reverse_lazy('blog-home')
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
        def get_initial(self):
            return {}

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        title = post_obj.title
        content = post_obj.content
        # print("In post")
        # initial_base = self.get_initial()
        # initial_base['title']=title
        # initial_base['content']=content
        form_class=self.get_form_class()
        draft_form = form_class(instance=post_obj)
        # print(draft_form)
        # form=self.get_form(form_class)
        # print(form)
        # print(initial_base['content'])
        # form.title =title
        # form.content=content
        # print(form.title)
        # return HttpResponse()
        # print(form)
        context = {'form':draft_form}
        return render(request,"blog/post_form.html",context)

    # template_name=<modelname>_<form>

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url="/"
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

def commentView(request):
    user = request.user
    if request.method == "POST":
        if "post_comment" in request.POST:
            if(user.is_authenticated):
                post_id = request.POST.get("post_id")
                # print(post_id)
                comment_text = request.POST.get("comment")
                # print(comment_text)
                post_obj = Post.objects.get(id=post_id)
                post_obj.comments.add(user)

                comment_obj, created = Comment.objects.get_or_create(author=user,post_id=post_id)
                comment_obj.comment = comment_text
                    # print(comment_obj.comment)
                comment_obj.save()
                return JsonResponse({'status':1})
            else:
                # return render(request,"users/login.html",{})
                return JsonResponse({'status':0})
        elif "get_comments" in request.POST:
            data = {"comments":[]}
            post_id = request.POST.get("post_id")
            comments = Comment.objects.filter(post_id=post_id)
            for comment in comments:
                data["comments"].append({"comments":comment.comment,"author":User.objects.get(pk=comment.author_id).username,"date_posted":(comment.date_posted).strftime("%B, %d %Y"),"pro_img":Profile.objects.get(user_id=comment.author_id).image.url})
            return JsonResponse(data)
        return HttpResponse()

def drafts(request):
    user=request.user
    if request.method=="POST":
        if "save_draft" in request.POST:
            title = request.POST.get("title")
            content=request.POST.get("content")
            draft_count=Post.objects.filter(author_id=user,draft=1).count()
            # print(draft_count)
            if draft_count<=5:

                post = Post(title=title,content=content,author=user,draft=True)
                # print("check")
                post.save()
                # print("success")
                return JsonResponse({'status':1})
            elif draft_count>5:
                return JsonResponse({'status':6})
            else:
                return JsonResponse({'status':0})

        if "get_draft" in request.POST:
            posts = Post.objects.filter(author=user,draft=True)
            response={'posts':[]}
            for post in posts:
                response["posts"].append({"content":post.content,"title":post.title,"post_id":post.id})
            return JsonResponse(response)


        if "delete_draft" in request.POST:
            post_id=request.POST.get("post_id")
            Post.objects.filter(id=post_id).delete()
            # return JsonResponse({"status":1})
            return render(request,"blog/home.html",{})

        return HttpResponse()


def about(request):
    return render(request,'blog/about.html',{'title':'About'})
