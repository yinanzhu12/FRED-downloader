#%%
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from json import loads
import pandas as pd
#%%
# source code
class fred:
    def __init__(self,
                 key='0e661dd72c588efd3a141e6e37f47bac',
                 information=['frequency','id',
                              'observation_start','observation_end','title'],
                ):
        self.api_key=key
        self.information=information
        self.recent_search=[]
        
    def fetch(self,url):
        req = Request(url)
        p = urlopen(req)
        result = p.read().decode('utf-8')
        p.close()
        return result
    
    def search(self,search_text,limit=10,order='search_rank'):
        params={
            'api_key':self.api_key,
            'search_text':search_text,
            'file_type':'json',
            'limit':limit,
            'order_by':order
        }
        url = 'https://api.stlouisfed.org/fred/series/search?'+urlencode(params)
        result = loads(self.fetch(url))
        self.recent_search=pd.DataFrame(result['seriess']).loc[:,self.information]
        return self.recent_search
    
    def download(self,series_id,start='1776-07-04',end='9999-12-31',freq=None,agg='avg'):
        params={
            'api_key':self.api_key,
            'series_id':series_id,
            'observation_start':start,
            'observation_end':end,
            'file_type':'json',
        }
        if freq!=None:
            params['frequency']=freq
            params['aggregation_method']=agg
        url = 'https://api.stlouisfed.org/fred/series/observations?'+urlencode(params)
        result = loads(self.fetch(url))
        return pd.DataFrame(result['observations']).loc[:,['date','value']]
    
    def download_recent(self,index,start='1776-07-04',end='9999-12-31',freq=None,agg='avg'):
        if len(self.recent_search)==0:
            print("You haven't searched anything")
            return
        if len(self.recent_search)<=index:
            print("Requested series doesn't exist")
            return
        series_id=self.recent_search.loc[index,'id']
        return self.download(series_id,start,end,freq,agg)
#%%
# Demonstration

# create an object

# Arguments:

#    api_key: optional, the key used to access the FRED online service

#    information: list of string, optional, the information to show in search result, 
#                 default ['frequency','id','observation_start','observation_end','title']
#                 for possible options of information, see https://research.stlouisfed.org/docs/api/fred/series_search.html#examples
f=fred()
#%%
# search data base with key words through https://research.stlouisfed.org/docs/api/fred/series_search.html

# Arguments:
#    word: string, required, for search

#    limit: integer, optional, number of search results shown, default:10

#    order: string, optional, the order by which the search results are arranged
#           default: 'search_rank'
#           option of order, see https://research.stlouisfed.org/docs/api/fred/series_search.html#order_by

# Return: a pandas dataframe listing the top results
f.search('GDP')
f.search('GDP',limit=5,order='series_id')
#%%
# donwload data using id through https://research.stlouisfed.org/docs/api/fred/series_observations.html, no previous search is required

# Arguments:
#    series_id:string, required, the id of desired data

#    start:  YYYY-MM-DD format time, optional, the time where the data start, default '1776-07-04'

#    end:  YYYY-MM-DD format time, optional, the time where the data ends, default '9999-12-31'

#    freq: optional, the frequency of data, if specified, must be lower than
#          the original data's frequency, default: None
#          for option of freq, see https://research.stlouisfed.org/docs/api/fred/series_observations.html#frequency

#    agg: optional, if freq is specified, agg is the aggregation method used to turn original data 
#         into the frequency specified by user, default: 'avg' (average)
#         for option of agg, see https://research.stlouisfed.org/docs/api/fred/series_observations.html#aggregation_method

# Return: a pandas dataframe of the requested series
f.download('GDPC1',freq='a',agg='eop')
f.download('GDPCA',start='1990-01-01',end='2005-01-01')
#%%
# donwload from the most recent search result by index

# Arguments:
#    index: integer,required, the index of desired data in the most recent search result

#    start,end,freq,agg: same to those in fred.download()

# Return: a pandas dataframe of the requested series
f.download_recent(4,start='2000-01-01',freq='a',agg='eop')
#%%
# if no search have been done or the requested label outbounds the search result, warning
# message will be returned
f.download_recent(100)
#%%
g=fred()
g.download_recent(1)
