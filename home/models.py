import django
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from datetime import date, datetime

from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, \
    StreamFieldPanel, MultiFieldPanel, InlinePanel

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from .blocks import InlineVideoBlock, ImageTextBlock, ImageTextArticleBlock


# Start of Website page models
class HomePage(Page):
    """Home page model."""

    template = "home/home_page.html"
    max_count = 1

    banner_title = models.CharField(
        max_length=100, blank=False, null=True
    )
    banner_subtitle = RichTextField()
    intro = StreamField(
        [
            ("video", InlineVideoBlock()),
        ],
        null=True,
        blank=True,
    )
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
    store_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    store_text = RichTextField(
        max_length=100,
        blank=True,
        null=True
    )
    store_link = models.CharField(
        max_length=100, blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        StreamFieldPanel("intro"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("banner_cta"),
        MultiFieldPanel([ImageChooserPanel('store_image'),
                         FieldPanel('store_text'),
                         FieldPanel('store_link')],
                        heading="Store Block"
                        ),
    ]

    class Meta:
        """Meta class."""

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


class TheClub(Page):
    """The club page model."""

    template = "club/the_club.html"
    max_count = 1

    about = StreamField(
        [
            ("about", ImageTextArticleBlock()),
        ],
        null=True,
        blank=True,
    )
    videos = StreamField(
        [
            ("video", InlineVideoBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("about"),
        StreamFieldPanel("videos"),
    ]

    class Meta:
        """Meta class."""

        verbose_name = "The Club Page"
        verbose_name_plural = "The Club Pages"


class Scorecard(Page):
    """Scorecard page model."""

    template = "club/scorecard.html"
    max_count = 1

    banner_title = models.CharField(
        max_length=100, blank=True, default=''
    )
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
    ]

    class Meta:
        """Meta class."""

        verbose_name = "Scorecard Page"
        verbose_name_plural = "Scorecard Pages"


class FixturePreview(Page):
    """Fixture Preview page model."""

    template = "club/fixture_preview.html"
    max_count = 1

    banner_title = models.CharField(
        max_length=100, blank=True, default=''
    )
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
    ]

    class Meta:
        """Meta class."""

        verbose_name = "Fixture Preview Page"
        verbose_name_plural = "Fixture Preview Pages"


class Overview(Page):
    """Overview page model."""

    template = "club/overview.html"
    max_count = 1

    banner_title = models.CharField(
        max_length=100, blank=True, default=''
    )
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
    ]

    class Meta:
        """Meta class."""

        verbose_name = "Overview Page"
        verbose_name_plural = "Overview Pages"


class BlogIndexPage(Page):
    """Main page that holds the blog on."""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPage.objects.live().public() \
            .order_by(
            '-first_published_at'
        )
        date_sorted_posts = sorted(
            all_posts, key=lambda p: p.specific.date, reverse=True
        )
        # Paginate all posts by 5 per page
        paginator = Paginator(date_sorted_posts, 5)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        return context


class BlogPage(Page):
    """Individual blog page creation through adding child page."""

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel('date'),
                         FieldPanel('intro'),
                         FieldPanel('body', classname="full")],
                        heading="blogpage Options"
                        ),

        MultiFieldPanel(
            [
                InlinePanel(
                    'blogpage_images', max_num=30, min_num=0, label="blogpage images"
                )
            ],
            heading="blogpage Images"
        ),
    ]


class BlogPageGalleryImage(Orderable):
    """Orderable images for blog."""

    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name='blogpage_images'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


