from .lib import *
from .headers import *
##########

def set_backtest_filepath(path = r'D:\Python\datavns\Data') -> str:
    '''
    Chỉ định đường dẫn đến thư mục lưu dữ liệu phục vụ backtest
    -----

        Parameter:
        -----
        `path (str)`: đường dẫn đến thư mục lưu dữ liệu phục vụ backtest

    '''
    path = input('Nhập vào đường dẫn đến thư mục lưu dữ liệu phục vụ backtest:')
    if path == '':
        return r'D:\Python\datavns\Data'
    else:
        return path


class stock(headers_list):
    @classmethod
    def infor(cls,stock) -> pd.DataFrame:
        '''
        In ra dữ liệu về thông tin của các cổ phiếu niêm yết trên sàn chứng khoán tại Việt Nam
        -----

            Parameter:
            -----
            `stock (str)`: Mã cổ phiếu niêm yết

            Return:
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:
                Các khoản mục của thông tin tương ứng là columns của DataFrame
                    Eg: Để xem các khoản mục có thể thực hiện
                        `infor('HPG').columns`
        '''
        #PART 1
        try:
            url = f'https://restv2.fireant.vn/symbols/{stock}/fundamental'
            df_raw = rq.get(url,headers=cls.fireant_header).json()
            df = pd.DataFrame(df_raw,index=[0])
            df['symbol'] = stock
            #PART 2
            url = f"https://iboard-api.ssi.com.vn/statistics/company/company-profile?symbol={stock}&language=vn"
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb"
            }
            response = rq.get(url, headers=headers, verify=False).json()
            data = response['data']
            data = pd.DataFrame(data, index = [0])

            df = pd.merge(df,data,how='outer',on='symbol')
        except:
            pass
        return df
    
    @classmethod
    def historical_dividends(cls, stock = 'VCB', num = 50) -> pd.DataFrame:
        '''
        In ra dữ liệu về chi trả cổ tức của các doanh nghiệp
        -----

            Parameter:
            -----
            `stock (str)`: Mã cổ phiếu niêm yết
            `num (int)`: Số năm lấy dữ liệu chi trả cổ tức, tính ngược từ thời điểm hiện tại

            Return:
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:
                Năm thực hiện: year
                Cổ tức tiền mặt: cashDividend
                Cổ tức cổ phiếu: stockDividend
                Tổng tài sản doanh nghiệp tại thời điểm chi trả: totalAssets
                Tổng vốn chủ sở hữu tại thời điểm chi trả: stockHolderEquity
        '''
        url_ = 'https://restv2.fireant.vn/symbols/{}/dividends?count={}'.format(stock,num)
        df_raw = rq.get(url=url_,headers=cls.fireant_header).json()
        return pd.DataFrame(df_raw).fillna(0)


    @classmethod
    def historical_price(cls,stock,start_date = '2010-01-01',end_date = '2024-09-20') -> pd.DataFrame:
        '''
        In ra dữ liệu về thông tin giao dịch của các cổ phiếu niêm yết trên sàn chứng khoán tại Việt Nam
        -----

            Parameter:
            -----
                `stock (str)`: Mã cổ phiếu niêm yết
                `start_date (str)`: Ngày bắt đầu trong khoảng thời gian cần lấy thông tin giao dịch
                `end_date (str)`: Ngày kết thúc trong khoảng thời gian cần lấy thông tin giao dịch

            Return:
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:
                Các khoản mục của thông tin giao dịch tương ứng là columns của DataFrame
                    Eg: Để xem các khoản mục có thể thực hiện
                        `price('HPG').columns`
                Ngày ghi nhận là index của DataFrame
        '''
        try:
            url_ = 'https://restv2.fireant.vn/symbols/{}/historical-quotes?startDate={}&endDate={}&offset=0&limit=999999'.format(stock,start_date,end_date)
            df_raw = rq.get(url_,headers= cls.fireant_header).json()
            date_raw = pd.to_datetime([x['date'] for x in df_raw]).strftime(date_format='%Y%m%d').astype(int)
            df = pd.DataFrame(df_raw)
            df['date'] = date_raw
            df = df.sort_values(by = 'date', ascending= True)
            #####
            cols = ['priceOpen','priceClose','priceHigh','priceLow','priceAverage']
            try:
                df[cols] = df[cols].div(df['adjRatio'],axis=0)
            except:
                pass
            #####
            return df.reset_index(drop=True)
        except:
            pass
    
    @classmethod
    def financial_report(cls,stock,type = 1,year = 2023,period = 'Y') -> pd.DataFrame:
        '''
        In ra dữ liệu về báo cáo tài chính của các doanh nghiệp niêm yết tại Việt Nam
        -----

            Parameter:
            -----
            `stock (str)`: Mã cổ phiếu niêm yết
            `type (int)`: Loại báo cáo trong báo cáo tài chính cần lấy

                type = 1: Bảng cân đối kế toán
                type = 2: Báo cáo kết quả hoạt động kinh doanh
                type = 3: Báo cáo lưu chuyển tiền tệ trực tiếp (Đa số các doanh nghiệp bị trống dữ liệu về báo cáo lưu chuyển tiền tệ trực tiếp, trừ nhóm ngành ngân hàng)
                type = 4: Báo cáo lưu chuyển tiền tệ gián tiếp
            `year (int)`: Năm cuối cùng trong danh sách báo cáo tài chính cần lấy
            `period (str)`: Quý của báo cáo tài chính cần lấy
                period = Y: Sẽ lấy báo cáo tài chính theo năm của doanh nghiệp
                period = Q: Sẽ lấy báo cáo tài chính theo quý của năm tương ứng với parameter `year`

            Return:
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:
                Các khoản mục của báo cáo tương ứng là columns của DataFrame
                    Eg: Để xem các khoản mục có thể thực hiện
                        `bctc('HPG',type=1).columns`
                Năm báo cáo tương ứng là index của DataFrame
        '''
        if period == 'Y':
            quarter = 0
        else:
            quarter = 4

        def take_data(stock,type,year,quarter):
                ####
                url_ = 'https://restv2.fireant.vn/symbols/{}/full-financial-reports?type={}&year={}&quarter={}&limit=999999'.format(stock,type,year,quarter)
                df_raw = rq.get(url_,headers=headers_list.fireant_header).json()
                indexs = [x['name'] for x in df_raw]
                year_ = [x['year'] for x in df_raw[0]['values']]
                quarter_ = [x['quarter'] for x in df_raw[0]['values']]

                if quarter != 0:
                    dates = []
                    for x,y in zip(year_,quarter_):
                        date_ = pd.Period(year=x, quarter=y, freq='Q').end_time + pd.offsets.MonthEnd(1)
                        dates.append(float(date_.strftime('%Y%m%d')))
                    col = dates
                ###
                else:
                    col = [(x+1)*10**4 + 131 for x in year_]
                ###
                df = [[z['value']for z in y] for y in [x['values'] for x in df_raw]]
                df = pd.DataFrame(df,index = indexs, columns=col)
                #####
                df = df.fillna(value=0)
                df = df.transpose()
                #####
                return df
        if type == 'all':
            dfs = pd.DataFrame()
            for type_ in [1,2,3,4]:
                try:
                    df = take_data(stock,type_,year,quarter)
                    for x in df.columns:
                        if x in dfs.columns:
                            dfs[x] = dfs[x].fillna(df[x])
                        else:
                            dfs[x] = df[x]
                except:
                    pass
            #####
            dfs['Symbol'] = stock
            dfs['Date'] = dfs.index
            dfs = dfs.reset_index(drop=True)
            return dfs
        else:
            try:
                df = take_data(stock,type,year,quarter)\
                #####
                df['Symbol'] = stock
                df['Date'] = df.index
                df = df.reset_index(drop=True)
                return df
            except:
                print('Lỗi type nên không lấy được dữ liệu')
    @classmethod
    def financial_ratio(cls,stock, period):
        '''
        In ra dữ liệu về chỉ số tài chính của các doanh nghiệp niêm yết tại Việt Nam
        -----

            Parameter:
            -----
            `stock (str)`: Mã cổ phiếu niêm yết
            `period (str)`: Kiểu thời gian của chỉ số tài chính cần lấy
                period = Y: Sẽ lấy chỉ số tài chính theo năm của doanh nghiệp
                period = Q: Sẽ lấy chỉ số tài chính theo quý của doanh nghiệp

            Return:
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:
                Các khoản mục của chỉ số tương ứng là columns của DataFrame
                    Eg: Để xem các khoản mục có thể thực hiện
                        `financial_ratio('HPG',period='Q').columns`
                Năm báo cáo tương ứng là index của DataFrame
        '''
        url = f'https://restv2.fireant.vn/symbols/{stock}/financial-data?type={period}&count=9999'
        try:
            data = rq.get(url, headers= cls.fireant_header).json()
            values = [x['financialValues'] for x in data]
            values = pd.DataFrame(values)
            values['symbol'] = stock
            return values
        except:
            pass

    @classmethod
    def trading_structure(cls,stock = 'VCB'):
        '''
        In ra dữ liệu về cơ cấu giao dịch của các cổ phiếu niêm yết trên sàn chứng khoán tại Việt Nam
        -----

            Parameter:
            -----
            `stock (str)`: Mã cổ phiếu niêm yết

            Return:
            -----
            pd.Dataframe chứa thông tin cấu trúc giao dịch của cổ phiếu bao gồm:
                Ngày giao dịch: date
                Mã cổ phiếu: symbol
                Giá đóng cửa: close_value
                Và các giao dịch tổ chức, cá nhân trong và ngoài nước tương ứng
        '''
        url = "https://api-finance-t19.24hmoney.vn/v1/ios/stock/statistic-investor-history"
        params = {
            "symbol": stock
        }
        try:
            response = rq.get(url=url,params=params)
            response = response.json()['data']
            df = pd.DataFrame(response)
            df['trading_date'] = pd.to_datetime(df['trading_date'], unit='s') + pd.Timedelta(hours=7)
            df['trading_date'] = df['trading_date'].dt.strftime('%Y%m%d')
            ###
            df = df.rename(columns={'code':'symbol','trading_date':'date'})
            return df.sort_values(['symbol','date'], ascending=True)
        except:
            pass

    @classmethod
    def intraday_price(cls,stock, day_):
        '''
        In ra dữ liệu về giao dịch khớp lệnh trong phiên của các cổ phiếu niêm yết trên sàn chứng khoán tại Việt Nam
        -----

            Parameter:
            -----
            `stock (str)`: Mã cổ phiếu niêm yết
            `day_ (str)`: Ngày giao dịch cần lấy dữ liệu, định dạng là YYYY-MM-DD
                Eg: '2023-09-20'
            Return:
            -----
            pd.Dataframe chứa thông tin giao dịch khơp lệnh trong phiên của cổ phiếu
        '''
        start = (pd.to_datetime(day_)).timestamp()
        end = (pd.to_datetime(day_) + timedelta(days=1)).timestamp()
        #####
        url = "https://iboard-api.ssi.com.vn/statistics/charts/history"

        params = {
            "symbol": stock,
            "from": start,
            "to": end,
            "resolution": "1",
            "language": "vi"
        }
        #####
        try:
            response = rq.get(url, headers=cls.ssi_headers, params=params).json()
            data = pd.DataFrame(response['data'])
            data['v'] = data['v'].cumsum()
            data['symbol'] = stock
            return data
        except:
            pass

