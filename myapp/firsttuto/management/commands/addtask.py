from django.core.management.base import BaseCommand,CommandError
from firsttuto.models import Task
from datetime import date

class Command(BaseCommand):
    help = "Add task to BD. Indicate the number of tasks you want to create."

    def add_arguments(self,parser):
        parser.add_argument("nb_task",nargs="+",type=int)
    
    def handle(self,*args,**options):
        today = date.today()
        for i in range(options["nb_task"][0]):
            task = Task(description="Task %d %s."% (i,today.strftime("%b-%d-%Y")))
            task.save()
        self.stdout.write(self.style.SUCCESS('Success!'))
