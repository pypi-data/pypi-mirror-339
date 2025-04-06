# -*- coding: utf-8 -*-
"""
本模块功能：宏观经济基本面分析
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2025年3月9日
最新修订日期：2025年3月10日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
from siat.grafix import *
from siat.common import *
from siat.translate import *
#==============================================================================
import pandas as pd
from pandas_datareader import wb
import requests

#==============================================================================
if __name__=='__main__':
    key_words='GDP per capita'
    top=5; note=False
    
    indicator_wb(key_words='GDP',top=10,note=False)

def find_economic_indicator(key_words='GDP',top=10, \
                            note=False,translate=False,source='wb'):
    """
    ===========================================================================
    功能：查找宏观经济指标代码
    参数：
    key_words：关键词，支持多关键词，使用空格隔开，默认'GDP'
    top：显示最相似的若干个指标，默认10
    note：是否显示指标的描述，默认否False
    translate：是否调用AI大模型进行翻译，若翻译可能影响反应速度，默认否False
    source：信息来源，默认'wb'
    
    注意：有时网络可能拒绝访问，可以换个时段再次进行访问
    """
    if source=='wb':
        df=indicator_wb(key_words=key_words,top=top,note=note,translate=translate)
    else:
        print("  Sorry, the source option currently only supports wb (World Bank)")
        
    return

def indicator_wb(key_words='GDP',top=20,note=False,translate=False):
   """
   ============================================================================
   功能：在WB/IMF/FRED数据库中查找宏观经济指标的代码
   参数：
   key_words：可包括多个关键词，使用空格隔开，不区分大小写
   top：输出相似度最高的，默认5个
   note：是否显示每个指标的注释，默认False
   
   输出：基于文本相似度，输出可能的指标代码及其简介
   
   返回值：可能的指标代码及其简介
   """
   
   # 拆分关键词字符串为列表
   words_list=key_words.split(' ')
   
   # 循环查找每个关键词，并合成
   df=None
   for word in words_list:
       try:
           df_tmp=wb.search(word)
       except:
           print("  Sorry, data source rejected connection, try again later")
           return None
       
       # 合并
       if df is None:
           df=df_tmp
       else:
           df=pd.concat([df,df_tmp])
   
   # 去重
   df.drop_duplicates(subset=['id'],keep='first',inplace=True)
   
   # 去掉名称中的逗号、左右括号、美元符号和百分号，以免降低模糊匹配度
   import re
   #df['name2']=df['name'].apply(lambda x: re.sub('[(),$%]', '', x))
   df['name2']=df['name'].apply(lambda x: re.sub('[(),]', '', x))
   
   # 匹配相似度
   df2=fuzzy_search_wb(df,key_words=key_words,column='name2',top=top)
   
   # 遍历输出
   if len(df2)==0:
       print(f"Sorry, no indicator found with key words: {key_words}")
       return None
       
   #print('') #空一行
   for row in df2.itertuples():
       
       print(f"{row.id}",end=': ')
       if not translate:
           print(f"{row.name}",end='')
       else:
           print(f"{row.name}[{lang_auto2(row.name)}]",end='')
       if row.unit != '':
           print(f", unit: {row.unit}")
       else:
           print('')
       if note:
           if row.sourceNote != '':
               print(f"{row.sourceNote}")
               if translate:
                   print(f"{lang_auto2(row.sourceNote)}")
               print('') #空一行
   
   return df2

#==============================================================================
if __name__=='__main__':
    key_words='GDP per capita'
    column='name'
    top=10

def fuzzy_search_wb(df,key_words='GDP per capita',column='name',top=10):
    """
    ===========================================================================
    功能：给定key_words，模糊搜索df的column字段，列出匹配度最高的10个指标及其解释
    参数：
    df：wb.search产生的指标集
    column：需要搜索的字段名，默认'id'
    key_words：需要匹配的关键词组，默认'GDP'
    top：列出模糊匹配度最高的若干个指标，默认10
    
    输出：无
    返回：指标列表
    """
    
    # 将关键词组和列中的每个值都转换为小写单词集合
    def normalize_text(text):
        return set(text.lower().split())
    
    # 应用函数并比较集合
    df["normalized_"+column] = df[column].apply(normalize_text)
    key_words_set = normalize_text(key_words)
    
    # 计算相似度（基于集合的交集和并集）
    def calculate_similarity(text_set, key_words_set):
        intersection = text_set.intersection(key_words_set)
        union = text_set.union(key_words_set)
        return len(intersection) / len(union)
    
    df["similarity"] = df["normalized_"+column].apply(lambda x: calculate_similarity(x, key_words_set))

    # 按相似度降序
    df.sort_values(['similarity'], ascending = False, inplace=True)
    
    df2=df[['id','name','unit','sourceNote']].head(top)

    return df2
        
#==============================================================================
if __name__ =="__main__":
    indicator="NY.GDP.MKTP.KN"
    indicator="6.0.GDP_current"
    indicator="XYZ123"
    
    indicator_name_wb(indicator)

def indicator_name_wb(indicator):
    """
    ===========================================================================
    功能：抓取World Bank网页上指标的名称
    indicator：WB指标名称，例如'NY.GDP.MKTP.KN'
    """
    # 优先查询本地词典
    indicator_name=economic_translate(indicator)
    
    # 查询WB网页
    if indicator_name == indicator:
        # 构造 API 请求 URL
        url = f"https://api.worldbank.org/v2/indicator/{indicator}?format=json"
        
        # 发送请求
        response = requests.get(url)
        data = response.json()
        
        # 提取指标名称
        try:
            indicator_name = data[1][0]['name']
        except:
            indicator_name = indicator
    
    return indicator_name


#==============================================================================
if __name__ =="__main__":
    ticker='CN'; show_name=True
    check_country_code('ZWE',show_name=True)
    check_country_code('ZAF',show_name=True)
    check_country_code('cn',show_name=True)
    
def check_country_code(ticker='CN',show_name=False):
    """
    ===========================================================================
    功能：检查国家代码是否支持
    ticker：国家代码
    show_name：是否显示国家名称，默认否False
    
    返回值：若国家代码在列表中，True；否则，False
    """
    country_codes=wb.country_codes
    
    elements_to_remove = ['all','ALL','All']
    country_code_list = [x for x in country_codes if x not in elements_to_remove]
    
    result=False
    if ticker in country_code_list:
        result=True
        
    if show_name:
        if result:
            indicator='NY.GDP.MKTP.KN'
            df=economy_indicator_wb(ticker=ticker,indicator=indicator, \
                                  start='2000',graph=False)
            if not (df is None):
                if len(df) >= 1:
                    country_name=df['country'].values[0]
                    print(f"Country code {ticker} refers to {country_name}")
                else:
                    print(f"Country code {ticker} found, but its name not found")
            else:
                print(f"Found country code {ticker}, but its name not found")
        else:
            print(f"Country code {ticker} not found")
    
    return result


#==============================================================================
if __name__ =="__main__":
    ticker='CN'
    indicator="NY.GDP.MKTP.KN"
    indicator="GC.XPN.TOTL.GD.ZS"
    
    start='2010'; end='2025'; power=3
    
    zeroline=False
    attention_value=''; attention_value_area=''
    attention_point=''; attention_point_area=''
    average_value=False
    datatag=False; graph=True
    mark_top=True; mark_bottom=True; mark_end=True
    facecolor='whitesmoke';loc='best'
   
    
    df=economy_indicator_wb(ticker,indicator,start,end,power=3)

def economy_indicator_wb(ticker='CN',indicator='NY.GDP.MKTP.KN', \
                      start='L10Y',end='today',translate=False, \
                      zeroline=False, \
                           attention_value='',attention_value_area='', \
                           attention_point='',attention_point_area='', \
                      average_value=False, \
                      datatag=False,power=0,graph=True, \
                      mark_top=True,mark_bottom=True,mark_end=True, \
                      facecolor='whitesmoke',loc='best',maxticks=30):
    """
    ===========================================================================
    功能：绘制一个国家的一个宏观经济指标走势
    参数：
    ticker：国家编码，两位,默认'CN'
    indicator：宏观经济指标，默认GDP (constant LCU)，即本币不变价格GDP
    start：开始日期，默认近十年
    end：结束日期，默认当前日期
    zeroline：是否绘制零线，默认False
    attention_value：纵轴关注值或其列表，默认无''
    attention_value_area：纵轴关注值区间强调，默认无''
    attention_point：横轴关注值或其列表，默认无''
    attention_point_area：横轴关注值区间强调，默认无''
    average_value：是否绘制均值线，默认否False
    datatag：是否标记折线中的各个数据点的数值，默认否False
    power：是否绘制趋势线，默认否0
    graph：是否绘图，默认是True
    mark_top, mark_bottom, mark_end：是否标记最高、最低和末端点：默认是True
    facecolor：背景颜色，默认'whitesmoke'
    loc：图例位置，默认自动'best'
    
    输出：图形
    返回值：数据表
    """
    # 检测指标是否存在，并取得指标名称
    indicator_name=indicator_name_wb(indicator)
    if indicator_name == indicator:
        print(f"  #Error(economy_indicator_wb): indicator {indicator} not found")
        return None
    
    # 日期具体化    
    start,end=start_end_preprocess(start,end)
    
    # 下载数据
    try:
        pricedf=wb.download(indicator=indicator,country=ticker,start=start,end=end)
    except:
        print(f"  #Error(economy_indicator_wb): {indicator} deprecated or {ticker} not found")
        return None

    # 是否返回None
    if pricedf is None:
        print(f"  #Error(economy_indicator_wb): no data found on {indicator} in {ticker}")
        return None
    # 是否返回空的数据表
    if len(pricedf) == 0:
        print(f"  #Error(economy_indicator_wb): zero data found on {indicator} in {ticker}")
        return None
    # 是否返回数据表但内容均为NaN
    if pricedf[indicator].isnull().all():
        print(f"  #Error(economy_indicator_wb): empty data found on {indicator} in {ticker}")
        return None

    pricedf.reset_index(inplace=True)  
    pricedf.set_index('year',inplace=True)    
    pricedf.rename(columns={indicator:indicator_name},inplace=True)
    country=pricedf['country'].values[0]
    pricedf.sort_index(inplace=True)
    #pricedf.drop(columns='country',inplace=True)
    
    # 若不绘图则直接返回数据，不进行数量单位变换，否则后期对比可能产生数量级不一致问题
    if not graph:
        return pricedf
    
    erdf3=pricedf

    # 换算数量单位
    ind_max=erdf3[indicator_name].max()
    ind_min=erdf3[indicator_name].min()
    ind_median=erdf3[indicator_name].median()

    kilo=1000; million=kilo * 1000; billion=million * 1000
    trillion=billion * 1000; quadrillion=trillion * 1000
    
    if ind_median > quadrillion:
        unit=text_lang('单位：千万亿','in Quadrillions'); unit_amount=quadrillion
    elif ind_median > trillion:
        unit=text_lang('单位：万亿','in Trillions'); unit_amount=trillion
    elif ind_median > billion:
        unit=text_lang('单位：十亿','in Billions'); unit_amount=billion
    elif ind_median > million:
        unit=text_lang('单位：百万','in Millions'); unit_amount=million
    elif ind_median > kilo:
        unit=text_lang('单位：千','in Thousands'); unit_amount=kilo
    else:
        unit=''; unit_amount=1
        
    erdf3['unit']=unit; erdf3['unit_amount']=unit_amount
        
    if unit != '':
        erdf3[indicator_name]=erdf3[indicator_name].apply(lambda x: round(x/unit_amount,2))

    # 绘图
    """
    if not graph:
        return erdf3
    """
    # 判断是否绘制零线    
    if ind_max * ind_min <0:
        zeroline=True
    
    titletxt1=text_lang("经济分析","Economic Analysis")
    titletxt=titletxt1+': '+country_translate(country)+', '+indicator_name
    if unit != '':
        titletxt=titletxt+', '+unit
    
    import datetime; todaydt = datetime.date.today()
    sourcetxt=text_lang("数据来源：WB/IMF/FRED","Data source: World Bank")
    footnote=sourcetxt+', '+str(todaydt)
    collabel=indicator_name
    
    ylabeltxt=indicator_name
    
    # 为避免绘图出错，对空值进行插值
    erdf3.interpolate(method='linear',limit_direction='both',inplace=True)
    
    # 翻译：挪到绘图函数中
    """
    if translate:
        ylabeltxt=lang_auto2(ylabeltxt)
        titletxt=lang_auto2(titletxt)
    """
    try:
        plot_line(erdf3,indicator_name,collabel,ylabeltxt,titletxt,footnote,datatag=datatag, \
                  power=power,zeroline=zeroline, \
                  average_value=average_value, \
                      attention_value=attention_value,attention_value_area=attention_value_area, \
                      attention_point=attention_point,attention_point_area=attention_point_area, \
                  mark_top=mark_top,mark_bottom=mark_bottom,mark_end=mark_end, \
                  facecolor=facecolor,loc=loc,maxticks=30,translate=translate)
    except Exception as e:
        # 捕获所有异常
        print(f"  #Error(economy_indicator_wb)：{e}")
        print("  Details:")
        import traceback
        traceback.print_exc()
    
    return pricedf


#==============================================================
if __name__ =="__main__":
    ticker='CN'
    indicator=['NY.GDP.MKTP.CN','NY.GDP.MKTP.KN','NY.GDP.MKTP.CD','XYZ']
    start='2010'
    end='2025'
    
    attention_value=''; attention_value_area=''
    attention_point=''; attention_point_area=''
    band_area=''
    graph=True
    smooth=True
    loc='best'
    facecolor='whitesmoke'
    date_range=False
    date_freq=False
    annotate=False
    annotate_value=False
    mark_top=True; mark_bottom=True; mark_end=True
    maxticks=30
    
    df=economy_mindicators_wb(ticker,measures,fromdate,todate)

def economy_mindicators_wb(ticker='CN',indicator=['NY.GDP.MKTP.CN','NY.GDP.MKTP.KN'], \
                           start='L10Y',end='today', \
                               attention_value='',attention_value_area='', \
                               attention_point='',attention_point_area='', \
                               band_area='', \
                           graph=True,smooth=False,loc='best',facecolor='whitesmoke', \
                           date_range=False,date_freq=False, \
                           annotate=False,annotate_value=False, \
                           mark_top=False,mark_bottom=False,mark_end=False, \
                           maxticks=30,translate=False):
    """
    ===========================================================================
    功能：单个国家，多个宏观经济指标对比
    主要参数：
    ticker：国家代码，默认'CN'
    indicator：指标代码列表，默认['NY.GDP.MKTP.CN','NY.GDP.MKTP.KN']
    start：开始日期，默认'L10Y'
    end：截止日期，默认'today'
    attention_value：纵轴关注值或其列表，默认无''
    attention_value_area：纵轴关注值区间强调，默认无''
    attention_point：横轴关注值或其列表，默认无''
    attention_point_area：横轴关注值区间强调，默认无''
    band_area：两条曲线之间强调，默认无''
    graph：是否绘图，默认True
    loc：图例位置，默认自动'best'
    facecolor：画布背景颜色，默认'whitesmoke'
    annotate：是否在曲线末端标注，默认否False
    annotate_value：是否标注曲线末端值，默认否False
    mark_top, mark_bottom, mark_end：是否标注最大、最小、末端值，默认否
    maxticks=30：限制横轴刻度最大数量
    
    date_range=False：指定开始结束日期绘图
    date_freq=False：指定横轴日期间隔，例如'D'、'2D'、'W'、'M'等，横轴一般不超过25个标注，否则会重叠
    
    输出：图形
    返回值：数据表
    """
    DEBUG=False
    
    measures=indicator
    fromdate,todate=start_end_preprocess(start,end)
    
    #处理ticker，允许1个
    if isinstance(ticker,list):
        if len(ticker) >= 1:
            ticker=ticker[0]
        else:
            print("  #Error(economy_mindicators_wb): need at least 1 country to continue")
            return None

    #处理measures，允许多个
    if isinstance(measures,str):
        measures=[measures]

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    df=pd.DataFrame(); have_data=False
    indicator_list=[]
    for m in measures:
        print(f"  Searching indicator {m} ... ...")

        with HiddenPrints():
            dftmp=economy_indicator_wb(ticker=ticker,indicator=m, \
                                  start=fromdate,end=todate, \
                                  graph=False)
        if dftmp is None:
            print(f"  #Warning(economy_mindicators_wb): none found for {m} with {ticker}")
            continue
            #return None
        if len(dftmp) ==0:
            print(f"  #Warning(economy_mindicators_wb): empty record found on {m} for {ticker}")
            continue   
            #return None
        
        have_data=True
        
        country=dftmp['country'].values[0]
        dftmp.drop(columns=['country'],inplace=True)
        indicator_name=list(dftmp)[0]
        
        if m in band_area:
            band_area = [indicator_name if x == m else x for x in band_area]
        
        indicator_list=indicator_list+[indicator_name]
        
        if len(df)==0:
            df=dftmp
        else:
            df=pd.merge(df,dftmp,left_index=True,right_index=True)

    # 若不绘图则直接返回数据
    pricedf=df.copy()
    if not graph: return pricedf

    if not have_data:
        #print(f"  #Error(economy_mindicators_wb): no record found on {indicator} for {ticker}")
        return None
        
    # 绘图
    titletxt=text_lang("经济趋势分析","Economic Trend Analysis")+': '+country_translate(country)    

    y_label=text_lang('经济指标',"Economic Indicator")
    import datetime; todaydt = datetime.date.today()
    footnote2=text_lang("数据来源：WB/IMF/FRED","Data source: World Bank")+', '+str(todaydt)

    # 处理数量级问题
    max_val=min_val=0
    for c in list(df):
        max_tmp=df[c].max(); min_tmp=df[c].min()
        if max_val < max_tmp: max_val = max_tmp
        if min_val > min_tmp: min_val = min_tmp
    ind_median=(max_val + min_val) / 2
    
    kilo=1000; million=kilo * 1000; billion=million * 1000
    trillion=billion * 1000; quadrillion=trillion * 1000
    
    if ind_median > quadrillion:
        unit=text_lang('单位：千万亿','in Quadrillions'); unit_amount=quadrillion
    elif ind_median > trillion:
        unit=text_lang('单位：万亿','in Trillions'); unit_amount=trillion
    elif ind_median > billion:
        unit=text_lang('单位：十亿','in Billions'); unit_amount=billion
    elif ind_median > million:
        unit=text_lang('单位：百万','in Millions'); unit_amount=million
    elif ind_median > kilo:
        unit=text_lang('单位：千','in Thousands'); unit_amount=kilo
    else:
        unit=''; unit_amount=1    
    
    for c in list(df):
        df[c]=df[c].apply(lambda x: round(x/unit_amount,2) if x >= unit_amount else round(x/unit_amount,4))
    
    x_label=footnote2
    if unit != '':
        titletxt=titletxt+', '+unit
            
    x_label=footnote2

    axhline_value=0; axhline_label=''
    above_zero=0; below_zero=0
    for c in list(df):
        c_max=df[c].max(); c_min=df[c].min()
        try:
            if c_max>0 or c_min>0: above_zero+=1
            if c_max<0 or c_min<0: below_zero+=1                
        except: continue
        
    if above_zero>0 and below_zero>0: #有正有负
        if DEBUG:
            print("DEBUG: draw axhline=0")
        axhline_value=0
        axhline_label=text_lang('零线',"Zeroline")
    
    # 为避免绘图出错，对空值进行插值
    df.interpolate(method='linear',limit_direction='both',inplace=True)

    # 翻译指标名称
    for c in list(df):
        df.rename(columns={c:economic_translate(c)},inplace=True)
    
    draw_lines2(df,y_label,x_label,axhline_value,axhline_label,titletxt, \
               data_label=False,resample_freq='1D',smooth=smooth, \
               date_range=date_range,date_freq=date_freq,date_fmt='%Y-%m-%d', \
                    attention_value=attention_value,attention_value_area=attention_value_area, \
                    attention_point=attention_point,attention_point_area=attention_point_area, \
               annotate=annotate,annotate_value=annotate_value, \
               mark_top=mark_top,mark_bottom=mark_bottom,mark_end=mark_end,facecolor=facecolor, \
               band_area=band_area,loc=loc,maxticks=maxticks,translate=translate)

    return pricedf


#==============================================================================
if __name__ =="__main__":
    tickers=['CN','US','JP']
    indicator='NY.GDP.MKTP.PP.CD'    
    start='L20Y'; end='today'
    
    attention_value=''; attention_value_area=''
    attention_point=''; attention_point_area=''
    axhline_value=0; axhline_label=''
    preprocess='none'; linewidth=1.5
    scaling_option='start'
    plus_sign=False
    graph=True; loc='best'; facecolor='whitesmoke'
    annotate=False; annotate_value=False
    smooth=True
    mark_top=True; mark_bottom=True; mark_end=False
    maxticks=30    
    
    
    
def economy_mtickers_wb(ticker=['CN','US','JP'],indicator='NY.GDP.MKTP.PP.CD', \
                       start='L15Y',end='today', \
                        attention_value='',attention_value_area='', \
                        attention_point='',attention_point_area='', \
                      axhline_value=0,axhline_label='', \
                      preprocess='none',linewidth=1.5, \
                      scaling_option='start', \
                      plus_sign=False, \
                      graph=True,facecolor='whitesmoke', \
                      band_area='',loc='best', \
                      annotate=False,annotate_value=False, \
                      smooth=False, \
                      mark_top=True,mark_bottom=True,mark_end=False, \
                      maxticks=30,translate=False):
    """
    ===========================================================================
    功能：比较并绘制多个国家的单宏观经济指标曲线
    主要参数：
    ticker：国家代码，默认['CN','US','JP']
    indicator：宏观经济指标，默认'NY.GDP.MKTP.PP.CD'，即GDP PPP
    start：开始日期，默认'L20Y'
    end：截止日期，默认'today'
    attention_value：纵轴关注值或其列表，默认无''
    attention_value_area：纵轴关注区间强调，默认无''
    attention_point：横轴关注值或其列表，默认无''
    attention_point_area：横轴关注区间强调，默认无''
    preprocess：数据预处理，默认无'none'
    linewidth：曲线宽度，默认1.5
    scaling_option：数据缩放方法，默认'start'
    plus_sign：在缩放处理时，纵轴刻度是否带加减号，默认否False
    graph：是否绘图，默认是True
    loc：图例位置，默认自动处理'best'
    facecolor：画布背景颜色，默认'whitesmoke'
    annotate：是否标注曲线末端，默认否False
    annotate_value：是否标注曲线末端数值，默认否False
    mark_top：是否标注最大值，默认是True
    mark_bottom：是否标注最小值，默认是True
    mark_end：是否标注曲线末端值，默认否False
    maxticks：设定横轴刻度数量最大值，默认30
    
    注意：
    ticker中须含有2个及以上国家代码，
    indicator为单一指标，
    axhline_label不为空时绘制水平线
    
    preprocess：是否对绘图数据进行预处理，仅适用于指标数量级差异较大的数据，
    不适用于比例、比率和百分比等数量级较为一致的指标。
        standardize: 标准化处理，(x - mean(x))/std(x)
        normalize: 归一化处理，(x - min(x))/(max(x) - min(x))
        logarithm: 对数处理，np.log(x)
        scaling：缩放处理，五种选项scaling_option
        （mean均值，min最小值，start开始值，percentage相对每条曲线起点值的百分比，
        change%相对每条曲线起点值变化的百分比）
        change%方式的图形更接近于持有收益率(Exp Ret%)，设为默认的缩放方式。
    
    """
    DEBUG=False
    
    tickers=ticker; measure=indicator
    start,end=start_end_preprocess(start,end)
    
    tickers=upper_ticker(tickers)
    if not isinstance(tickers,list):
        tickers=[tickers]
    
    # 去掉重复代码：有必要，重复代码将导致后续处理出错KeyError: 0！
    tickers=list(set(tickers))

    if isinstance(measure,list):
        measure=measure[0]
    
    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout
    
    #循环获取指标
    #import pandas as pd
    #from functools import reduce

    dfs=pd.DataFrame(); have_data=False
    country_list=[]
    for t in tickers:
        print(f"  Looking for {measure} info in {t} ... ...")
        with HiddenPrints():
            df_tmp=economy_indicator_wb(ticker=t,indicator=measure, \
                                  start=start,end=end,graph=False)
        if df_tmp is None:
            print(f"  #Warning(economy_mticker_wb): {measure} info not found in {t}")
            continue
        if len(df_tmp)==0:
            print(f"  #Warning(economy_mticker_wb): zero info found for {measure} in {t}")
            continue

        have_data=True

        country=df_tmp['country'].values[0]
        country_list=country_list+[country]
        df_tmp.drop(columns=['country'],inplace=True)
        indicator_name=list(df_tmp)[0]
        
        if DEBUG:
            print(f"DEBUG: t={t}, band_area={band_area}, df_tmp={list(df_tmp)}")
            
        if t in band_area:
            band_area = [country if x == t else x for x in band_area]
         
        df_tmp.rename(columns={indicator_name:country},inplace=True)

        if len(dfs)==0:
            dfs=df_tmp
        else:
            dfs=pd.concat([dfs,df_tmp],axis=1,join='outer')
    
    # 翻译band_area
    band_area=[country_translate(x) for x in band_area]        
    
    if dfs is None:
        print(f"  #Error(economy_mticker_wb): no records found for {measure}")
        return None
    if len(dfs)==0:
        print(f"  #Error(economy_mticker_wb): zero records found for {measure}")
        return None

    # 若不绘图则返回原始数据
    pricedf=dfs.copy()
    if not graph: return pricedf

    if not have_data:
        #print(f"  #Error(economy_mticker_wb): no record found on {indicator} for {ticker}")
        return None

    # 绘图
    titletxt=text_lang("经济分析","Economic Analysis")+': '+indicator_name    
    #y_label=indicator_name
    y_label=text_lang("经济指标","Economic Indicator")
    
    import datetime; todaydt = datetime.date.today()
    footnote2=text_lang("数据来源：WB/IMF/FRED","Data source: WB/IMF/FRED")+', '+str(todaydt)

    # 处理数量级问题
    max_val=min_val=0
    for c in list(dfs):
        max_tmp=dfs[c].max(); min_tmp=dfs[c].min()
        if max_val < max_tmp: max_val = max_tmp
        if min_val > min_tmp: min_val = min_tmp
    ind_median=(max_val + min_val) / 2
    
    kilo=1000; million=kilo * 1000; billion=million * 1000
    trillion=billion * 1000; quadrillion=trillion * 1000
    
    if ind_median > quadrillion:
        unit=text_lang('单位：千万亿','in Quadrillions'); unit_amount=quadrillion
    elif ind_median > trillion:
        unit=text_lang('单位：万亿','in Trillions'); unit_amount=trillion
    elif ind_median > billion:
        unit=text_lang('单位：十亿','in Billions'); unit_amount=billion
    elif ind_median > million:
        unit=text_lang('单位：百万','in Millions'); unit_amount=million
    elif ind_median > kilo:
        unit=text_lang('单位：千','in Thousands'); unit_amount=kilo
    else:
        unit=''; unit_amount=1    
    
    for c in list(dfs):
        dfs[c]=dfs[c].apply(lambda x: round(x/unit_amount,2) if x >= unit_amount else round(x/unit_amount,4))

    x_label=footnote2
        
    if preprocess == 'scaling' and scaling_option == 'change%':
        title_txt2=text_lang("增减幅度%","Change%")
        titletxt=titletxt+', '+title_txt2            
        axhline_value=0
        axhline_label="零线"
    else:
        if unit != '' and preprocess == 'none':
            titletxt=titletxt+', '+unit

    # 为避免出错，对空值进行插值
    dfs.interpolate(method='linear',limit_direction='both',inplace=True)
    # 标准化处理
    try:
        dfs2,axhline_label,x_label,y_label,plus_sign=df_preprocess(dfs,measure, \
                axhline_label=axhline_label,x_label=x_label,y_label=y_label, \
                preprocess=preprocess,scaling_option=scaling_option)
    except:
        print("  #Error(economy_mticker_wb): preprocess failed, returning dfs for further check")
        return dfs

    if DEBUG:
        print("DEBUG: dfs2=",list(dfs2))
        
    above_zero=0; below_zero=0
    for c in list(dfs2):
        c_max=dfs2[c].max(); c_min=dfs2[c].min()
        try:
            if c_max>0 or c_min>0: above_zero+=1
            if c_max<0 or c_min<0: below_zero+=1
        except: continue

    if DEBUG:
        print("DEBUG: above_zero=",above_zero,'below_zero=',below_zero)
    
    if above_zero>0 and below_zero>0: #有正有负
        if axhline_label=='':
            axhline_label='零线'

    # 翻译国家名称
    for c in list(dfs2):
        dfs2.rename(columns={c:country_translate(c)},inplace=True)

    draw_lines(dfs2,y_label,x_label,axhline_value,axhline_label,titletxt, \
               data_label=False,resample_freq='D',smooth=smooth,linewidth=linewidth, \
               band_area=band_area,loc=loc, \
                    attention_value=attention_value,attention_value_area=attention_value_area, \
                    attention_point=attention_point,attention_point_area=attention_point_area, \
               annotate=annotate,annotate_value=annotate_value,plus_sign=plus_sign, \
               mark_top=mark_top,mark_bottom=mark_bottom,mark_end=mark_end,facecolor=facecolor, \
               maxticks_enable=False,maxticks=10, \
               translate=translate)

    return pricedf

#==============================================================================


def economy_trend2(ticker='CN',indicator='NY.GDP.MKTP.KN', \
                   start='L10Y',end='today',translate=False, \
                   attention_value='',attention_value_area='', \
                   attention_point='',attention_point_area='', \
                   mark_top=False,mark_bottom=False,mark_end=False, \
                   graph=True,facecolor='whitesmoke',loc='best',maxticks=30, \
                   
                   zeroline=False,average_value=False, \
                   datatag=False,power=0, \
                   
                   annotate=False,annotate_value=False,smooth=False, \
                       
                   band_area='',date_range=False,date_freq=False, \
                       
                   axhline_value=0,axhline_label='', \
                   preprocess='none',linewidth=1.5, \
                   scaling_option='start', \
                   plus_sign=False, \
                   ):
    """
    功能：分析宏观经济指标，支持单国家单指标、多国家单指标、单国家多指标
    主要公共参数：
    ticker：国家编码，两位或三位ISO编码，默认'CN'
    indicator：宏观经济指标，默认GDP (constant LCU)，即本币不变价格GDP
    start：开始日期，默认近十年
    end：结束日期，默认当前日期
    attention_value：纵轴关注值或其列表，默认无''
    attention_value_area：纵轴关注值区间强调，默认无''
    attention_point：横轴关注值或其列表，默认无''
    attention_point_area：横轴关注值区间强调，默认无''        
    graph：是否绘图，默认是True
    mark_top, mark_bottom, mark_end：是否标记最高、最低和末端点：默认是True
    facecolor：背景颜色，默认'whitesmoke'
    loc：图例位置，默认自动'best'

    仅支持单国家单指标的参数：
    zeroline：是否绘制零线，默认False        
    average_value：是否绘制均值线，默认否False
    datatag：是否标记折线中的各个数据点的数值，默认否False
    power：是否绘制趋势线，默认否0    
    
    支持多国家单指标、单国家多指标的参数：
    annotate：是否在曲线末端标注，默认否False
    annotate_value：是否标注曲线末端值，默认否False    
    
    仅支持单国家多指标的参数：
    band_area：两条曲线之间强调，默认无''
    date_range：指定开始结束日期绘图，默认False
    date_freq：指定横轴日期间隔，默认False。
        可指定'D'、'2D'、'W'、'M'等，横轴一般不超过25个标注，否则会重叠    
    
    仅支持多国家单指标的参数：
    preprocess：数据预处理，默认无'none'
    scaling_option：数据缩放方法，默认'start'，仅当preprocess为非'none'时有效
    plus_sign：在缩放处理时，纵轴刻度是否带加减号，默认否False    
    linewidth：曲线宽度，默认1.5

    输出：绘图
    返回值：数据表
    
    其他：套壳函数    
    """
    # 判断ticker个数
    ticker_num=0
    if isinstance(ticker,str): 
        ticker_num=1
        ticker=ticker.upper()
        if not check_country_code(ticker=ticker,show_name=False):
            print(f"  #Warning(economy_trend2): country code {ticker} not found")
            return None
        
    if isinstance(ticker,list):
        ticker=[x.upper() for x in ticker]
        for t in ticker:
            if not check_country_code(ticker=t,show_name=False):
                ticker.remove(t)
                print(f"  #Warning(economy_trend2): country code {t} not found")
        if len(ticker)==0:
            return None
        
        if len(ticker)==1: 
            ticker_num=1
            ticker=ticker[0]
        else:
            ticker_num=len(ticker)
    
    # 判断indicator个数
    indicator_num=0
    if isinstance(indicator,str): indicator_num=1
    if isinstance(indicator,list):
        if len(indicator)==1: 
            indicator_num=1
            indicator=indicator[0]
        else:
            indicator_num=len(indicator)
            
    # 单国家+单指标
    if ticker_num==1 and indicator_num==1:
        df=economy_indicator_wb(ticker=ticker,indicator=indicator, \
                                start=start,end=end,translate=translate, \
                                attention_value=attention_value, \
                                attention_value_area=attention_value_area, \
                                attention_point=attention_point, \
                                attention_point_area=attention_point_area, \
                                mark_top=mark_top,mark_bottom=mark_bottom,mark_end=mark_end, \
                                graph=graph,facecolor=facecolor,loc=loc,maxticks=maxticks, \
                                
                                power=power,average_value=average_value, \
                                zeroline=zeroline,datatag=datatag)
        return df
            
    # 多国家：仅使用第一个指标
    if ticker_num > 1:
        df=economy_mtickers_wb(ticker=ticker,indicator=indicator, \
                               start=start,end=end,translate=translate, \
                               attention_value=attention_value, \
                               attention_value_area=attention_value_area, \
                               attention_point=attention_point, \
                               attention_point_area=attention_point_area, \
                               mark_top=mark_top,mark_bottom=mark_bottom,mark_end=mark_end, \
                               graph=graph,loc=loc,facecolor=facecolor,maxticks=maxticks, \
                               band_area=band_area, \
                               annotate=annotate,annotate_value=annotate_value,smooth=smooth, \
                                   
                               preprocess=preprocess,scaling_option=scaling_option, \
                               plus_sign=plus_sign,linewidth=linewidth, \
                               axhline_value=axhline_value,axhline_label=axhline_label)
        return df
            
    # 单国家：使用多个指标
    if ticker_num == 1 and indicator_num > 1:
        df=economy_mindicators_wb(ticker=ticker,indicator=indicator, \
                                  start=start,end=end,translate=translate, \
                                  attention_value=attention_value, \
                                  attention_value_area=attention_value_area, \
                                  attention_point=attention_point, \
                                  attention_point_area=attention_point_area, \
                                  mark_top=mark_top,mark_bottom=mark_bottom,mark_end=mark_end, \
                                  graph=graph,facecolor=facecolor,loc=loc,maxticks=maxticks, \
                                      
                                  annotate=annotate,annotate_value=annotate_value,smooth=smooth, \
                                      
                                  band_area=band_area, \
                                  date_range=date_range,date_freq=date_freq)
        return df

    print(" #Warning: need at least 1 country and at leats 1 indicator")
    
    return None    
    
    
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================


def economic_translate(indicator):
    """
    ===========================================================================
    功能：翻译宏观经济指标术语
    参数：
    indicator: 指标编码，主要是世界银行编码。
    注意：部分编码已放弃，可能无数据或无最新数据。
    返回值：是否找到，基于语言环境为中文或英文解释。
    语言环境判断为check_language()
    
    数据结构：['指标编码','中文解释','英文解释']
    """
    DEBUG=False
    
    import pandas as pd
    trans_dict=pd.DataFrame([
        
        # NE.CON.PRVT:家庭及NPISH最终消费=======================================
        ['NE.CON.PRVT.CD','家庭及NPISH最终消费(美元时价)',
         'Household & NPISHs Final Consumption (current US$)',
         'Households and NPISHs Final consumption expenditure (current US$)'],
        
        ['NE.CON.PRVT.KD','家庭及NPISH最终消费(2015美元不变价格)',
         'Household & NPISHs Final Consumption (constant 2015 US$)',
         'Households and NPISHs Final consumption expenditure (constant 2015 US$)'],
        
        ['NE.CON.PRVT.CN','家庭及NPISH最终消费(本币时价)',
         'Household & NPISHs Final Consumption (current LCU)',
         'Households and NPISHs Final consumption expenditure (current LCU)'],
        
        ['NE.CON.PRVT.KN','家庭及NPISH最终消费(本币不变价格)',
         'Household & NPISHs Final Consumption (constant LCU)',
         'Households and NPISHs Final consumption expenditure (constant LCU)'],

        ['NE.CON.PRVT.ZS','家庭及NPISH最终消费(占GDP%)',
         'Household & NPISHs Final Consumption (GDP%)',
         'Households and NPISHs Final consumption expenditure (% of GDP)'],

        ['NE.CON.PRVT.KD.ZG','家庭及NPISH最终消费(年增速%)',
         'Household & NPISHs Final Consumption (annual % growth)',
         'Households and NPISHs Final consumption expenditure (annual % growth)'],

        ['NE.CON.PRVT.PP.CD','家庭及NPISH最终消费(购买力平价，国际美元时价)',
         'Household & NPISHs Final Consumption (PPP, current intl $)',
         'Households and NPISHs Final consumption expenditure, PPP (current international $)'],

        ['NE.CON.PRVT.PP.KD','家庭及NPISH最终消费(购买力平价，2021国际美元不变价格)',
         'Household & NPISHs Final Consumption (PPP, constant 2021 intl $)',
         'Households and NPISHs Final consumption expenditure, PPP (constant 2021 international $)'],

        ['NE.CON.PRVT.PC.KD.ZG','人均家庭及NPISH最终消费(年增速%)',
         'Household & NPISHs Final Consumption per capita growth (annual %)',
         'Households and NPISHs Final consumption expenditure per capita growth (annual %)'],

        ['NE.CON.PRVT.PC.KD','人均家庭及NPISH最终消费(2015美元不变价格)',
         'Household & NPISHs Final Consumption per capita (constant 2015 US$)',
         'Households and NPISHs Final consumption expenditure per capita (constant 2015 US$)'],

        ['NE.CON.PRVT.CN.AD','家庭及NPISH最终消费(统计口径调整后，本币时价)',
         'Household & NPISHs Final Consumption (linked series, current LCU)',
         'Households and NPISHs Final consumption expenditure: linked series (current LCU)'],
        
        # 币种指标：CD=current US$, KD=constant 2015 US$, CN=current LCU
        # KN=constant LCU, ZS=% of GDP, PC=per capita, PP=PPP
        
        
        
        
        
        
        ], columns=['indicator','cword','eword','original_eword'])

    found=False; result=indicator
    try:
        dict_word=trans_dict[trans_dict['indicator']==indicator]
        found=True
    except:
        #未查到翻译词汇，返回原词
        pass
    
    if dict_word is None:
        found=False    
    elif len(dict_word) == 0:
        found=False
    
    if found:
        lang=check_language()
        
        if DEBUG:
            print(f"DEBUG: indicator={indicator}, lang={lang}, dict_word={dict_word}")
        
        if lang == 'Chinese':
            result=dict_word['cword'].values[0]
        else:
            result=dict_word['eword'].values[0]
            
    return result

if __name__=='__main__': 
    indicator='NE.CON.PRVT.CD'
    indicator='NE.CON.PRVT.KD'

    indicator='NE.CON.PRVT.CN'
    indicator='NE.CON.PRVT.KN'
    
    result=economic_translate(indicator)
    economic_translate(indicator)[1]

#==============================================================================


def country_translate(country):
    """
    ===========================================================================
    功能：翻译国家名称
    参数：
    country: 国家名称英文，并非国家代码。
    返回值：是否找到，基于语言环境为中文或英文解释。
    语言环境判断为check_language()
    
    数据结构：['国家名称英文','国家名称中文','国家代码2位','国家代码3位']
    """
    
    import pandas as pd
    trans_dict=pd.DataFrame([
        
        ['China','中国','CN','CHN'],
        ['United States','美国','US','USA'],
        ['Japan','日本','JP','JPN'],
        ['Germany','德国','DE','DEU'],
        ['India','印度','IN','IND'],
        ['Brazil','巴西','BR','BRA'],
        
        ['France','法国','FR','FRA'],
        ['United Kingdom','英国','GB','GBR'],
        ['Russian Federation','俄罗斯','RU','RUS'],
        ['Canada','加拿大','CA','CAN'],
        ['Australia','澳大利亚','AU','AUS'],
        ['Korea, Rep.','韩国','KR','KOR'],
        
        ['Italy','意大利','IT','ITA'],
        ['Mexico','墨西哥','MX','MEX'],
        ['South Africa','南非','ZA','ZAF'],
        ['Saudi Arabia','沙特阿拉伯','SA','SAU'],
        ['Indonesia','印度尼西亚','ID','IDN'],
        ['Turkiye','土耳其','TR','TUR'],
        
        ['Argentina','阿根廷','AR','ARG'],
        ['Egypt','埃及','EG','EGY'],
        ['European Union','欧盟','EU','EUU'],
        ['Hong Kong SAR, China','中国香港','HK','HKG'],
        ['Taiwan, China','中国台湾','TW','TWN'],
        ['World','全球','1W','WLD'],
        
        ['Singapore','新加坡','SG','SGP'],
        ['Malaysia','马来西亚','MY','MYS'],
        ['Thailand','泰国','TH','THA'],
        ['Israel','以色列','IL','ISR'],
        ['Vietnam','越南','VN','VNM'],
        ['Philippines','菲律宾','PH','PHL'],
        ['Brunei','文莱','BN','BRN'],
        ['Cambodia','柬埔寨','KH','KHM'],
        
        ['Laos','老挝','LA','LAO'],
        ['Myanmar','缅甸','MM','MMR'],
        
        
        
        
        
        ], columns=['ecountry','ccountry','country code2','country code3'])

    found=False; result=country
    try:
        dict_word=trans_dict[trans_dict['ecountry']==country]
        found=True
    except:
        #未查到翻译词汇，返回原词
        pass
    
    if dict_word is None:
        found=False    
    elif len(dict_word) == 0:
        found=False
    
    if found:
        lang=check_language()
        if lang == 'Chinese':
            result=dict_word['ccountry'].values[0]
        else:
            #result=dict_word['ecountry'].values[0]
            pass
            
    return result

if __name__=='__main__': 
    country='China'
    country='United States'
    
    result=country_translate(country)

#==============================================================================
    