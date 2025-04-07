<div align="center">

# **Thư viện thu thập dữ liệu và backtest chiến lược đầu tư**
# **dữ liệu dựa trên thị trường chứng khoán Việt Nam**
</div>


## Hướng dẫn cài đặt

Để cài đặt package sử dụng câu lệnh:

    pip install datavns
  
Để import thư viện vào file và sử dụng

    from datavns import *

## I. GIỚI THIỆU TỔNG QUAN
Pakage bao gồm 2 phần
- Phần một là thu thập dữ liệu về thị trường

- Phần hai là công cụ xây dựng bộ lọc cổ phiếu tùy chỉnh và báo cáo theo dõi thị trường

## II. THU THẬP DỮ LIỆU

### Phần 1: Thu thập dữ liệu về cổ phiếu

#### 1.1 Thu thập dữ liệu về danh sách cổ phiếu niêm yết
*Để thu thập dữ liệu về danh sách cổ phiếu theo sàn, chúng ta có thể sử dụng câu lệnh*
```python
market.market_list(exchange = 'HSX')
```
Trong đó:

  `exchange (str)`: Sàn giao dịch niêm yết cổ phiếu ('all' để lấy toàn bộ các sàn)

<details>
  <summary>Output</summary>

```
              Symbol      Date       Open       High        Low      Close     Volume Exchange
0                SAM  20000728     2.0349     2.0349     2.0349     2.0365       3200      HSX
1                REE  20000728     0.9776     0.9776     0.9776     0.9787       1000      HSX
2                SAM  20000731     2.0588     2.0588     2.0588     2.0604      10000      HSX
3                REE  20000731     0.9959     0.9959     0.9959     0.9970        300      HSX
4                SAM  20000802     2.0948     2.0948     2.0948     2.0964        200      HSX
...              ...       ...        ...        ...        ...        ...        ...      ...
2912924          SMC  20250306     5.9100     5.9600     5.8200     5.9000     578300      HSX
2912925          SPM  20250306    12.2500    12.2500    11.6000    11.9000       1700      HSX
2912926          SRF  20250306     9.8000     9.8000     9.8000     9.8000        500      HSX
2912927          AAM  20250306     6.8000     7.0500     6.8000     6.9000       8600      HSX
2913587  VNAll-INDEX  20250306  1369.0400  1381.4000  1368.8500  1381.4000  898852100      HSX
```
</details>

#### 1.2 Thu thập dữ liệu về lịch sử giao dịch của cổ phiếu
*Để thu thập dữ liệu về thông tin giao dịch của từng cổ phiếu, chúng ta có thể sử dụng câu lệnh*
```python
stocks.historical_price('VCB',start_date = '2010-01-01', end_date = '2024-09-20')
```
Trong đó:

  `cp (str)`: Mã cổ phiếu niêm yết

  `start_date (str)`: Ngày bắt đầu trong khoảng thời gian cần lấy thông tin giao dịch

  `end_date (str)`: Ngày kết thúc trong khoảng thời gian cần lấy thông tin giao dịch
<details>
  <summary>Output</summary>

