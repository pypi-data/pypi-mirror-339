from .lib import *
from .headers import *
#####
class bond(headers_list):
    @classmethod
    def trading_data(cls,start_date, end_date):
        today = date.today().strftime('%d/%m/%Y')
        year = date.today().strftime('%Y')
        #####
        url = "https://cbonds.hnx.vn/thong-ke-thi-truong/danh-sach"
        payload = [
            ("keySearch", f"{today}|{today}||1|1|{year}|{today}|{today}|{start_date}|{end_date}"),
            ("arrCurrentPage[]", "1"),
            ("arrCurrentPage[]", "2"),
            ("arrCurrentPage[]", "1"),
            ("arrNumberRecord[]", "5"),
            ("arrNumberRecord[]", "10000"),
            ("arrNumberRecord[]", "20")
        ]
        response = rq.post(url, headers=cls.cbonds_headers, data=payload, verify=False)
        numpage = re.findall(r'Tổng số <b>(.*?)</b> bản ghi', response.text)[0]
        #####
        url = "https://cbonds.hnx.vn/thong-ke-thi-truong/danh-sach"
        payload = [
            ("keySearch", f"{today}|{today}||1|1|{year}|{today}|{today}|{start_date}|{end_date}"),
            ("arrCurrentPage[]", "1"),
            ("arrCurrentPage[]", str(numpage)),
            ("arrCurrentPage[]", "1"),
            ("arrNumberRecord[]", "5"),
            ("arrNumberRecord[]", str(numpage)),
            ("arrNumberRecord[]", "20")
        ]
        response = rq.post(url, headers=cls.cbonds_headers, data=payload, verify=False)
        # Creat DataFrame
        data = re.sub(r'\s+', ' ', response.text)
        data = re.findall(r'<div id="register_bond" class="hidden">(.*?)</table>', data)\
        #####
        head = re.findall(r'<thead>(.*?)</thead>', data[0])
        head = re.findall(r'">(.*?)</th>', head[0])
        #####
        body = re.findall(r'<tbody>(.*?)</tbody>', data[0])
        body = re.findall(r'<tr>(.*?)</tr>', body[0])
        value = []
        for row in body:
            row = re.findall(r'">(.*?)</td>|<td>(.*?)</td>', row)
            row = [x[0] if x[0] != '' else x[1] for x in row]
            value.append(row)
        #####
        return pd.DataFrame(value, columns = head)
    
    @classmethod
    def yield_curve(cls, date):
        date_ = pd.to_datetime(date).strftime('%d/%m/%Y') + '|'
        url = "https://www.hnx.vn/ModuleReportBonds/Bond_YieldCurve/SearchAndNextPageDuLieuTT_Indicator"
        headers = {
            "x-requested-with": "XMLHttpRequest"
        }
        payload = {
            "p_keysearch": date_,
            "pColOrder": "col_a",
            "pOrderType": "ASC",
            "pCurrentPage": "1",
            "pIsSearch": "1"
        }

        def convert(x):
            if 'năm' in x:
                x = x.replace(' năm','').strip()
                x = float(x) * 12
                return str(x)
            else:
                x = x.replace(' tháng','').strip()
                return str(x)

        response = rq.post(url, headers=headers, data=payload, verify=False).text
        #####
        data = re.sub(r'\s+', ' ', response)
        head = re.findall(r'<thead>(.*?)</thead>', data)
        head = re.findall(r'">(.*?)</th>', head[0])
        head = [html.unescape(x) for x in head]
        #####
        value = re.findall(r'<tbody>(.*?)</tbody>', data)
        value = re.findall(r'<tr>(.*?)</tr>', value[0])
        value = [re.findall(r'">(.*?)</td>', x) for x in value]
        df = pd.DataFrame(value, columns=head)
        df = df.applymap(lambda x: html.unescape(x))
        df['Kỳ hạn còn lại'] = df['Kỳ hạn còn lại'].apply(convert)
        df = df.applymap(lambda x: float(x.replace(',','.') if x != '' else 0))
        df['date'] = int(pd.to_datetime(date).strftime('%Y%m%d'))
        #####
        return df