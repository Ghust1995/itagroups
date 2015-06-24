from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse

from groups.models import Group, User

from groups.HelperMethods.functionalities import verification, search_groups


def home_page(request):

	# Home page post is adding new group
	if request.method == 'POST':

		# Writing less
		name = request.POST['group_name']
		alias = request.POST['group_alias']
		tags = request.POST['group_tags']
		description = request.POST['group_description']
	
		if verification(request, name, alias, tags):			
			return verification(request, name, alias, tags)

		group = Group()
		group.name = name
		group.alias = alias
		group.tags = tags
		group.description = description
		group.save()

		return render(request, 'home.html', {
			'group_success': True,
			'open_popup': True, 
			'group_name': group.name,
			'group_tags': group.tags,
			'group_alias': group.alias,
			'group_description': group.description
			})

	# Home page get is searching for groups
	if request.method == 'GET':
		search_tags = request.GET.get('search_group', '')
		if search_tags != '':
			found_groups = search_groups(search_tags)
			return render(request, 'home.html', {
				'groups': found_groups
				})

	return render(request, 'home.html')
	
def view_group(request, group_alias):
	found_groups = search_groups(group_alias)
	if found_groups:
		return render(request, 'view.html', {
			'group_name': found_groups[0].name
			})
	return redirect('/')

def verify_login(request):

	user = request.POST['username_input']

	response = redirect('/') if User.objects.filter(access_token = user) else redirect('/signup/')

	#Cookie username

	response.set_cookie('LOGSESSID', user)

	return response

def signup(request):
	
	if request.method == 'POST':

		# Writing less
		apelido = request.POST['apelido_input']
		turma = request.POST['turma_input']

		#Getting the cookie
		username = request.COOKIES['LOGSESSID']

		response = redirect('/')

		if User.objects.filter(access_token = username):
			response.set_cookie('LOGSESSID', username)

			return response

		user = User()
		user.access_token = username
		user.apelido = apelido
		user.turma = turma
		user.save()

		return response

	return render(request, 'signup.html')