```
          date symbol  priceHigh   priceLow  priceOpen  priceAverage  priceClose  ...  sellQuantity  adjRatio  currentForeignRoom  propTradingNetDealValue  propTradingNetPTValue  propTradingNetValue    unit
0     20100104    VCB  11.300549  10.773343  10.773343     11.300549   11.300549  ...      865560.0   4.36262          85159984.0                      NaN                    NaN                  NaN  1000.0
1     20100105    VCB  11.804834  11.300549  11.690224     11.415159   11.415159  ...     1999730.0   4.36262          85278644.0                      NaN                    NaN                  NaN  1000.0
2     20100106    VCB  11.415159  11.002563  11.025485     11.002563   11.002563  ...     1339960.0   4.36262          85231164.0                      NaN                    NaN                  NaN  1000.0
3     20100107    VCB  11.025485  10.773343  11.002563     10.773343   10.773343  ...      568020.0   4.36262          85178404.0                      NaN                    NaN                  NaN  1000.0
4     20100108    VCB  10.956719  10.750421  10.910875     10.773343   10.773343  ...      638120.0   4.36262          85225064.0                      NaN                    NaN                  NaN  1000.0
...        ...    ...        ...        ...        ...           ...         ...  ...           ...       ...                 ...                      ...                    ...                  ...     ...
3665  20240916    VCB  90.000000  88.800000  89.600000     89.461289   88.900000  ...     1439529.0   1.00000         371202084.0             1.126212e+10          -5.580000e+10        -4.453788e+10  1000.0
3666  20240917    VCB  90.500000  88.600000  89.000000     89.320375   90.500000  ...     1463678.0   1.00000         371934866.0             3.356401e+09           0.000000e+00         3.356401e+09  1000.0
3667  20240918    VCB  91.900000  89.700000  90.600000     91.210615   91.000000  ...     3497524.0   1.00000         371899480.0             1.173037e+10          -4.840000e+06         1.172553e+10  1000.0
3668  20240919    VCB  91.700000  90.900000  91.000000     91.378410   91.500000  ...     2765481.0   1.00000         371316716.0             1.069481e+10          -1.778000e+06         1.069303e+10  1000.0
3669  20240920    VCB  92.000000  90.600000  91.800000     91.137649   90.600000  ...     4702415.0   1.00000         370455345.0            -9.759550e+09          -8.150000e+05        -9.760365e+09  1000.0
```
</details>

#### 1.3 Thu thập dữ liệu về báo cáo tài chính
*Để thu thập dữ liệu về báo cáo tài chính của từng cổ phiếu, chúng ta có thể sử dụng câu lệnh*
```python
stocks.financial_report('VCB',type= 1, year= 2025, quarter= 0)
```
Trong đó:

  `cp (str)`: Mã cổ phiếu niêm yết

  `type (int)`: Loại báo cáo trong báo cáo tài chính cần lấy
  
      type = 'all': Lấy toàn bộ các báo cáo tài chính ghép lại
      type = 1: Bảng cân đối kế toán
      type = 2: Báo cáo kết quả hoạt động kinh doanh
      type = 3: Báo cáo lưu chuyển tiền tệ trực tiếp (Đa số các doanh nghiệp bị trống dữ liệu về báo cáo lưu chuyển tiền tệ trực tiếp, trừ nhóm ngành ngân hàng)
      type = 4: Báo cáo lưu chuyển tiền tệ gián tiếp

  `year (int)`: Năm cuối cùng trong danh sách báo cáo tài chính cần lấy

  `quarter (int)`: Quý của báo cáo tài chính cần lấy

      quarter = 0: Sẽ lấy báo cáo tài chính theo năm của doanh nghiệp
      quarter = 1-4: Sẽ lấy báo cáo tài chính theo quý của năm tương ứng với parameter `year`

<details>
  <summary>Output</summary>

