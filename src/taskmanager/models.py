from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=100, primary_key=True)
    controllingRole = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.role_name

class User(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.name + ": " + self.email

class List(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    can_read = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='viewable_lists')
    can_claim = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='claimable_lists')
    can_add = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='addable_lists')
    
    def __str__(self):
        return self.name

class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    claimants = models.ManyToManyField(User, related_name='claimed_tasks')
    title = models.CharField(max_length=10000)
    task_list = models.ForeignKey(List, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000000000)
    priority = models.IntegerField()
    larger_goal = models.CharField(max_length=10000, null=True)
    estimate_end_date = models.DateField()
    #WIP OTHER DATA

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000000000000)
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title