from django.shortcuts import render
from .models import Tweet,Comment
from .forms import Tweetform,CustomRegisterForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_str
from django.conf import settings 
# Create your views here.
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
def index(request):
    return render(request ,'socialize/index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    liked_tweet_ids = []

    if request.user.is_authenticated:
        liked_tweet_ids = Tweet.objects.filter(like=request.user).values_list('id', flat=True)

    return render(request, 'socialize/tweet_list.html', {
        'tweets': tweets,
        'liked_tweet_ids': liked_tweet_ids
    })

@login_required
def tweet_create(request):
    if request.method == "POST":
      form=Tweetform(request.POST,request.FILES)
      if form.is_valid():
          tweet=form.save(commit=False)
          tweet.user =request.user  
          tweet.save()
          return redirect ('tweet_list')      
    else:
        form =Tweetform()       
    return render(request,'socialize/tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet =get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
      form=Tweetform(request.POST,request.FILES,instance=tweet)
      if form.is_valid():
          tweet= form.save(commit=False)
          tweet.user=request.user
          tweet.save()
          return redirect('tweet_list')
    else:
        form=Tweetform(instance=tweet)
    return render(request,'socialize/tweet_form.html',{'form':form})
    
@login_required
def tweet_delete(request,tweet_id):
    tweet =get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'socialize/tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method=='POST':
      form=CustomRegisterForm(request.POST)
      if form.is_valid():
         user=form.save(commit=False) 
         user.set_password(form.cleaned_data['password'])
         user.is_active=False #Disable account until email verified 
         user.save()
         #send email verification 
         token=default_token_generator.make_token(user)
         uid=urlsafe_base64_encode(force_bytes(user.pk))
         activation_link=request.build_absolute_uri(reverse('activate',kwargs={'uidb64':uid,'token' :token})) 
         subject='Activate Your Account -BE SOCIALIZE'
         message=f'Hi {user.username},\n\nPlease click the link below to verify your account:\n\n{activation_link} '
         send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[user.email],fail_silently=False)




         messages.success(request,"Please check your email to activate your account ")
         return redirect('login')
    else:
        form =CustomRegisterForm()

    return render(request,'registration/register.html',{'form':form})


def User_login(request):
   if request.method=='POST':
      username= request.POST['username']
      password = request.POST['password']
      user= authenticate(request,username=username,password=password)
      if user is not None:
         login(request,user)
         return redirect('tweet_list')
      else:
         return render(request,'registration/login.html',{'error' :'Invalid credentials'})
   return render(request,'registration/login.html') 
@login_required 
def User_logout(request):
    logout(request)
    return redirect(request,'socialize/tweet_list.html')    
   
def search_result(request):
   querry=request.GET.get('q')
   result=[]
   if querry:
      result= Tweet.objects.filter(Q(text__icontains=querry) | Q(user__username__icontains=querry)).order_by('-created_at')
   return render(request,'socialize/search_result.html',{'querry':querry,'results':result})

def test(request):
   tweet=Tweet.objects.all().order_by('-created_at')
   return render(request,'socialize/test.html',{'tweets':tweet})
@login_required
def like(request,tweet_id):
   tweet=get_object_or_404(Tweet,pk=tweet_id,)
   liked =False
   if request.user.is_authenticated:
      if request.user in tweet.like.all():
         tweet.like.remove(request.user) # unlike
      else:
         tweet.like.add(request.user) # like 
         liked=True
   return JsonResponse({'liked':liked,'liked_count':tweet.like.count})
@login_required
def add_comment(request,tweet_id):
    if request.method=='POST':
        tweet=get_object_or_404(Tweet,pk=tweet_id)
        text=request.POST.get('comment_text','').strip()
        if text:
           Comment.objects.create(
              tweet=tweet,
              text=text,
              user=request.user
           )
    return redirect('tweet_list')

@csrf_exempt
def increment_share_count(request, tweet_id):
    if request.method == "POST":
        try:
            tweet = Tweet.objects.get(id=tweet_id)
            tweet.share_count += 1
            tweet.save()
            return JsonResponse({'success': True, 'share_count': tweet.share_count})
        except Tweet.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tweet not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect('register')      
      
     
         
         
      
   