```
   TÀI SẢN I. Tiền mặt, chứng từ có giá trị, ngoại tệ, kim loại quý, đá quý II. Tiền gửi tại NHNN  ... TỔNG CỘNG NGUỒN VỐN Symbol      Date
0        0                                    1042698000000.0                     1866498000000.0  ...    81668309000000.0    VCB  20030131
1        0                                    1512072000000.0                     4892625000000.0  ...    97653125000000.0    VCB  20040131
2        0                                    1869932000000.0                     2607245000000.0  ...   121430938000000.0    VCB  20050131
3        0                                    2006412000000.0                     6336385000000.0  ...   136720611000000.0    VCB  20060131
4        0                                    2418207000000.0                    11848460000000.0  ...   166952020000000.0    VCB  20070131
5        0                                    3204247000000.0                    11662669000000.0  ...   197408036000000.0    VCB  20080131
6        0                                    3482209000000.0                    30561417000000.0  ...   221950448000000.0    VCB  20090131
7        0                                    4485150000000.0                    25174674000000.0  ...   255495883000000.0    VCB  20100131
8        0                                    5232743000000.0                     8239851000000.0  ...   307496090000000.0    VCB  20110131
9        0                                    5393766000000.0                    10616759000000.0  ...   366722279000000.0    VCB  20120131
10       0                                    5627307000000.0                    15732095000000.0  ...   414488317000000.0    VCB  20130131
11       0                                    6059673000000.0                    24843632000000.0  ...   468994032000000.0    VCB  20140131
12       0                                    8323385000000.0                    13267101000000.0  ...   576995651000000.0    VCB  20150131
13       0                                    8519334000000.0                    19715035000000.0  ...   674394640000000.0    VCB  20160131
14       0                                    9692053000000.0                    17382418000000.0  ...   787906892000000.0    VCB  20170131
15       0                                   10102861000000.0                    93615618000000.0  ...  1035293283000000.0    VCB  20180131
16       0                                   12792045000000.0                    10845701000000.0  ...  1074026560000000.0    VCB  20190131
17       0                                   13778358000000.0                    34684091000000.0  ...  1222718858000000.0    VCB  20200131
18       0                                   15095394000000.0                    33139373000000.0  ...  1326230092000000.0    VCB  20210131
19       0                                   18011766000000.0                    22506711000000.0  ...  1414986259000000.0    VCB  20220131
20       0                                   18348534000000.0                    92557809000000.0  ...  1813815170000000.0    VCB  20230131
21       0                                   14504849000000.0                    58104503000000.0  ...  1839613198000000.0    VCB  20240131
22       0                                   14268065000000.0                    49340493000000.0  ...  2085397244000000.0    VCB  20250131
```
</details>

#### 1.4 Thu thập dữ liệu về lịch sử chi trả cổ tức
*Để thu thập dữ liệu về lịch sử chi trả cổ tức của của từng cổ phiếu, chúng ta có thể sử dụng câu lệnh*
```python
stocks.historical_dividends('VCB',num=50)
```
Trong đó:

  `start_date (str)`: Ngày bắt đầu trong khoảng thời gian cần lấy thông tin giao dịch

  `end_date (str)`: Ngày kết thúc trong khoảng thời gian cần lấy thông tin giao dịch

<details>
  <summary>Output</summary>

```
    year  cashDividend  stockDividend   totalAssets  stockHolderEquity
0   2002           0.0            0.0  8.166831e+13       4.564857e+12
1   2003           0.0            0.0  9.765312e+13       5.923811e+12
2   2004           0.0            0.0  1.214309e+14       8.051755e+12
3   2005           0.0            0.0  1.367206e+14       8.416426e+12
4   2006           0.0            0.0  1.669520e+14       1.112725e+13
5   2007           0.0            0.0  1.974080e+14       1.355155e+13
6   2008           0.0            0.0  2.219504e+14       1.379004e+13
7   2009           0.0            0.0  2.554959e+14       1.671033e+13
8   2010        1200.0            0.0  3.074961e+14       2.066948e+13
9   2011           0.0           12.0  3.667223e+14       2.863870e+13
10  2012        1200.0            0.0  4.144883e+14       4.154685e+13
11  2013        1200.0            0.0  4.689940e+14       4.238606e+13
12  2014        1200.0           15.0  5.769957e+14       4.332397e+13
13  2015        1000.0            0.0  6.743946e+14       4.500704e+13
14  2016        1000.0           35.0  7.879069e+14       4.795799e+13
15  2017         800.0            0.0  1.035293e+15       5.246864e+13
16  2018         800.0            0.0  1.074027e+15       6.211039e+13
17  2019         800.0            0.0  1.222719e+15       8.079952e+13
18  2020         800.0            0.0  1.326230e+15       9.400996e+13
19  2021        1200.0           27.6  1.414986e+15       1.090993e+14
20  2022           0.0            0.0  1.813815e+15       1.355577e+14
21  2023           0.0           18.1  1.839613e+15       1.649187e+14
22  2024           0.0            0.0  2.085397e+15       1.988598e+14
23  2025           0.0           49.5  0.000000e+00       0.000000e+00
```
</details>

