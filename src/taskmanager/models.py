from django.db import models

class Role(models.Model):
    class Meta:
        unique_together = (('role_team', 'access_level'),)

    role_team = models.CharField(max_length=100)
    access_level = models.IntegerField()
    
    def __str__(self):
        return self.role_team + " Level " + str(self.access_level)

class User(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.name + ": " + self.email

class List(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    can_read = models.IntegerField(null=True)
    can_claim = models.IntegerField(null=True)
    can_add = models.IntegerField(null=True)
    can_admin = models.IntegerField(null=True)
    team = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    claimants = models.ManyToManyField(User, related_name='claimed_tasks')
    title = models.CharField(max_length=10000)
    task_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=1000000000)
    priority = models.IntegerField()
    larger_goal = models.CharField(max_length=10000, null=True)
    estimate_end_date = models.DateField(null=True)

    def __str__(self):
        return self.title

class Note(models.Model):
    text = models.CharField(max_length=1000000000000)
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes')
    
    def __str__(self):
        return self.text
