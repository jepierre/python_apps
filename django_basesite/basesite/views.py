from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import Post
from .forms import ContactForm
import datetime
from django.views.generic import DetailView, ListView
from django.utils import timezone

# Create your views here.
class HomePageView(TemplateView):
    # only display the first 3 posts on this page, ordered by date
    post_to_display = 3
    posts = Post.published.order_by('-publish')[:post_to_display]
    # get current time to send to html so that css will reload
    now = datetime.datetime.now().strftime('%H:%M:%S')

    def get(self, request, **kwargs):
        form = ContactForm()
        return render(request,'basesite\index.html',{'posts':self.posts,
            'time_value':self.now, 'form':form});

    # this can also be inherited from using View instead of TemplateView 
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalide header found.')
            return redirect('basesite:success')
        return render(request, "basesite\index.html", {'form':form})

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'basesite/post_detail.html'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['slug'],
                status='published',
                publish__year=self.kwargs['year'],
                publish__month=self.kwargs['month'],
                publish__day=self.kwargs['day'])
    
class PostListView(ListView):
    context_object_name = 'posts'
    template_name = 'basesite/post_list.html'
    pagination = 10 # new page every 10 posts

    def get_queryset(self):
        """ Returns all the post """
        return Post.published.order_by('-publish')

def successView(request):
    return HttpResponse("Success! Thank you for your message.")