### Phần 2: Thu thập dữ liệu về trái phiếu

#### 2.1 Thu thập dữ liệu về giao dịch trái phiếu
```python
bond.trading_data(start_date='01/01/2024',end_date='31/03/2025')
```
Trong đó:

  `cp (str)`: Mã cổ phiếu niêm yết

  `num (int)`: Số năm lấy dữ liệu chi trả cổ tức, tính ngược từ thời điểm hiện tại

<details>
  <summary>Output</summary>

```
       STT Ngày giao dịch Mã giao dịch Khối lượng giao dịch  Giá trị giao dịch Giá giao dịch cuối cùng của ngày
0              20/12/2024     SUJ12101              299,980  4,338,655,137,040                       14,464,499
1              24/12/2024     XD312301               25,000  3,510,588,437,500                      140,436,356
2              20/01/2025     MKH12301               25,000  3,232,666,375,000                      129,318,337
3              27/09/2024     XD312301               22,500  3,126,825,000,000                      138,970,000
4              28/11/2024     IDS12101           30,028,272  3,083,690,404,508                          102,027
...     ..            ...          ...                  ...                ...                              ...
345191         06/03/2025     PTJ12301                    0                  0                                0
345192         06/03/2025     CTG12414                    0                  0                                0
345193         06/03/2025     VJC12406                    0                  0                                0
345194         06/03/2025     HDC12202                    0                  0                                0
345195         06/03/2025     VIB12108                    0                  0                                0
```
</details>


### Phần 3: Thu thập dữ liệu về các quỹ trên thị trường

*Hiện tại chỉ có dữ liệu của các quỹ mở đang hoạt động mới có thể thu thập*
#### 3.1 Thu thập dữ liệu về thông tin quỹ
```python
fund.market_list(fund_type='all')
```
Trong đó:

  `fund_type (str)`: Kiểu quỹ mong muốn lấy dữ liệu
                    - Bao gồm : Quỹ cổ phiếu, Quỹ trái phiếu và Quỹ cân bằng

<details>
  <summary>Output</summary>

