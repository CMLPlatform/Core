from django.contrib import admin
# Import the UserProfile model individually.

# Import the UserProfile model with Category and Page.
# If you choose this option, you'll want to modify the import statement you've already got to include UserProfile.
from ExioVisuals.models import  GhgEmissions
# admin.py
from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from ExioVisuals.models import Product, Country, years, Substance,YearF
#register the GHG emission table so we can see it in the administration

admin.site.register(GhgEmissions)


class ProductAdminOption(admin.ModelAdmin):
    list_display = ("get_repr", "get_tree")
    ordering = ("url",)
    search_fields = ('name', )


class CountryAdminOption(admin.ModelAdmin):
    list_display = ("get_repr", "get_tree")
    ordering = ("url",)
    search_fields = ('name', )


class SubstanceAdminOption(admin.ModelAdmin):
    list_display = ("get_repr", "get_tree")
    ordering = ("url",)
    search_fields = ('name', )

class YearsAdminOption(admin.ModelAdmin):
    list_display = ("get_repr", "get_tree")
    ordering = ("url",)
    search_fields = ('name', )



admin.site.register(Product, ProductAdminOption)
admin.site.register(Country, CountryAdminOption)
admin.site.register(Substance, SubstanceAdminOption)
admin.site.register(years)
admin.site.register(YearF, YearsAdminOption)