from __future__ import unicode_literals
from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from django.contrib.auth.models import User
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel,StreamFieldPanel
from taggit.models import TaggedItemBase
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.tags import ClusterTaggableManager
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.fields import StreamField
class HomePage(Page):
    #set a custom context for the usage as template tags in the html
    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        #get the user profiles (only for the groups of moderators)
        users = User.objects.filter(groups__name='Editors')
        if request.user.is_authenticated():
            username = request.user.username
            # special for cml researcher to get info to be used later
            context.update({'username': username})
        listOfUsers = []
        listOfProfiles = []
        for user in users:
            listOfUsers.append(user.username)
            listOfProfiles.append(user.profile.topics)

        context['listOfUsers'] = zip(listOfUsers, listOfProfiles)
        return context
    research = RichTextField(blank=True)
    blog = RichTextField(blank=True)
    tools_dbs = RichTextField(blank=True)
    IV_CML =\
        RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('research', classname="full"),FieldPanel('blog', classname="full"),
        FieldPanel('tools_dbs', classname="full"),FieldPanel('IV_CML', classname="full"),
    ]

class BlogIndexPage(Page):
    #set a custom context for the usage as template tags in the html
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        if request.user.is_authenticated():
            username = request.user.username
            # special for cml researcher to get info to be used later
            context.update({'username': username})
        return context

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')
class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        if request.user.is_authenticated():
            username = request.user.username
            # special for cml researcher to get info to be used later
            context.update({'username': username})
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        #get the user profiles (only for the groups of moderators)
        if request.user.is_authenticated():
            username = request.user.username
            # special for cml researcher to get info to be used later
            context.update({'username': username})
        return context

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class ToolsDbsIndexPage(Page):
    #set a custom context for the usage as template tags in the html
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(ToolsDbsIndexPage, self).get_context(request)
        toolsdbspages = self.get_children().live().order_by('-first_published_at')
        context['toolsdbspages'] = toolsdbspages
        if request.user.is_authenticated():
            username = request.user.username
            # special for cml researcher to get info to be used later
            context.update({'username': username})
        return context

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ToolsDbsPage(Page):
    def get_context(self, request):
        context = super(ToolsDbsPage, self).get_context(request)
        # get the user profiles (only for the groups of moderators)
        if request.user.is_authenticated():
            username = request.user.username
            # special for cml researcher to get info to be used later
            context.update({'username': username})
        return context

    content = StreamField([
        ('table', TableBlock()),
    ])

    search_fields = Page.search_fields
    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]

