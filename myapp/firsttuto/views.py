from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from firsttuto.form import RegisterForm, TaskForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,FormView,ListView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from .models import Task
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(TemplateView):
    template_name = 'index.html'

class Login(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_invalid(self,form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        form.save() # save the user
        return super().form_valid(form)

def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div class="alert alert-danger mt-3" role="alert" id="username-error">This username is already used.</div>')
    else:
        return HttpResponse('<div class="alert alert-success mt-3" role="alert" id="username-error">This username is available.</div>')


class TaskList(LoginRequiredMixin,ListView):
    template_name = "task/tasks.html"
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()

class TaskListDB(LoginRequiredMixin,ListView):
    template_name = "task/tasks-db.html"
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.all().order_by('id')
    
def listing(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 5)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    tasks = paginator.get_page(page_number)
    return render(request, "task/tasks-db.html", {"tasks": tasks})

@login_required
def add_task(request):
    description = request.POST.get('taskdescription')
    task = Task.objects.create(description=description)
    request.user.tasks.add(task)
    tasks = request.user.tasks.all()
    return render(request,'task/task-list.html',{'tasks':tasks})

@login_required
def toggle_task_subscription(request, id):
    task = Task.objects.get(id=id)

    if request.user in task.users.all():
        task.users.remove(request.user)
        subscribed = False
    else:
        task.users.add(request.user)
        subscribed = True

    data = {
        'subscribed': subscribed,
        'num_users': task.users.count(),
        'usernames': [user.username for user in task.users.all()],
    }

    return redirect(reverse('db_tasks'))

def task_detail(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'task/task_detail.html', {'task': task})

def edit_task(request, id):
    task = Task.objects.get(id=id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('db_tasks'))
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/edit_task.html', {'form': form, 'task': task})

@login_required
@require_http_methods('DELETE')
def supp_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    tasks = request.user.tasks.all()
    return render(request, 'task/task-list.html', {'tasks':tasks})

@login_required
def search_task(request):
    search_text = request.POST.get('search')
    usertasks = request.user.tasks.all()
    results = Task.objects.filter(description__icontains=search_text).filter(description__in=usertasks.values_list('description', flat=True)[:10])
    # results = Task.objects.filter(description__icontains=search_text).exclude(description__in=usertasks.values_list('description', flat=True)[:10])

    context = {'results':results}
    return render(request, 'task/search-result.html', context)