```
    id                                               name shortName     code subCode          tradeCode  ... performanceFee  avgAnnualReturn          type          status  dataFundAssetType fundType
0   68   QUỸ ĐẦU TƯ CỔ PHIẾU KINH TẾ HIỆN ĐẠI VINACAPITAL     VMEEF     VMPF    None           VMPFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
1   11         QUỸ ĐẦU TƯ LỢI THẾ CẠNH TRANH BỀN VỮNG SSI    SSISCA   SSISCA    None         mua SSISCA  ...            NaN             29.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
2   46               QUỸ ĐẦU TƯ CỔ PHIẾU TĂNG TRƯỞNG VCBF  VCBF-MGF  VCBFMGF    None            VCBFMGF  ...            NaN              1.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
3   49            QUỸ ĐẦU TƯ TĂNG TRƯỞNG DÀI HẠN VIỆT NAM      VLGF     VLGF    None           mua VLGF  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
4   14            QUỸ ĐẦU TƯ CỔ PHIẾU TRIỂN VỌNG BẢO VIỆT      BVPF     BVPF    None           BVPFN001  ...            NaN             14.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
5   32                  QUỸ ĐẦU TƯ CỔ PHIẾU HÀNG ĐẦU VCBF  VCBF-BCF  VCBFBCF    None            VCBFBCF  ...           1.90             25.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
6   47                      QUỸ ĐẦU TƯ GIÁ TRỊ MB CAPITAL      MBVF     MBVF    None               MBVF  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
7   64                   QUỸ ĐẦU TƯ TRÁI PHIẾU LIGHTHOUSE      LHBF     LHBF    None           LHBFN001  ...          12.00              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
8   22           QUỸ ĐẦU TƯ CÂN BẰNG TUỆ SÁNG VINACAPITAL      VIBF     VIBF    None           VIBFN003  ...            NaN             19.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
9   23  QUỸ ĐẦU TƯ CỔ PHIẾU TIẾP CẬN THỊ TRƯỜNG VINACA...     VESAF    VESAF    None          VESAFN002  ...            NaN             33.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
10  28                QUỸ ĐẦU TƯ CHỨNG KHOÁN NĂNG ĐỘNG DC      DCDS   VFMVF1    None         VFMVF1N001  ...            NaN             36.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
11  31                QUỸ ĐẦU TƯ CÂN BẰNG CHIẾN LƯỢC VCBF  VCBF-TBF  VCBFTBF    None            VCBFTBF  ...           0.00             20.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
12  20         QUỸ ĐẦU TƯ CỔ PHIẾU HƯNG THỊNH VINACAPITAL      VEOF     VEOF    None           VEOFN003  ...            NaN             22.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
13  70                       QUỸ ĐẦU TƯ CÂN BẰNG BẢN VIỆT    VCAMBF   VCAMBF    None         VCAMBFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
14  41    QUỸ ĐẦU TƯ CỔ PHIẾU TĂNG TRƯỞNG BALLAD VIỆT NAM      TBLF     TBLF    None  nop tien mua TBLF  ...           1.00             -4.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
15  48                           QUỸ ĐẦU TƯ TRÁI PHIẾU MB    MBBOND   MBBOND    None             MBBOND  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
16  35  QUỸ ĐẦU TƯ CỔ PHIẾU TĂNG TRƯỞNG MIRAE ASSET VI...     MAGEF    MAGEF    None          MAGEFN001  ...           1.75             21.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
17  72                       QUỸ ĐẦU TƯ CỔ PHIẾU MANULIFE    MAFEQI   MAFEQI    None             MAFEQI  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
18  81  QUỸ ĐẦU TƯ NĂNG ĐỘNG EASTSPRING INVESTMENTS VI...       ENF      ENF    None            ENFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
19  12             QUỸ ĐẦU TƯ CỔ PHIẾU NĂNG ĐỘNG BẢO VIỆT     BVFED    BVFED    None          BVFEDN001  ...            NaN             16.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
20  33                         QUỸ ĐẦU TƯ TRÁI PHIẾU VCBF  VCBF-FIF  VCBFFIF    None            VCBFFIF  ...           0.10              6.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
21  37                          QUỸ ĐẦU TƯ TRÁI PHIẾU VND     VNDBF    VNDBF    None          mua VNDBF  ...            NaN              7.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
22  45                        QUỸ ĐẦU TƯ TRÁI PHIẾU PVCOM      PVBF     PVBF    None       mua quy PVBF  ...           1.00              8.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
23  27                           QUỸ ĐẦU TƯ TRÁI PHIẾU DC      DCBF   VFMVFB    None         VFMVFBN001  ...            NaN             14.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
24  71                       QUỸ ĐẦU TƯ CÂN BẰNG MANULIFE    MAFBAL   MAFBAL    None             MAFBAL  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
25  29                        QUỸ ĐẦU TƯ TĂNG TRƯỞNG DFVN      DCAF     DCAF    None           DCAFN002  ...           1.50             19.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
26  21        QUỸ ĐẦU TƯ TRÁI PHIẾU BẢO THỊNH VINACAPITAL       VFF      VFF    None            VFFN003  ...            NaN             10.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
27  50  QUỸ ĐẦU TƯ TRÁI PHIẾU LINH HOẠT MIRAE ASSET VI...      MAFF     MAFF    None           MAFFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
28  77                      QUỸ ĐẦU TƯ NĂNG ĐỘNG MANULIFE       MDI      MDI    None                MDI  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
29  58            QUỸ ĐẦU TƯ CỔ PHIẾU UNITED ESG VIỆT NAM     UVEEF    UVEEF    None          UVEEFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
30  69                    QUỸ ĐẦU TƯ GIA TĂNG GIÁ TRỊ GFM   GFM-VIF   GFMVIF    None         GFMVIFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
31  13                    QUỸ ĐẦU TƯ TRÁI PHIẾU BẢO VIỆT       BVBF     BVBF    None           BVBFN001  ...            NaN             12.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
32   8                          QUỸ ĐẦU TƯ TRÁI PHIẾU SSI     SSIBF    SSIBF    None          mua SSIBF  ...            NaN              7.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
33  65                      QUỸ ĐẦU TƯ TRÁI PHIẾU AN BÌNH      ABBF     ABBF    None           ABBFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
34  25            QUỸ ĐẦU TƯ CỔ PHIẾU TẬP TRUNG CỔ TỨC DC      DCDE   VFMVF4    None         VFMVF4N001  ...            NaN             13.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
35  63                     QUỸ ĐẦU TƯ TRÁI PHIẾU BẢN VIỆT    VCAMFI   VCAMFI    None         VCAMFIN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
36  67  QUỸ ĐẦU TƯ TRÁI PHIẾU GIA TĂNG THU NHẬP CỐ ĐỊN...      DCIP   VFMVFC    None         VFMVFCN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
37  51                QUỸ ĐẦU TƯ TRÁI PHIẾU AN TOÀN AMBER      ASBF     ASBF    None           ASBFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
38  38                            QUỸ ĐẦU TƯ CHỦ ĐỘNG VND     VNDAF    VNDAF    None          mua VNDAF  ...            NaN             15.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
39  40                QUỸ ĐẦU TƯ TRÁI PHIẾU LINH HOẠT VND     VNDCF    VNDCF    None          mua VNDCF  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
40  66              QUỸ ĐẦU TƯ CHỌN LỌC PHÚ HƯNG VIỆT NAM     PHVSF    PHVSF    None          PHVSFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
41  53      QUỸ ĐẦU TƯ TRÁI PHIẾU THANH KHOẢN VINACAPITAL      VLBF     VLBF    None           VLBFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
42  62               QUỸ ĐẦU TƯ TRÁI PHIẾU LỢI TỨC CAO HD    HDBOND   HDBOND    None         HDBONDN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
43  30                         QUỸ ĐẦU TƯ TRÁI PHIẾU DFVN      DFIX     DFIX    None           DFIXN002  ...           0.90              1.0  TRADING_FUND  PRODUCT_ACTIVE     Quỹ trái phiếu   Quỹ mở
44  52                 QUỸ ĐẦU TƯ CỔ PHIẾU TRIỂN VỌNG NTP     NTPPF     TVPF    None           TVPFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
45  61                          QUỸ ĐẦU TƯ CÂN BẰNG PVCOM      PBIF     PBIF    None           PBIFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
46  86         QUỸ ĐẦU TƯ CỔ PHIẾU CỔ TỨC TĂNG TRƯỞNG KIM      KDEF     KDEF    None           KDEFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
47  83                   QUỸ ĐẦU TƯ THỊNH VƯỢNG RỒNG VIỆT     RVPIF   RVPF24    None         RVPF24N001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
48  82                  QUỸ ĐẦU TƯ THU NHẬP CHỦ ĐỘNG VCBF  VCBF-AIF  VCBFAIF    None        VCBFAIFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
49  80   QUỸ ĐẦU TƯ CỔ PHIẾU CỔ TỨC NĂNG ĐỘNG VINACAPITAL      VDEF     VDEF    None           VDEFN001  ...            NaN              0.0  TRADING_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
50  79                  QUỸ ĐẦU TƯ TĂNG TRƯỞNG THÀNH CÔNG      TCGF     TCGF    None           TCGFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
51  78      QUỸ ĐẦU TƯ UNITED THU NHẬP NĂNG ĐỘNG VIỆT NAM     UVDIF    UVDIF    None          UVDIFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cân bằng   Quỹ mở
52  76                    QUỸ ĐẦU TƯ NĂNG ĐỘNG LIGHTHOUSE     LHCDF    LHCDF    None          LHCDFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
53  75                      QUỸ ĐẦU TƯ BẢN VIỆT DISCOVERY    VCAMDF   VCAMDF    None         VCAMDFN001  ...            NaN              0.0      NEW_FUND  PRODUCT_ACTIVE       Quỹ cổ phiếu   Quỹ mở
```
</details>

