from .lib import *
from .headers import *
##########

class fund(headers_list):
    @classmethod
    def market_list(cls, fund_type = 'all'):
        '''
        In ra danh sách các quỹ mở đang hoạt động tại Việt Nam
        -----
            Parameter:\n
            -----
            `fund_type (str)`: Phân loại quỹ thông qua tài sản quản lý
            -----
            Return:\n
            -----
            pd.Dataframe chứa thông tin về cổ phiếu bao gồm:  
                Mã trái phiếu: id  
                Tên quỹ: TradeCenterId  
                Tên rút gọn: shortName  
                Mã: code  
                Mã bổ sung: subCode  
                Mã giao dịch: tradeCode  
                Lợi nhuận kỳ vọng: expectedReturn  
                Phí quản lý: managementFee  
                Phí hiệu suất: performanceFee  
                Lợi nhuận trung bình năm: avgAnnualReturn  
                Phân loại quỹ thông qua tài sản: dataFundAssetType  
                + Bao gồm: Quỹ cổ phiếu, Quỹ trái phiếu, Quỹ cân bằng  
                Phân loại quỹ thông qua loại hình: fundType
            -----
        '''

        url = 'https://api.fmarket.vn/res/products/filter'
        header = cls.fmarket_headers
        payload = {
                "types": ["NEW_FUND", "TRADING_FUND"],
                "issuerIds": [],
                "sortOrder": "DESC",
                "sortField": "navTo12Months",
                "page": 1,
                "pageSize": 999999,
                "isIpo": False,
                "fundAssetTypes": [],
                "bondRemainPeriods": [],
                "searchField": "",
                "isBuyByReward": False,
                "thirdAppIds": []
                }

        df = rq.post(url, headers=header, json=payload).json()
        df = pd.DataFrame(df['data']['rows'])
        result = df[['id', 'name', 'shortName', 'code', 'subCode', 'tradeCode', 'sipCode',
                'expectedReturn', 'managementFee', 'performanceFee',
                'avgAnnualReturn','type','status']]
        #####
        result['dataFundAssetType'] = [x['name'] for x in df['dataFundAssetType']]
        result['fundType'] = [x['name'] for x in df['fundType']]
        #####
        if fund_type =='all':
            return result
        else:
            return result[result['dataFundAssetType'] == fund_type].reset_index(drop=True)
        
    @classmethod
    def infor(cls,id = 11,report_type = 'holding_list'):
        url = f'https://api.fmarket.vn/res/products/{id}'
        header = cls.fmarket_headers
        df = rq.get(url, headers=header).json()
        #####
        summary_data = df['data']
        report = summary_data['fundReport']
        key_list = ['id','code','tradeCode','price','nav','managementFee','performanceFee']
        summary = {x:summary_data[x] for x in key_list}
        summary_data = summary | report
        summary_data['riskLevel'] = df['data']['riskLevel']['name']
        summary_data = pd.DataFrame(summary_data,index=[0])
        summary_data['reportTime'] = summary_data['reportTime'].apply(lambda x: pd.to_datetime(x, unit='ms').strftime('%Y%m%d'))
        if report_type == 'summary':
            data = summary_data
        else:
            if report_type == 'holding_list':
                data = df['data']['productTopHoldingList'] + df['data']['productTopHoldingBondList']
                data = pd.DataFrame(data)
                data['updateAt'] = data['updateAt'].apply(lambda x: pd.to_datetime(x, unit='ms').strftime('%Y%m%d'))
                data['id'] = df['data']['id']
                data['tradeCode']= df['data']['tradeCode']

            elif report_type == 'asset_list':
                data = df['data']['productAssetHoldingList']
                data = pd.DataFrame(data)
                data['assetType'] = [x['name'] for x in data['assetType']]
                data['updateAt'] = data['updateAt'].apply(lambda x: pd.to_datetime(x, unit='ms').strftime('%Y%m%d'))
                data['createAt'] = data['createAt'].apply(lambda x: pd.to_datetime(x, unit='ms').strftime('%Y%m%d'))
                data['id'] = df['data']['id']
                data['tradeCode']= df['data']['tradeCode']
            elif report_type == 'industry_list':
                data = df['data']['productIndustriesHoldingList']
                data = pd.DataFrame(data)
                data['id'] = df['data']['id']
                data['tradeCode']= df['data']['tradeCode']
            else:
                print('Kiểm tra lại report_type')
            #####
            data = pd.merge(data,summary_data,how='outer',on=['id','tradeCode'])
        #####
        try:
            return data
        except:
            pass