# Start of Club database
class Profile(models.Model):
    """Add new fields to user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website_link = models.CharField(max_length=100)

    class Meta:
        """Meta class."""

    def __str__(self):
        return str(self.user)


class Team(models.Model):
    """Range of age levels at standards of cricket clubs."""

    name = models.CharField(max_length=20, default='')
    abr = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return self.name


class Role(models.Model):
    """Roles available at the lub like player or captain."""

    name = models.CharField(max_length=20, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return self.name


class Venue(models.Model):
    """Home away or neutral grounds are possible."""

    name = models.CharField(max_length=20, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return self.name


class OppositionNames(models.Model):
    """Opposition names Table."""

    name = models.CharField(max_length=30, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return self.name


class Type(models.Model):
    """Type of cricket players available."""

    name = models.CharField(max_length=20, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return str(self.name)


class Member(models.Model):
    """Make a member of a team."""

    ards = models.BooleanField(null=True, blank=True)
    player_link = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True,
        null=True, default=''
    )
    name = models.CharField(max_length=40, default='')
    dateOfBirth = models.DateField(blank=True, null=True)
    role = models.ManyToManyField(Role)
    type = models.ManyToManyField(Type)
    teamsPlayedFor = models.ManyToManyField(Team)
    dateJoined = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=15, default='')
    profile_pic = models.ImageField(
        default="default profile pic1.png", null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Cup(models.Model):
    """Available types of cups."""

    name = models.CharField(max_length=30, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return str(self.name)


class Award(models.Model):
    """Exact award given out."""

    type = models.ForeignKey(Cup, on_delete=models.CASCADE, default='')
    year = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1950)]
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default='')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default='')

    class Meta:
        """Meta class."""

        unique_together = (("type", "team", "year"),)

    def __str__(self):
        return str('{0} {1} {2}'.format(
            self.member, self.type, self.year)
        )


class MatchFormat(models.Model):
    """Range from t20 to 35 over game."""

    name = models.CharField(max_length=20, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return self.name


class CoinToss(models.Model):
    """How did ards do in the toss."""

    decision = models.CharField(blank=True, default='', max_length=40)

    class Meta:
        """Meta class."""

        unique_together = (("decision",),)

    def __str__(self):
        return str('{0}'.format(self.decision))


class Wicket(models.Model):
    """Types of wickets that can happen."""

    name = models.CharField(max_length=20, default='')

    class Meta:
        """Meta class."""

        unique_together = (("name",),)

    def __str__(self):
        return str(self.name)


class Club(models.Model):
    """Holds club information."""

    name = models.CharField(max_length=30, default='')
    badge = models.ImageField(
        default="original_images/default_logo.png", null=True, blank=True
    )
    home_venue = models.CharField(max_length=40, default='', null=True, blank=True)

    class Meta:
        """Meta class."""

        unique_together = (("name", "home_venue"),)

    def __str__(self):
        return str(self.name)


class Match(models.Model):
    """Specific to match information."""

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, default='')
    match_format = models.ForeignKey(
        MatchFormat, on_delete=models.SET_NULL, null=True, default=''
    )
    opponent = models.ForeignKey(
        Club, on_delete=models.SET_NULL, null=True, default=''
    )
    date = models.DateField(blank=True, null=True, default=django.utils.timezone.now)
    time = models.TimeField(blank=True, null=True, default=django.utils.timezone.now)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, default='')
    decision = models.ForeignKey(
        CoinToss, on_delete=models.SET_NULL,
        blank=True,
        null=True, default=''
    )
    ards_overs_batted = models.DecimalField(
        blank=True, null=True, decimal_places=1, max_digits=4, default=0
    )
    ards_runs = models.IntegerField(blank=True, null=True, default=0)
    ards_wickets = models.IntegerField(blank=True, null=True, default=0)
    opponent_overs_batted = models.DecimalField(
        blank=True, null=True, decimal_places=1, max_digits=4, default=0
    )
    opponent_runs = models.IntegerField(blank=True, null=True, default=0)
    opponent_wickets = models.IntegerField(
        blank=True, null=True, default=0,
    )
    report = models.TextField(
        max_length=600, default='', null=True, blank=True
    )

    class Meta:
        """Meta class."""

        unique_together = (("team", "date", "opponent"),)

    def __str__(self):
        if self.ards_runs > self.opponent_runs:
            runs_diff = self.ards_runs - self.opponent_runs
            result = "Ards won"
            return str('{0} on {1} {2} by {3} against {4}'.format(
                self.team, self.date.strftime("%d %B %Y"), result,
                runs_diff, self.opponent)
            )
        elif self.ards_runs == self.opponent_runs:
            result = "Match drawn"
            return str('{0} on {1} {2} against {3}'.format(
                self.team, self.date.strftime("%d %B %Y"), result, self.opponent)
            )
        else:
            runs_diff = self.opponent_runs - self.ards_runs
            result = "Ards lost"
            return str('{0} on {1} {2} by {3} against {4}'.format(
                self.team, self.date.strftime("%d %B %Y"), result,
                runs_diff, self.opponent)
            )

    def result(self):
        """Return result string."""
        if self.ards_runs > self.opponent_runs:  # skipcq: PYL-W0622
            runs_diff = self.ards_runs - self.opponent_runs
            result = "Ards won"
            return str('{0} by {1} runs'.format(result, runs_diff))
        elif self.ards_runs == self.opponent_runs:  # skipcq: PYL-W0622
            result = "Match drawn"
            return str('{0}'.format(result))
        else:
            runs_diff = self.opponent_runs - self.ards_runs
            result = "Ards lost"
            return str('{0} by {1} runs'.format(result, runs_diff))

    def banter(self):
        """Difference in runs."""
        runs_diff = self.ards_runs - self.opponent_runs
        return str('{0}').format(runs_diff)

    def ards_score(self):
        """Output the ards score."""
        if self.ards_wickets == 10:
            var1 = "All Out"
            return str('{0} {1}').format(self.ards_runs, var1)
        else:
            var1 = self.ards_wickets
            return str('{0}-{1}').format(self.ards_runs, var1)

    def opponents_score(self):
        """Output the opponents score."""
        if self.opponent_wickets == 10:
            var1 = " All Out"
            return str('{0} {1}').format(self.opponent_runs, var1)
        else:
            var1 = self.ards_wickets
            return str('{0}-{1}').format(self.opponent_runs, var1)

    def location(self):
        var1 = ''
        if self.venue.name == "Home":
            var1 = "Londonderry Park,  Newtownards"
        elif self.venue.name == 'Away':
            var1 = self.opponent.home_venue
        return str('{0}').format(var1)

    def team_v_team(self):
        var1 = ''
        if self.venue.name == "Home":
            var1 = "Ards v " + self.opponent.name
        elif self.venue.name == 'Away':
            var1 = self.opponent.name + " v Ards"
        return str('{0}').format(var1)


class Extras(models.Model):
    """Extras that were bowled by each team in a match."""

    ards = models.BooleanField(blank=True, null=True)
    wides = models.IntegerField(blank=True, null=True)
    no_balls = models.IntegerField(blank=True, null=True)
    byes = models.IntegerField(blank=True, null=True)
    leg_byes = models.IntegerField(blank=True, null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')

    class Meta:
        """Meta class."""

        unique_together = (("ards", "match",),)

    def __str__(self):
        return str('{0}w, {1}b, {2}lb, {3}nb'
                   .format(self.wides, self.byes, self.leg_byes, self.leg_byes)
                   )

    def extras_total(self):
        """Output the total extras."""
        total = self.wides + self.no_balls + self.byes + self.leg_byes
        return total


class Batting(models.Model):
    """Batting performances within a match."""

    member = models.ForeignKey(Member, on_delete=models.CASCADE, default='')
    batter_number = models.IntegerField(
        blank=False, default=1, validators=[MaxValueValidator(11), MinValueValidator(1)]
    )
    fours = models.IntegerField(blank=True, null=True, default=0)
    sixes = models.IntegerField(blank=True, null=True, default=0)
    runs = models.IntegerField(blank=True, null=True, default=0)
    mode_of_dismissal = models.ForeignKey(Wicket, on_delete=models.CASCADE, default='')
    out_by = models.ForeignKey(
        OppositionNames, on_delete=models.CASCADE, default='', blank=True, null=True
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')

    class Meta:
        """Meta class."""

        unique_together = (("batter_number", "match",),)

    def __str__(self):
        return str('{0} {1} scored {2} runs'
                   .format(self.member, self.match.date, self.runs)
                   )


class Bowling(models.Model):
    """Bowling performances within a match."""

    ards = models.BooleanField(blank=True, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default='')
    bowler_number = models.IntegerField(
        blank=False, default=1, validators=[MaxValueValidator(11), MinValueValidator(1)]
    )
    overs = models.IntegerField(blank=True, null=True, default=0)
    runs = models.IntegerField(blank=True, null=True, default=0)
    maidens = models.IntegerField(blank=True, null=True, default=0)
    wickets = models.IntegerField(blank=True, null=True, default=0)
    wides = models.IntegerField(blank=True, null=True, default=0)
    no_balls = models.IntegerField(blank=True, null=True, default=0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')

    class Meta:
        """Meta class."""

        unique_together = (("ards", "bowler_number", "match",),)

    def __str__(self):
        return str('{0} {1}, figures of {2}-{3}-{4}'
                   .format(self.member, self.match.date, self.overs,
                           self.runs, self.wickets))

    def bowler_extras(self):
        """Output the bowlers extras."""
        extras = self.wides + self.no_balls
        return str('{0}'.format(extras))

    def economy(self):
        """Workout the economy."""
        econ = float(self.runs) / float(self.overs)
        return format(econ, '.2f')


class BattingOpponents(models.Model):
    """Batting performances within a match."""

    batter_name = models.ForeignKey(
        OppositionNames, on_delete=models.CASCADE, default='', blank=True, null=True
    )
    batter_number = models.IntegerField(
        blank=True, null=True, validators=[MaxValueValidator(11), MinValueValidator(1)]
    )
    runs = models.IntegerField(blank=True, null=True, default=0)
    mode_of_dismissal = models.ForeignKey(
        Wicket, on_delete=models.CASCADE, default=''
    )
    out_by = models.ForeignKey(Member, on_delete=models.CASCADE, default='')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')

    class Meta:
        """Meta class."""

        unique_together = (("batter_number", "match",),)

    def __str__(self):
        return str('{0} {1} scored {2} runs'.format(
            self.batter_name, self.match.date, self.runs)
        )


class BowlingOpponents(models.Model):
    """Bowling performances within a match."""

    bowler_name = models.ForeignKey(
        OppositionNames, on_delete=models.CASCADE, default=''
    )
    bowler_number = models.IntegerField(
        blank=True, null=True, validators=[MaxValueValidator(11), MinValueValidator(1)]
    )
    overs = models.IntegerField(blank=True, null=True, default=0)
    runs = models.IntegerField(blank=True, null=True, default=0)
    wickets = models.IntegerField(blank=True, null=True, default=0)
    wides = models.IntegerField(blank=True, null=True, default=0)
    no_balls = models.IntegerField(blank=True, null=True, default=0)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')

    class Meta:
        """Meta class."""

        unique_together = (("bowler_number", "match",),)

    def __str__(self):
        return str('{0} {1}, figures of {2}-{3}-{4}'.format(
            self.bowler_name, self.match.date, self.overs, self.runs, self.wickets)
        )

    def bowler_extras(self):
        """Bowlers extras output."""
        extras = self.wides + self.no_balls
        return str('{0}'.format(extras))

    # got to add extras in with this
    def economy(self):
        """Workout the economy."""
        econ = float(self.runs) / float(self.overs)
        return format(econ, '.2f')

# End of Club database
