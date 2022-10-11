from pydoc import cli
from database import client

news_index = client.index('news')
#news_index.update_filterable_attributes(['tags',])

#client.create_index('employee_chat', {'primaryKey': 'id'})
employee_chat_index = client.index('employee_chat')
#news_index.update_filterable_attributes(['tags',])