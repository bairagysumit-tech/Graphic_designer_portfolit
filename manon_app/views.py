from django.shortcuts import render, redirect
from manon_app.models import Design, BlogData, Image, OtpStore, UserProfile, LikeData,\
    CommentData, ReplyData, Subscribe, LikeDesign
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from _ast import Pass
import random
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.contrib import auth
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import redirect_to_login
#from audioop import reverse
from django.contrib.messages.context_processors import messages

# Create your views here.
def Home(req):
    dict_={}
    for i in range(1):
        dict_['image%d' %i]='hello'+str(i)
    all_design = Design.objects.all().order_by('-id')[:20]
    act = 'nav_active'
    return render(req, 'manon_home.html',{'active_home':act, 'ad':all_design})


def About(req):
    act = 'nav_active'
    return render(req, 'manon_about.html',{'active_about':act})

def Portfolio(req):
    act = 'nav_active'
    flyer = Design.objects.filter(catagory = 'Flyer').order_by('-id')[:20]
    brochure = Design.objects.filter(catagory = 'Brochure').order_by('-id')[:20]
    branding = Design.objects.filter(catagory = 'Branding').order_by('-id')[:20]
    instagram = Design.objects.filter(catagory = 'Instagram').order_by('-id')[:20]
    post_card = Design.objects.filter(catagory = 'Post_Card').order_by('-id')[:20]
    rack_card = Design.objects.filter(catagory = 'Rack_Card').order_by('-id')[:20]
    buisness_card = Design.objects.filter(catagory = 'Buisness_Card').order_by('-id')[:20]
    bookcover = Design.objects.filter(catagory = 'Book Cover').order_by('-id')[:20]
    all_post = Design.objects.all()
    dict = {'ap':all_post,'active_port':act, 'flyer':flyer, 'brochure':brochure, 'branding':branding, 'instagram':instagram, 'post_Card':post_card, 'rack_card':rack_card, 'buisness_card':buisness_card,'book_cover':bookcover,}
    return render(req, 'manon_portfolio.html',dict)

def Blog(req):
    blog = BlogData.objects.all().order_by('-id')
    image= Image.objects.all()
    like = LikeData.objects.all()
    comment = CommentData.objects.all()
    act = 'nav_active'
    return render(req, 'manon_blog.html',{'active_blog':act,'image':image, 'blog':blog, 'like1':like,'comment':comment})

def BlogDitels(req, blog_slug):
    if req.method == "POST":
        comm = req.POST.get('comment')
        user = req.user
        post = BlogData.objects.get(blog_slug = blog_slug)
        comment = CommentData(user = user, post = post, comm = comm)
        comment.save()
        cc = CommentData.objects.filter(post = post, comm_status = 'Published').count()
        cs = BlogData(id = post.id, comment = cc )
        cs.save(update_fields=["comment"])
        
        
    comme= CommentData.objects.all().order_by('-id')
    blog = BlogData.objects.get(blog_slug = blog_slug)
    image= Image.objects.filter(image_id = blog)
    like = LikeData.objects.all()
    reply= ReplyData.objects.filter(post = blog)
    act = 'nav_active'
    return render(req, 'postditels.html',{'active_blog':act,'blog':blog, 'image':image, 'like1':like, 'comment':comme,'reply':reply})

def Contact(req):
    act = 'nav_active'
    return render(req, 'manon_contact.html',{'active_contact':act})

def blogview(req):
    ad = BlogData.objects.all()
    ai = Image.objects.all()
    return render(req, 'blog_view.html', {'ad':ad, 'ai':ai})

def SignIn(req):
    next_url = req.GET.get('next', '')
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        x=authenticate(req, username = username, password = password)
        if x is None:
            massage = "User name Not Valid."
            return render(req, 'signin.html',{'massage':massage})
        
        elif x.is_superuser:
            login(req,x)
            if next_url == '':
                return redirect('/')
            else:
                return redirect(next_url)
            
        else:
            user_obj = User.objects.filter(username = username).first()
            get_user = UserProfile.objects.get(user = user_obj)
            
            if x.is_superuser:
                login(req,x)
                return redirect(next_url)
            
            elif get_user.profile == 'staf' and get_user.status == True:
                if next_url == '':
                    return redirect('/')
                else:
                    return redirect(next_url)
            else:
                massage = "User Is Desible."
                return render(req, 'signin.html',{'massage':massage})
    else:
        return render(req, 'signin.html')
    
