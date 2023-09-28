from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField  # Import from ckeditor
from django.utils import timezone

def python_default():
    python_hashtag, created = Hashtag.objects.get_or_create(name="python")
    return [python_hashtag.id]

class Hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class CryptoAnalysis(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=False, default=python_default)
    content = RichTextField(null=True, blank=True)  # Dodaj to pole
    def __str__(self):
        return self.title

class Editorial(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True)
    content = RichTextField(null=True)  # Use RichTextField from ckeditor
    pub_date = models.DateTimeField('date published', default=timezone.now)
    hashtags = models.ManyToManyField(Hashtag, blank=False, default=python_default)


    def save(self, *args, **kwargs):
        if not self.slug:
            potential_slug = slugify(self.title)
            if Editorial.objects.filter(slug=potential_slug).exists():
                i = 1
                while Editorial.objects.filter(slug=potential_slug + '-' + str(i)).exists():
                    i += 1
                self.slug = potential_slug + '-' + str(i)
            else:
                self.slug = potential_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('editorial', args=[str(self.slug)])

    def __str__(self):
        return self.title



class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True)
    content = RichTextField(null=True)
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=False)
    main_article_position = models.PositiveIntegerField(null=True, blank=True, unique=True, choices=[(1, 'Main'), (2, 'Side 1'), (3, 'Side 2')])
    hashtags = models.ManyToManyField(Hashtag, blank=False, default=python_default)

    def save(self, *args, **kwargs):
        if not self.slug:
            potential_slug = slugify(self.title)
            if News.objects.filter(slug=potential_slug).exists():
                i = 1
                while News.objects.filter(slug=potential_slug + '-' + str(i)).exists():
                    i += 1
                self.slug = potential_slug + '-' + str(i)
            else:
                self.slug = potential_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news', args=[str(self.slug)])

    def __str__(self):
        return self.title

class PressRelease(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True)
    content = RichTextField(null=True)  # Use RichTextField from ckeditor
    hashtags = models.ManyToManyField(Hashtag, blank=False, default=python_default)

    def save(self, *args, **kwargs):
        if not self.slug:
            potential_slug = slugify(self.title)
            if PressRelease.objects.filter(slug=potential_slug).exists():
                i = 1
                while PressRelease.objects.filter(slug=potential_slug + '-' + str(i)).exists():
                    i += 1
                self.slug = potential_slug + '-' + str(i)
            else:
                self.slug = potential_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('press-release', args=[str(self.slug)])

    def __str__(self):
        return self.title

class NewestCourse(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = RichTextField(null=True)  # Use RichTextField to have a rich text editor for course descriptions
    hashtags = models.ManyToManyField(Hashtag, blank=False, default=python_default)

    def save(self, *args, **kwargs):
        if not self.slug:
            potential_slug = slugify(self.title)
            if NewestCourse.objects.filter(slug=potential_slug).exists():
                i = 1
                while NewestCourse.objects.filter(slug=potential_slug + '-' + str(i)).exists():
                    i += 1
                self.slug = potential_slug + '-' + str(i)
            else:
                self.slug = potential_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('newest_course', args=[str(self.slug)])

    def __str__(self):
        return self.title



class ProcessedLink(models.Model):
    link = models.URLField(unique=True)

