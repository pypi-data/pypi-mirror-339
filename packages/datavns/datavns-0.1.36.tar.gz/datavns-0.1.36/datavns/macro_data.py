from .lib import *
from .headers import *
#####
class macro(headers_list):
    @classmethod
    def fx_rate(cls, symbol, start_date, end_date):
        start = int(pd.to_datetime(start_date, format='%Y-%m-%d').timestamp())
        end = int(pd.to_datetime(end_date, format='%Y-%m-%d').timestamp())
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}=X"
        #####
        params = {
            "period1": str(start),
            "period2": str(end),
            "interval": "1d",
            "includePrePost": "true",
            "events": "div|split|earn",
            "lang": "en-US",
            "region": "VN"
        }
        #####
        response = rq.get(url, headers=cls.yahoo_headers, params=params).json()
        try:
            index = response['chart']['result'][0]['timestamp']
            value = response['chart']['result'][0]['indicators']['quote'][0]
            adjvalue = response['chart']['result'][0]['indicators']['adjclose'][0]
            df = pd.DataFrame(value|adjvalue, index= index)
            df['date'] = df.index
            df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y%m%d')).astype(int)
            df = df.reset_index(drop=True)
            return df
        except:
            return response