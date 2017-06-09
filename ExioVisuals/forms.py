
from ExioVisuals.models import Product, Selection, Selection2, Selection3, Selection4, Country, Substance, YearF
from django import forms
from ExioVisuals.widgets import FancyTreeWidget
from ExioVisuals.models import years
class modes(forms.Form):
    CHOICES=[('selectD','Country where impact occurs'),
          ('selectC','Sector where impact occurs')   ,('selectF', 'Region selling final product'),
    ('selectA','Consumed product category'),('selectB','Consuming region'),('selectE','Environmental pressure [not functional yet]')
    ]
    y = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(modes, self).__init__(*args, **kwargs)
        self.fields['y'].label = ":"
class modesGeo(forms.Form):
    CHOICES=[('selectD','Country where impact occurs')   ,('selectF', 'Region selling final product'),
             ('selectB','Consuming region')
    ]
    modeSelection = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(modesGeo, self).__init__(*args, **kwargs)
        self.fields['modeSelection'].label = ":"

#two supplychain modes as they should behave independently
class supplychainLeftMode(forms.Form):
    CHOICES=[('1','Region of emission'),
          ('2','Sector of emission')   ,('3', 'Region of supply'),
    ('4','Product or service'),('5','Region of consumption')
    ]
    left = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(supplychainLeftMode, self).__init__(*args, **kwargs)
        self.fields['left'].label = ":"
class supplychainRightMode(forms.Form):
    CHOICES=[('1','Region of emission'),
          ('2','Sector of emission')   ,('3', 'Region of supply'),
    ('4','Product or service'),('5','Region of consumption')
    ]
    right = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(supplychainRightMode, self).__init__(*args, **kwargs)
        self.fields['right'].label = ":"

class rightMode(forms.Form):
    CHOICES=[('selectD','Country where impact occurs'),
          ('selectC','Sector where impact occurs')   ,('selectF', 'Region selling final product'),
    ('selectA','Consumed product category'),('selectB','Consuming region'),('selectE','Environmental pressure [not functional yet]')
    ]
    y = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(modes, self).__init__(*args, **kwargs)
        self.fields['y'].label = ":"
        #below is the class for the case that a user selected the TimeSeries (it does not make sense to split on year as that is default)
class modesTimeSeries(forms.Form):
    CHOICES=[('selectD','Country where impact occurs'),
          ('selectC','Sector where impact occurs')   ,('selectF', 'Region selling final product'),
    ('selectA','Consumed product category'),('selectB','Consuming region'),('selectE','Environmental pressure [not functional yet]')
    ]

    y = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super(modesTimeSeries, self).__init__(*args, **kwargs)
        self.fields['y'].label = ":"
class yearsSingleSelect(forms.Form):

    p = []
    t = []
    absData = years.objects.all().values_list('years', flat=True)
    for x in absData:
        p.append(x+"#"+x)
    for x in p:
         t.append(x.split('#'))
    print(t)
    k = t

    Year = forms.ChoiceField(
                                         choices=k)
    def __init__(self, *args, **kwargs):
        super(yearsSingleSelect, self).__init__(*args, **kwargs)
        self.fields['Year'].label = ""

class yearsMultipleSelect(forms.Form):

    p = []
    t = []
    absData = years.objects.all().values_list('years', flat=True)
    for x in absData:
        p.append(x+"#"+x)
    for x in p:
         t.append(x.split('#'))
    print(t)
    OPTIONS = t

    Year = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':'10,10'}),
                                             choices=OPTIONS)
class PostFormEFactor(forms.Form):
    name = forms.CharField()
    grams = forms.FloatField()
    OPTIONS = (
            ("a", "Achoice"),
            ("b", "Bchoice"),
            )
    names = forms.MultipleChoiceField(
                                         choices=OPTIONS)
    OPTIONS2 = (
            ("a", "Achoice"),
            ("b", "Bchoice"),
            )
    names2 = forms.ChoiceField(
                                         choices=OPTIONS2)



    CHOICES=[('select1','select 1'),('select2','select 2')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class reloadForm(forms.Form):
    CHOICES=[('select1','mode 1'),('select2','mode 2')]

    selection = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

products = Product.objects.order_by('tree_id', 'lft')
countries = Country.objects.order_by('tree_id', 'lft')
substances = Substance.objects.order_by('tree_id', 'lft')
yearF = YearF.objects.order_by('tree_id', 'lft')


class ProductSelectionForm(forms.ModelForm):
    class Meta:
        model = Selection
        fields = ( 'products',)
        widgets = {
            'products': FancyTreeWidget(queryset=products)
        }

class CountrySelectionForm(forms.ModelForm):
    class Meta:
        model = Selection2
        fields = ( 'countries',)
        widgets = {
            'countries': FancyTreeWidget(queryset=countries)
        }

class SubstanceSelectionForm(forms.ModelForm):
    class Meta:
        model = Selection3
        fields = ( 'substances',)
        widgets = {
            'substances': FancyTreeWidget(queryset=substances)
        }
class YearFSelectionForm(forms.ModelForm):
    class Meta:
        model = Selection4
        fields = ( 'yearF',)
        widgets = {
            'yearF': FancyTreeWidget(queryset=yearF)
        }