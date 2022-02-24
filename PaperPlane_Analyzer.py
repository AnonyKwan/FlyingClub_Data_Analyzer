
import datetime
from time import sleep
import plotly.express as px
import streamlit as st
import pandas as pd
import random
import requests
import json

store_address = {  
  'MOD Public': '0X8578CFE80787835359A6B8B33CFA42BF299C8304',
  'Mod Sequel': '0X31CEF1A024EFBECDEDD099894B720032F69942E0',
  'Bar PUN': '0X6DC7A24D2F38BA02BE2123DDDD6EFEF7A60E7B58',
  'ROOM by Le Kief ': '0XDE9B673D94FB9BF4877F24BFE201DE6DEA3D7991',
  'g.o.a.t by GURU HOUSE': '0X8C5155151564318570964E6F99984E9C5E65BA2A',
  'no.MORE 莫忘衷初股份有限公司': '0XCE0F9F08E7549578E51112F42CD90049C8117089',
  'The Public House': '0XABCEF555B028AA6576EA80A34B3FC301EA0EA63A',
  "[tei] by O'bond": '0X6ED546F75F0407C3E65456874811377BAEB0599A',
  'Fourplay Cuisine': '0X7A0C64F2B8A2BA39C2A792423604083065512B4E',
  'Fourplay 2.0': '0X6F5E6FD5555CD1BFD67EBE6A8CA3D1597B4212CA',
  'INDULGE Bistro': '0X5A773D91C3A888EDAAE341C0FED007C0B88D2D39',
  '純愛小吃部': '0X5B48743F42DD21BEE2BCEB6AC2BCA3129E8E1B73',
  '栖.Habitat': '0XE1594DC5CEA70071B81E06FED9BBB514852014B7',
  'Vender Bar': '0XF14D93135BEEB0CA3D6B3AF35F7A0CCC040EF588',
  '舟舟 Bar Boat': '0X166CCBCE2493D2D43613AA44151DDC07DA680DF8',
  '安慰劑台中': '0X5CBB9E855FDF4667B3B552CAD493F8700C2DE984',
  'Tipsy Room': '0XFF543AE3BD3B8C3AB98A04C339AC5C0710DB9A71',
  'Bar TCRC': '0XEDDEBE2279AC31844CBE4DCE76CCBE31CCECE90E',
  'Bar Home': '0X81391946A00FB986F0DB74A6F83D47B2989FC064',
  '食上主義': '0X29F81BF509E05FDC034ADCB18D9E527847B45BC1',
  '酣呷': '0X1F56BFFBAB3987E960D71E1BFEBF6D106431C8C8'
  }

airdrop_address = ['0XFF252828972608B52A056AED2491412163504B06','0XF1EC1E30B3A84A1121C361D579511A167D9CCBF9','VKXWNXZ134PUJZ9874UU7W72CMYXTE7XG1']

api_key_list = ["4JIJWVNR8HJDJF44C37MF5UJAA3NFMZ5R2","FN7RPKGTW7UHXSA6FATIWXQD4M53R9MDF7","5BZDS26XVNHWU4SFJC7E99V7MENRSRSBCJ"]

# REVERSE store_address TO "ADDRESS" : "STORE NAME"
store_address_reverse = dict(map(reversed, store_address.items()))

