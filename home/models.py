from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    """Home page model"""

    template = "home/home_page.html"
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField()
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("banner_cta"),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


# Start of Club database

class Team(models.Model):
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.name)


class Member(models.Model):
    name = models.CharField(max_length=40, default='')
    dateOfBirth = models.DateField(blank=True, null=True)
    role = models.ManyToManyField(Role)
    type = models.ManyToManyField(Type)
    teamsPlayedFor = models.ManyToManyField(Team)
    dateJoined = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=15, default='')
    profile_pic = models.ImageField(default="default profile pic1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Cup(models.Model):
    name = models.CharField(max_length=30, default='')

    def __str__(self):
        return str(self.name)


class Award(models.Model):
    type = models.ForeignKey(Cup, on_delete=models.CASCADE)
    year = models.IntegerField(blank=True, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return str('{0} {1} {2},'.format(self.member, self.type, self.year))


class Wicket(models.Model):
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.name)


class Opponent(models.Model):
    name = models.CharField(max_length=30, default='')

    def __str__(self):
        return str(self.name)


class Batting(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    opponent = models.ManyToManyField(Opponent)
    date = models.DateField(blank=True, null=True)
    fours = models.IntegerField(blank=True, null=True)
    sixes = models.IntegerField(blank=True, null=True)
    runs = models.IntegerField(blank=True, null=True)
    out = models.ManyToManyField(Wicket)

    def __str__(self):
        return str('Member={0}, Date={1}'.format(self.member, self.date))


class Bowling(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    opponent = models.ManyToManyField(Opponent)
    date = models.DateField(blank=True, null=True)
    overs = models.IntegerField(blank=True, null=True)
    runs = models.IntegerField(blank=True, null=True)
    wickets = models.IntegerField(blank=True, null=True)
    extras = models.CharField(max_length=20, default='')

    def __str__(self):
        return str('Member={0}, Date={1}'.format(self.member, self.date))

# End of Club database