def SignUp(req):
    if req.method == "POST":
        email = req.POST.get('email')
        password = req.POST.get('password')
        re_password= req.POST.get('repassword')
        f_name = req.POST.get('f-name')
        l_name = req.POST.get('l-name')
        
        if (len(email)== 0 ) and (len(password) == 0) and (len(f_name) == 0) and (len(l_name)== 0):
            wm='Some field are empty!!'
            cl = 'd-b alert alert-danger'
            context={'wm':wm, 'cl':cl}
            return render(req, 'signup.html',context)
        
        else:
            check_user = User.objects.filter(username = email).first()
            if check_user:
                wm='Some field are empty!!'
                cl = 'd-b alert alert-danger'
                context={'wm':wm, 'cl':cl}
                return render(req, 'signup.html',context)
            
            else:
                newuser=User.objects.create_user(username=email, password=password)
                newuser.save()
                
                randomotp = str(random.randint(1000,9999))
                subject="test email"
                reply_to_list=[email]
                emailsave = EmailMessage(subject,randomotp,'nextversionn@gmail.com',reply_to_list)
                emailsave.send(fail_silently=True)
                 
                userprofile =  UserProfile(user=newuser, f_name = f_name, l_name = l_name)
                userprofile.save()
                
                otpsave = OtpStore(user = newuser, otp = randomotp)
                otpsave.save()
                
                req.session['email1'] = email
                return redirect('/otp_check')
    else:
        return render(req, 'signup.html')
        
def OtpCheck(req):
    if req.user.is_authenticated:
        return redirect('/')
    try:
        user1 = req.session['email1']
        user_obj = User.objects.filter(username = user1).first()
        get_user = OtpStore.objects.get(user = user_obj)
        if get_user.otp_count < 4:
            if req.method == "POST":
                get_otp = req.POST.get('otp')
                if get_user.otp == get_otp:
                    get_user.vrify=True
                    get_user.save()
                    return redirect('/signin')
                else:
                    old_count = get_user.otp_count
                    get_user.otp_count =old_count + 1
                    get_user.save(update_fields=["otp_count"]) 
                    oc = old_count +1
                    wm='Wrong OTP '
                    cl = 'd-b alert alert-danger'
                    context={'wm':wm, 'cl':cl, 'oc1':oc}
                    return render(req, 'otp_check.html', context)
            else:
                return render(req, 'otp_check.html')
        else:
            return redirect('/otp')
        return render(req, 'otp_check.html')
    except:
        wu = 'Undifine Error!!!!'
        context={'massage':wu}
        return render(req, 'error.html', context)
    
def testemail(req):
    subject="test email"
    message="hi sikbh how are you"
    reply_to_list=['']
    email = EmailMessage(subject,message,'nextversionn@gmail.com',reply_to_list)
    email.send(fail_silently=True)
    #send_mail( 'LogIn OTP', 'hello','nextversionn@gmail.com',[email])
    return render(req, 'signin.html')

def signup_test(req):
    if req.method == "POST":
        password = req.POST.get('password')
        if len(password) >7:
            return redirect('/otp')
        else:
            return render(req, 'signup.html')
    else:
        return render(req, 'signup.html')
    
def design_upload(req):
    return render(req, 'admin/design_upload.html')

def BlogInsert(req):
    if req.method == "POST":
        lr = req.POST.get('lr')
        blog1 = req.POST.get('blog')
        blog_text = req.POST.get('blog_text')
        tag = req.POST.get('tag')
        img_alt = req.POST.get('image_alt')
        img_title= req.POST.get('image_title')
        bd = BlogData(title1 = blog1, blog = blog_text, blog_tag = tag)
        bd.save()
        looprange = int(lr)
        dict = {}
        if looprange>0:
            for i in range(looprange):
                key = str("image"+str(i))
                dict[key]=req.FILES['image'+str(i)]
                bi = Image(image_id = bd, image=dict[key], img_alt = img_alt, img_title = img_title)
                bi.save()
        else:
            pass
        return redirect('/blog')
    else:
        return render(req, 'manon_blog.html')
       
def SignOut(req):
    next_url = req.GET.get('next', '')
    if next_url == '':
        auth.logout(req)
        return redirect('/')
    else:
        auth.logout(req)
        return redirect(next_url)

def Blog_Delete(req, pk):
    if req.method == "POST":
        blog = BlogData.objects.get(id = pk)
        blog.delete()
        return redirect('/blog')
    else:
        blog = BlogData.objects.get(id = pk)
        image = Image.objects.filter(image_id = blog)
        return render(req, 'blogdelete.html', {'blog':blog, 'image':image})
    