def sidebar():
    # CSS FOR SIDEBAR
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 100px;
    }
    .css-nlntq9 e16nr0p30 {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    # SIDEBAR
    with st.sidebar.container():
        st.sidebar.image(paperplane_icon)
        sidebar_layout_title = st.sidebar.columns([1,5,1])
        with sidebar_layout_title[1]:
            st.title("OPENSEA STATS")

        # OPENSEA API FOR FLYINGCLUB STATS
        response = json.loads(requests.get("https://api.opensea.io/api/v1/collection/paperplane-by-flyingclubio/stats").text)

        sidebar_layout_0 = st.sidebar.columns([1,4,4,1])
        with sidebar_layout_0[0]:
            st.empty()
        with sidebar_layout_0[1]:
            num_items = int(response['stats']['count'])
            st.metric(label="紙飛機數量", value=num_items)     
        with sidebar_layout_0[2]:
            num_holders = int(response['stats']['num_owners'])
            st.metric(label="紙飛持有者", value=num_holders)
        with sidebar_layout_0[3]:
            st.empty()

        sidebar_layout_1 = st.sidebar.columns([1,4,4,1])
        with sidebar_layout_1[0]:
            st.empty()
        with sidebar_layout_1[1]:
            floor_price = response['stats']['floor_price']
            st.metric(label="當前地板價", value=floor_price)   
        with sidebar_layout_1[2]:
            thirty_day_volume = response['stats']['thirty_day_volume']
            st.metric(label="30日交易量", value=f"{thirty_day_volume:.1f} Ξ")
        with sidebar_layout_1[3]:
            st.empty()

def searchBar ():
    with st.container():
        searchbar_layout = st.columns([1,2,1])
        with searchbar_layout[1]:
            #Actual Search Bar
            wallet_address_user_input = st.text_input(label="",placeholder="請輸入錢包地址").lower()
        if len(wallet_address_user_input) == 42:
            wallet_address = wallet_address_user_input
            # POLYGON API FOR GETTING USER TRANSATIONS... CAN ONLY FETCH LAST 10000 RESULTS
            ramdon_api_key = random.choice(api_key_list)
            response = requests.get(f"https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=0x3Fb89b4385779a8513d73Aed99AC6E4b77C34821&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ramdon_api_key}").text
            # IF ADDRESS IS WRONG
            if int(json.loads(response)["status"]) == 0:
                st.warning("請重新輸入錢包地址")
            else:
                
                ## CALCULATION PROCESS
                ############################################################################
                redeem_info = json.loads(response)
                redeem_datetime = []
                redeem_store = []
                redeem_amount = []
                token_spent = 0
                token_remain = 0
                total_income = 0
                redeem_datetime_within_week = []
                redeem_store_within_week = []
                redeem_amount_within_week = []
                for transation in redeem_info['result']:
                    print (transation)
                    if  transation['to'].upper() in wallet_address.upper():
                        total_income += int(transation['value'][:-18])
                        continue
                    else:
                        # GET ALL TRANSATIONS
                        token_spent += int(transation['value'][:-18])
                        redeem_datetime.append(datetime.datetime.utcfromtimestamp(int(transation['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S %a'))
                        # IF STORE ADDRESS IN KEY : VALUE PAIR, USE THE NAME INSTATE
                        if transation['to'].upper() in [i for i in list(store_address_reverse.keys())]:
                            redeem_store.append(store_address_reverse[transation['to'].upper()])
                        else:
                            redeem_store.append(transation['to'])
                        redeem_amount.append(f"   {transation['value'][:-18]} NZ")

                        # GET LAST 7 DAYS TRANSATIONS
                        last_week = (datetime.datetime.now() - datetime.timedelta(days=7))
                        if last_week <= datetime.datetime.utcfromtimestamp(int(transation['timeStamp'])):
                            redeem_datetime_within_week.append(datetime.datetime.utcfromtimestamp(int(transation['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S %a'))
                            if transation['to'].upper() in [i for i in list(store_address_reverse.keys())]:
                                redeem_store_within_week.append(store_address_reverse[transation['to'].upper()])
                            else:
                                redeem_store_within_week.append(transation['to'])
                            redeem_amount_within_week.append(f"   {transation['value'][:-18]} NZ")
                ############################################################################

                # METRIC OUTPUT
                metric_layout = st.columns([1,3,2,2,2,1])
                with metric_layout[2]:
                    token_remain = total_income - token_spent
                    st.metric(label="剩餘 NZ", value=token_remain)   
                with metric_layout[3]:
                    st.metric(label="已用 NZ", value=token_spent)

                # DATAFRAME OUTPUT
                expander_layout = st.columns(3)
                with expander_layout[1]:
                    with st.expander("個人交易記錄 ( 7 日 )"):
                        # IF NONE TRANSATION WITIN LAST 7 DAYS, HIDE DATAFRAME
                        if len(redeem_datetime_within_week) != 0:
                            df = pd.DataFrame(
                                # [-9:] last 10 elements from list
                                    {"日期": reversed(redeem_datetime_within_week[-9:]), '交易錢包': reversed(redeem_store_within_week[-9:]),'交易數量': reversed(redeem_amount_within_week[-9:])})
                            st.table(df)
                            # st.dataframe NOT ABLE TO ADJUST WIDTH
                            # st.dataframe(df)
                        # FOR DEBUG ONLY
                        # st.json(json.loads(response))

        elif len(wallet_address_user_input) == 0:
            pass
        else:
            st.warning("請重新輸入錢包地址")

@st.cache(ttl=300)
def stores_transations_calculation ():
    store_address_list = list(store_address_reverse.keys())
    store_name_list = list(store_address.keys())
    stores_token_received = []
    total_store_income = 0
    store_transation_count_list = []
    store_transation_count = 0
    users_contributions = {}
    # API TO CHECK EACH STORE TRANSATIONS
    for wallet_address in store_address_list:
        # BECAUSE THE API CALL IS LIMITED, USING MULTIPLE APIKEY INSTATE OF ONE.
        ramdon_api_key = random.choice(api_key_list)
        print (f"Using API KEY: {ramdon_api_key}")
        response = requests.get(f"https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=0x3Fb89b4385779a8513d73Aed99AC6E4b77C34821&address={wallet_address.lower()}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ramdon_api_key}").text
        store_info = json.loads(response)
        for transation in store_info['result']:
            # IF RECEVING ADDRESS IS STORE ADDRESS
            print (transation)
            if  transation['to'].upper() in wallet_address:
                # GET LAST 30 DAYS TRANSATIONS
                last_month = (datetime.datetime.now() - datetime.timedelta(days=30))
                if last_month <= datetime.datetime.utcfromtimestamp(int(transation['timeStamp'])):   
                    # NOT ACCEPT TRANSATIONS FROM AIRDROP ADDRESS        
                    if transation['from'].upper() not in [i for i in airdrop_address] :
                        total_store_income += int(transation['value'][:-18])
                        store_transation_count += 1
                        # users_contributions[transation['from']] = {store_address_reverse[transation['to'].upper()]: {
                        #                                                                                             transation[
                        #                                                                                                 'hash']: {"Date":datetime.datetime.utcfromtimestamp(int(transation['timeStamp'])),
                        #      
                        #                                                                                                    "Spent":transation['value']}}}
        store_transation_count_list.append(store_transation_count)
        stores_token_received.append(total_store_income)
        total_store_income = 0
        store_transation_count = 0
    return store_name_list,stores_token_received,store_transation_count_list

def mainPageStoreChart():
    with st.container():
        store_name_list,stores_token_received,store_transation_count_list = stores_transations_calculation()    
        fig = px.bar( x=store_name_list, y=stores_token_received, color=store_transation_count_list,
                    labels=dict(x="兌換店家", y="兌換數量",color='兌換次數'),
                    title="28日兌換圖表"
                )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

# def mainPageContributionChart():


if __name__ == "__main__":
    paperplane_icon = 'https://flyingclub.io/assets/paperplane-3245df87512ef7c15e7b91cc0cdeae37109489f2c839fd48cb3674606e5fe0b3.png'
    st.set_page_config(
                        page_title="PaperPlane Analyzer",
                        page_icon=paperplane_icon,
                        layout="wide",
                        initial_sidebar_state="expanded"
                    )
    st.markdown("<h1 style='text-align: center;'>PaperPlane Analyzer</h1>", unsafe_allow_html=True)

    sidebar()
    searchBar()
    mainPageStoreChart()