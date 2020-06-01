from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
import house
import user
from house.models import Category, Comment, HouseForm, House, ImageForm, Images
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user
    try:
        profile = UserProfile.objects.get(user_id=current_user.id)

        # return HttpResponse(profile)
        context = {'category': category,
                   'profile': profile}

        return render(request, 'user_profile.html', context)
    except:
        return HttpResponseRedirect("/")


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was succesfully updated!')
            return redirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category
        })


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments, 'setting': setting,
    }

    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def addhouse(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = House()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['category']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'Your House Inserted Successfuly')
            return HttpResponseRedirect('/user/houses')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/addhouse')
    else:
        category = Category.objects.all()
        form = HouseForm()
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user_addhouse.html', context)


@login_required(login_url='/login')
def houseedit(request, id):
    house = House.objects.get(id=id)
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your House Updated Successfuly')
            return HttpResponseRedirect('/user/houses')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/houseedit/' + str(id))
    else:
        category = Category.objects.all()
        form = HouseForm(instance=house)
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user_addhouse.html', context)


@login_required(login_url='/login')
def houses(request):
    category = Category.objects.all()
    current_user = request.user
    houses = House.objects.filter(user_id=current_user.id, status='True')
    context = {
        'category': category,
        'houses': houses,
    }
    return render(request, 'user_houses.html', context)


@login_required(login_url='/login')
def housedelete(request, id):
    current_user = request.user
    House.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'House deleted..')
    return HttpResponseRedirect('/user/houses')


def houseaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.house_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been succesfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        house = House.objects.get(id=id)
        images = Images.objects.filter(house_id=id)
        form = ImageForm()
        context = {
            'house': house,
            'images': images,
            'form': form,
        }
        return render(request, 'houseImage_gallery.html', context)