def Blog_Edit(req, pk):
    if req.method == "POST":
        blog_data = BlogData()
    
        lr = req.POST.get('lr')
        blog1 = req.POST.get('blog')
        blog_text = req.POST.get('blog_text')
        tag = req.POST.get('blog_tag')
        
        bd = BlogData()
        bd.id = pk
        bd.title1 = blog1
        bd.blog = blog_text
        bd.status = True
        bd.blog_tag = tag
        bd.save()
      
        looprange = int(lr)
        dict = {}
        if looprange>0:
            for i in range(looprange):
                key = str("image"+str(i))
                dict[key]=req.FILES['image'+str(i)]
                bi = Image(image_id = bd, image=dict[key])
                bi.save()
        else:
            pass
        return redirect('/blog')
    else:
        blog = BlogData.objects.get(id = pk)
        image = Image.objects.filter(image_id = blog)
        return render(req, 'blog_edit.html', {'blog':blog, 'image':image})
    
def BlogPP(req):
    if req.user.is_authenticated:
        post_id = req.POST.get('postid')
        post = BlogData.objects.filter(id=post_id).first()
        
        ps = post.status
        
        
        if ps == True:
            bs = BlogData(id = post_id, status = False)
            bs.save(update_fields=["status"])
            
        else:
            bs = BlogData(id = post_id, status = True)
            bs.save(update_fields=["status"])
               
    else:
        return redirect("/")
    return HttpResponse('Liked!')
            
def PostLike(req):
    if req.user.is_authenticated:
        get_user = req.user
        post_id = req.POST.get('postid')
        post = BlogData.objects.filter(id=post_id).first()
        lf = LikeData.objects.filter(user=get_user,post=post_id).first()
        if lf is None:
            li=LikeData(user=get_user,  post = post, like = True )
            li.save()
            lc = LikeData.objects.filter(post = post_id, like = True).count()
            liadd = BlogData(id = post_id, like = lc )
            liadd.save(update_fields=["like"])
        else:
            if lf.like == False:
                li=LikeData(user=get_user, id = lf.id, post = post, like = True )
                li.save(update_fields=["like"])
                lc = LikeData.objects.filter(post = post_id, like = True).count()
                liadd = BlogData(id = post_id, like = lc )
                liadd.save(update_fields=["like"])
            else:
                li=LikeData(user=get_user, id = lf.id,  post = post, like = False )
                li.save(update_fields=["like"])
                lc = LikeData.objects.filter(post = post_id, like = True).count()
                liadd = BlogData(id = post_id, like = lc )
                liadd.save(update_fields=["like"])
                
    else:
        return render(req, 'signin.html')
    return HttpResponse('Liked!')

def CommentReply(req):
    if req.method == "POST":
        user = req.user
        comment = req.POST.get('comment')
        post_id = req.POST.get('post')
        reply = req.POST.get('reply')
        next_url = req.POST.get('next','')
        post = BlogData.objects.filter(id=post_id).first()
        comm = CommentData.objects.filter(id=comment).first()
        reply_data = ReplyData( post = post, comment = comm, user=user, reply = reply)
        reply_data.save()
        return redirect(next_url)
    else:
        return HttpResponse('Reply Done!')

def DesignInsert(req):
    if req.method == "POST":
        image = req.FILES['image']
        type = req.POST.get('type')
        desc = req.POST.get('desc')
        view = req.POST.get('design_view')
        like = req.POST.get('design_like')
        tag = req.POST.get('design_tag')
        di = Design(catagory= type, image = image, ditels=desc, design_view = view, design_like1=like, design_tag = tag )
        di.save()
        return render(req, 'designinsert.html')
    else:
        return render(req, 'designinsert.html')

def DesignUpdate(req, pk):
    image_id = Design.objects.get(id=pk)
    
    if req.method == "POST":
        image = req.POST.get('image')
        type = req.POST.get('type')
        desc = req.POST.get('desc')
        view = req.POST.get('design_view')
        like = req.POST.get('design_like')
        tag = req.POST.get('design_tag')
        if image != '':
            di = Design()
            di.id = pk
            di.catagory= type
            di.image = image
            di.ditels=desc
            di.design_view = view
            di.design_like1 = like
            di.design_tag = tag 
            di.save()
            url = '/design-ditels/'+di.image_slug+'/'
            return redirect(url)
        else:
            di = Design()
            di.id = pk
            di.catagory= type
            di.ditels=desc
            di.design_view = view
            di.design_like1 = like
            di.image = image_id.image
            di.design_tag = tag
            di.save()
            url = '/design-ditels/'+di.image_slug+'/'
            return redirect(url)
    else:
        image = Design.objects.get(id=pk)
        return render(req, 'designinsert.html', {'image':image})

def DesignDelete(req, pk):
    image = Design.objects.get(id=pk)
    image.delete()
    return redirect('/portfolio/')

