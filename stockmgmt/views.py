from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout

# Create your views here.

from stockmgmt.models import Stock
from stockmgmt.forms import StockCreateForm
from stockmgmt.forms import StockSearchForm
from stockmgmt.forms import StockUpdateForm


def home(request):
	title = 'Welcome: This is the home Page'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)

#def login(request):
	#title = 'Welcome: This is the login Page'
	#context = {
	#"title": title,
	#}
	#return render(request, "login.html",context)



#def login(request):
#
 #   title = 'Welcome: This is the login Page'
  #  context = {
#        "title": title,
 #   }
#
 #   if request.method == 'POST':
  #      username = request.POST['username']
   #     password = request.POST['password']
   #     if username == 'admin' and password == 'admin':
    #        return redirect('list_item_user')
     #   else:
            #return redirect('list_item')
   # else:
   #     return render(request, 'login.html', context)




from django.contrib.auth import authenticate, login as login_user

def login(request):
    # Process login form submission
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if the authentication was successful
        if user is not None:
            login_user(request, user)
            if user.is_superuser:  # check if the user is an admin
                return redirect('list_item')  # redirect to the admin interface
            elif user.is_authenticated:  # check if the user is authenticated
                return redirect('list_item_user')  # redirect to the list item page
            else:
                return redirect('home')  # redirect to the home page
        else:
            # Authentication failed
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})

    # Display the login form
    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'login' with the name of your login page URL



def forgot_passwd(request):
	title = 'forgot password'
	context = {
	"title": title,
	}
	return render(request, "forgot_passwd.html",context)



def list_item(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    
    if request.method == "POST" :
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                            item_name__icontains=form['item_name'].value()
                                            )
        context = {
            "form": form,
            "queryset": queryset,
        }
    return render(request, "list_item.html", context)


def list_item_user(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }
    
    if request.method == "POST" :
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                            item_name__icontains=form['item_name'].value()
                                            )
        context = {
            "form": form,
            "queryset": queryset,
        }
    return render(request, "list_item_user.html", context)


def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list_item')
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)


def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/list_item')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)


def delete_item(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		return redirect('/list_item')
	return render(request, 'delete_item.html')

