import re
from django.shortcuts import render, HttpResponse, redirect
from doubt.models import doubt, Answer
from django.contrib import messages
from django.contrib.auth.models import User
# from blog.templatetags import extras


def blogHome(request):
    allPosts = doubt.objects.all()
    context = {'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)


def blogPost(request, slug):
    post = doubt.objects.filter(slug=slug).first()
    if post:
        post.views = post.views + 1
        post.save()
    comments = Answer.objects.filter(post=post, parent=None)
    replies = Answer.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments,
               'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = doubt.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = Answer(comment=comment, user=user, post=post)
            comment.save()
            messages.success(
                request, "Your comment has been posted successfully")
        else:
            parent = Answer.objects.get(sno=parentSno)
            comment = Answer(
                comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(
                request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")