def DesignDitels(req, image_slug):
    act = 'nav_active'
    get_design = Design.objects.filter(image_slug = image_slug).first()
    
    gad = Design.objects.filter(catagory  = get_design.catagory ).exclude(image_slug = image_slug)
    
    flyer     = Design.objects.filter(catagory = 'Flyer').order_by('-id')
    brochure  = Design.objects.filter(catagory = 'Brochure').order_by('-id')
    branding  = Design.objects.filter(catagory = 'Branding').order_by('-id')
    instagram = Design.objects.filter(catagory = 'Instagram').order_by('-id')
    post_card = Design.objects.filter(catagory = 'Post_Card').order_by('-id')
    rack_card = Design.objects.filter(catagory = 'Rack_Card').order_by('-id')
    buisness_card = Design.objects.filter(catagory = 'Buisness_Card').order_by('-id')
    all_design = Design.objects.all()
    dict = {'ap':all_design,'get_design': get_design, 'gad':gad, 'active_port':act, 'flyer':flyer, 'brochure':brochure, 'branding':branding, 'instagram':instagram, 'post_Card':post_card, 'rack_card':rack_card, 'buisness_card':buisness_card}
    
    return render(req, 'designditels.html',dict)

def AllDesign(req, designtype):
    act = 'nav_active'
    dt = str(designtype)
    alldesign = Design.objects.filter(catagory = dt).order_by('-id')
    return render(req, 'all-design.html', {'ad':alldesign, 'active_port':act})


def DesignLike(req):
    if req.user.is_authenticated:
        get_user = req.user
        post_id = req.POST.get('postid')
        post = Design.objects.filter(id=post_id).first()
        lf = LikeDesign.objects.filter(user=get_user,post=post_id).first()
        if lf is None:
            li=LikeDesign(user=get_user,  post = post, like = True )
            li.save()
            lc = LikeDesign.objects.filter(post = post_id, like = True).count()
            liadd = Design(id = post_id, design_like = lc )
            liadd.save(update_fields=["design_like"])
        else:
            if lf.like == False:
                li=LikeDesign(user=get_user, id = lf.id, post = post, like = True )
                li.save(update_fields=["like"])
                lc = LikeDesign.objects.filter(post = post_id, like = True).count()
                liadd = Design(id = post_id, design_like = lc )
                liadd.save(update_fields=["design_like"])
            else:
                li=LikeDesign(user=get_user, id = lf.id,  post = post, like = False )
                li.save(update_fields=["like"])
                lc = LikeDesign.objects.filter(post = post_id, like = True).count()
                liadd = Design(id = post_id, design_like = lc )
                liadd.save(update_fields=["design_like"])
                
    else:
        return render(req, 'signin.html')
    return HttpResponse('Liked!')

def AllSignin(req):
    
    return render(req, 'all_signin.html')

def EmailSubs(req):
    name = req.POST.get('name')
    email= req.POST.get('postid')
    check_email = Subscribe.objects.filter(email = email).first()
    if check_email:
        return HttpResponse("Exists")
    else:
        se = Subscribe(email = email,name=name)
        se.save()
        return HttpResponse("Success Your Subscribe")
    return HttpResponse("Email Send Done!!!")


def DesignViewCount(req):
    design = req.POST.get('postid')
    get_design = Design.objects.filter(image_slug = design).first()
    dv = get_design.design_view
    if dv == None:
        view_count = Design(id =get_design.id, design_view =  1)
        view_count.save(update_fields=["design_view"])
    else:
        view_count = Design(id =get_design.id, design_view = dv + 1)
        view_count.save(update_fields=["design_view"])
    return HttpResponse("view count")

def BlogViewCount(req):
    design = req.POST.get('postid')
    get_design = BlogData.objects.filter(id = design).first()
    dv = get_design.blog_view
    if dv == None:
        view_count = BlogData(id =get_design.id, blog_view =  1)
        view_count.save(update_fields=["blog_view"])
    else:
        view_count = BlogData(id =get_design.id, blog_view = dv + 1)
        view_count.save(update_fields=["blog_view"])
    return HttpResponse("view count")

def BlogImageDelete(req):
    image_id = req.POST.get('postid')
    image = Image.objects.filter(id = image_id).first()
    image.delete()
    return HttpResponse('Image Delete....')

def CommentStatus(req):
    comment_id = req.POST.get('comment_id')
    comment = CommentData.objects.filter(id = comment_id).first()
    cs = comment.comm_status
    if cs == 'Under Review':
        comm = CommentData(id =comment.id, comm_status = 'Published')
        comm.save(update_fields=["comm_status"])
    else:
        comm = CommentData(id =comment.id, comm_status = 'Under Review')
        comm.save(update_fields=["comm_status"])
    return HttpResponse('Image Delete....')

def CommentDelete(req):
    comment_id = req.POST.get('comment_id')
    comment = CommentData.objects.filter(id = comment_id).first()
    comment.delete()
    return HttpResponse('Comment Delete....')




