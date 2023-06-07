from django.db import models
from users.models import Profile
import uuid


class Project(models.Model):
    owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    img_file = models.ImageField(blank = True, null = True, default= "default.jpg")
    demo_link = models.CharField(max_length=1000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    vote_total = models.IntegerField(default=0, blank=True, null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    tcreated = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def ImgURL(self):
        try:
            url = self.img_file.url
        except:
            url = 'default.jpg'
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner_id', flat=True)
        return queryset
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):
    VOTE_CU = (
        ('up', 'vote up'),
        ('down', 'vote down'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=200, choices=VOTE_CU)
    tcreated = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]


class Tag(models.Model):
    name = models.CharField(max_length=200)
    tcreated = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.name