#### 3.2 Thu thập dữ liệu về giao dịch trái phiếu
```python
fund.infor(id= 11, report_type='summary')
```
Trong đó:

  `id (str)`: Mã của quỹ

  `report_type (int)`: Kiểu báo cáo muốn lấy
    Bao gồm:
      - summary: Thông tin chung
      - holding_list: Danh sách cổ phiếu/trái phiếu chiếm % lớn trong danh mục quỹ
      - asset_list: Cơ cấu tài sản quỹ
      - industry_list: Cơ cấu danh mục quỹ theo ngành

<details>
  <summary>Output</summary>

```
fund.infor(id= 22, report_type='summary')

   id  code tradeCode    price       nav  managementFee performanceFee  totalAssetValue totalAssetValueStr     reportTime   riskLevel
0  22  VIBF  VIBFN003  10000.0  18112.39           1.75           None     861649450888           861.6 tỷ  1735664400000  Trung bình

fund.infor(id= 22, report_type='holding_list')

   id     stockCode   price  changeFromPrevious  changeFromPreviousPercent                    industry           type  netAssetPercent  updateAt tradeCode
0  22           MBB   24.60                0.50                       2.08                   Ngân hàng          STOCK             6.73  20250207  VIBFN003
1  22           FPT  141.30               -0.30                      -0.21      Công nghệ và thông tin          STOCK             4.14  20250207  VIBFN003
2  22           ACB   26.65                0.25                       0.95                   Ngân hàng          STOCK             3.75  20250207  VIBFN003
3  22           HPG   27.95                0.00                       0.00           Vật liệu xây dựng          STOCK             3.27  20250207  VIBFN003
4  22           STB   39.55                0.05                       0.13                   Ngân hàng          STOCK             3.25  20250207  VIBFN003
5  22           VEA   40.40                0.10                       0.25  Sản xuất Thiết bị, máy móc          STOCK             3.05  20250207  VIBFN003
6  22           CTG   41.80                0.15                       0.36                   Ngân hàng          STOCK             2.82  20250207  VIBFN003
7  22     TN1122016     NaN                 NaN                        NaN                Bất động sản           BOND             7.72  20250207  VIBFN003
8  22      KDH12202     NaN                 NaN                        NaN                Bất động sản  UNLISTED_BOND             4.02  20250207  VIBFN003
9  22  VN00DS150127     NaN                 NaN                        NaN                        Khác  UNLISTED_BOND             2.87  20250207  VIBFN003
```
</details>

## III. XÂY DỰNG BÁO CÁO THEO DÕI THỊ TRƯỜNG
*Liên hệ [Github](https://github.com/the-a1pha) hoặc [Linkedin](https://www.linkedin.com/in/bui-truong-an/) để nhận template và code xây dựng báo cáo*

## IV. XÂY DỰNG MÔ HÌNH CHẤM ĐIỂM VÀ ĐÁNH GIẤ THỊ TRƯỜNG, CỔ PHIẾU
*Liên hệ [Github](https://github.com/the-a1pha) hoặc [Linkedin](https://www.linkedin.com/in/bui-truong-an/) để nhận thêm thông tin*


