class market(headers_list):
    @classmethod
    def market_list(cls,exchange = 'HSX', type_ = 'all') -> pd.DataFrame:
        '''
        In ra danh sách cổ phiếu của các sàn giao dịch tại Việt Nam
        -----

            Parameter:
            -----
            `exchange (str)`: Tên của sàn giao dịch
            `type_ (str)`: Loại chứng khoán
            Return:
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:
                Mã giao dịch: Symbol
                Sàn niêm yết: TradeCenterId
                Tên công ty: CompanyName
                Ngành nghề của doanh nghiệp: CategoryName
        '''
        start_point = "https://s.cafef.vn/du-lieu-download.chn#data"

        html_text = rq.post(start_point, verify=False).text
        html_text = re.findall(r'<a href=(.*?)>Upto 3 sàn<', html_text)[0]

        url = re.findall(r'\'(.*?)\'', html_text)[0]
        response = rq.get(url)

        r_data = pd.DataFrame()
        with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip:
            file_list = the_zip.namelist()

            for file_name in file_list:
                with the_zip.open(file_name) as file:
                    df = pd.read_csv(file)
                    df['<Exchange>'] = file_name.split('.')[1]
                
                r_data = pd.concat([r_data, df], axis= 0)
        r_data.columns = [re.sub(r'[<>]', '', x) for x in r_data.columns]

        r_data = r_data.rename(columns={'Ticker':'Symbol', 'DTYYYYMMDD':'Date'})
        r_data = r_data.sort_values('Date', ascending= True).reset_index(drop=True)

        if exchange == 'all' and type_ == 'all':
            return r_data
        elif type_ == 'all' and exchange != 'all':
            return r_data.query('Exchange == @exchange')
        else:
            return r_data.query('Exchange == @exchange').query('Symbol.str.len() == 3')