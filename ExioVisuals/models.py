from djgeojson.fields import PointField
from django.db import models
from djgeojson.fields import PolygonField
from mptt.models import MPTTModel, TreeForeignKey


# models.py
from djgeojson.fields import PointField
from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urljoin

from django.db import models
from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
import mptt

#from urlparse import urljoin

#make structure of ghgEmission database tables
class GhgEmissions(models.Model):
     #has a countryname
    label = models.CharField(max_length=128, unique=True)
    #has a countrycode
    code = models.CharField(max_length=128, unique=True)
    #has a absolute value
    absolute = models.FloatField()



    #mandatory
    def __unicode__(self):
        return self.label

class years(models.Model):
     #has a countryname
    years = models.CharField(max_length=128, unique=True)

    #mandatory
    def __unicode__(self):
        return self.years



class Product(models.Model):
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='children')

    name = models.CharField(max_length=200)
    local = models.CharField(max_length=200, default="none")
    lvl = models.CharField(max_length=200, default="none")
    slug = models.CharField(max_length=100)
    url = models.TextField(editable=False)
    lwst_level = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "FancyTreeProduct"
        unique_together = (("name", "slug", "parent"), )
        ordering = ("tree_id", "lft")

    def __str__(self):
        return self.url

    def save(self, force_insert=False, force_update=False, **kwargs):
        super(Product, self).save(
            force_insert=force_insert,
            force_update=force_update,
            **kwargs)
        self.update_url()

    def get_tree(self, *args):
        """
        Return the tree structure for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level
        return _tree_structure
    get_tree.short_description = 'tree'

    def get_repr(self, *args):
        """
        Return the branch representation for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level + ' ' + self.name
        return _tree_structure
    get_repr.short_description = 'representation'

    def tree_order(self):
        return str(self.tree_id) + str(self.lft)

    def update_url(self):
        """
        Updates the url for this Product and all children Categories.
        """
        url = urljoin(getattr(self.parent, 'url', '') + '/', self.slug)
        if url != self.url:
            self.url = url
            self.save()

            for child in self.get_children():
                child.update_url()



class Country(models.Model):
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='children')

    name = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    lvl = models.CharField(max_length=200)

    slug = models.CharField(max_length=100)
    url = models.TextField(editable=False)
    lwst_level = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "FancyTreeCountry"
        unique_together = (("name", "slug", "parent"), )
        ordering = ("tree_id", "lft")

    def __str__(self):
        return self.url

    def save(self, force_insert=False, force_update=False, **kwargs):
        super(Country, self).save(
            force_insert=force_insert,
            force_update=force_update,
            **kwargs)
        self.update_url()

    def get_tree(self, *args):
        """
        Return the tree structure for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level
        return _tree_structure
    get_tree.short_description = 'tree'

    def get_repr(self, *args):
        """
        Return the branch representation for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level + ' ' + self.name
        return _tree_structure
    get_repr.short_description = 'representation'

    def tree_order(self):
        return str(self.tree_id) + str(self.lft)

    def update_url(self):
        """
        Updates the url for this Country and all children Categories.
        """
        url = urljoin(getattr(self.parent, 'url', '') + '/', self.slug)
        if url != self.url:
            self.url = url
            self.save()

            for child in self.get_children():
                child.update_url()


class Substance(models.Model):
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='children')

    name = models.CharField(max_length=200)

    slug = models.CharField(max_length=100)
    url = models.TextField(editable=False)


    class Meta:
        verbose_name_plural = "FancyTreeSubstance"
        unique_together = (("name", "slug", "parent"), )
        ordering = ("tree_id", "lft")

    def __str__(self):
        return self.url

    def save(self, force_insert=False, force_update=False, **kwargs):
        super(Substance, self).save(
            force_insert=force_insert,
            force_update=force_update,
            **kwargs)
        self.update_url()

    def get_tree(self, *args):
        """
        Return the tree structure for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level
        return _tree_structure
    get_tree.short_description = 'tree'

    def get_repr(self, *args):
        """
        Return the branch representation for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level + ' ' + self.name
        return _tree_structure
    get_repr.short_description = 'representation'

    def tree_order(self):
        return str(self.tree_id) + str(self.lft)

    def update_url(self):
        """
        Updates the url for this Country and all children Categories.
        """
        url = urljoin(getattr(self.parent, 'url', '') + '/', self.slug)
        if url != self.url:
            self.url = url
            self.save()

            for child in self.get_children():
                child.update_url()
class YearF(models.Model):
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='children')

    name = models.CharField(max_length=200)

    slug = models.CharField(max_length=100)
    url = models.TextField(editable=False)


    class Meta:
        verbose_name_plural = "FancyTreeYearF"
        unique_together = (("name", "slug", "parent"), )
        ordering = ("tree_id", "lft")

    def __str__(self):
        return self.url

    def save(self, force_insert=False, force_update=False, **kwargs):
        super(YearF, self).save(
            force_insert=force_insert,
            force_update=force_update,
            **kwargs)
        self.update_url()

    def get_tree(self, *args):
        """
        Return the tree structure for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level
        return _tree_structure
    get_tree.short_description = 'tree'

    def get_repr(self, *args):
        """
        Return the branch representation for this element
        """
        level_representation = "--"
        if self.level == 0:
            node = "| "
        else:
            node = "+ "
        _tree_structure = node + level_representation * self.level + ' ' + self.name
        return _tree_structure
    get_repr.short_description = 'representation'

    def tree_order(self):
        return str(self.tree_id) + str(self.lft)

    def update_url(self):
        """
        Updates the url for this Country and all children Categories.
        """
        url = urljoin(getattr(self.parent, 'url', '') + '/', self.slug)
        if url != self.url:
            self.url = url
            self.save()

            for child in self.get_children():
                child.update_url()

mptt.register(Product, order_insertion_by=['name'])
mptt.register(Country, order_insertion_by=['name'])
mptt.register(Substance, order_insertion_by=['name'])
mptt.register(YearF, order_insertion_by=['name'])


class Selection (models.Model):
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('selection', args=[self.pk])


class Selection2 (models.Model):
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('selection', args=[self.pk])

class Selection3 (models.Model):
    substances = models.ManyToManyField(Substance)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('selection', args=[self.pk])
class Selection4 (models.Model):
    yearF = models.ManyToManyField(YearF)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('selection', args=[self.pk])