import django_tables2 as tables
from trade_currency.models import TradeCurrency


class TradeCurrencyTable(tables.Table):
     
     BUTTON_TEMPLATE = """
       
        <a href="{% url 'trade_currency:edit_currency' record.pk %}" title="Edit" class="btn"><i class="fa fa-edit"></i></a>
      
     """
     Actions = tables.TemplateColumn(BUTTON_TEMPLATE,orderable=False )
     def render_counter(self, record):
      records = list(self.data)
      index = records.index(record)
      counter = index + 1
      return counter
     counter = tables.Column(verbose_name='S.No',orderable=False,accessor='pk',)
     class Meta:
         model =  TradeCurrency
         orderable = False
         attrs = {'class': 'table table-bordered table-striped','id':'example2'}
         fields=['counter','currncytype','name','symbol','status','Actions']




