
from __future__ import annotations

from datetime import date, timedelta
import io
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import streamlit as st


st.set_page_config(page_title="U.S. Government Debt Analytics | Mountain Path Academy", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

NAVY, BLUE, GOLD, DARK_GOLD = "#0B2545", "#0B5CAD", "#F3C84B", "#D4A017"
TEAL, GREEN, RED, PURPLE, ORANGE = "#13A89E", "#2E8B57", "#E45756", "#7C3AED", "#F28E2B"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}.stApp{background:linear-gradient(180deg,#F7F9FC,#EEF3F8)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0B2545,#153F69)}[data-testid="stSidebar"] *{color:#F4F8FC!important}
.hero{background:linear-gradient(115deg,#081F3A 0%,#124A78 70%,#A97908 150%);padding:31px 35px;border-radius:20px;color:white;box-shadow:0 12px 32px rgba(6,27,52,.18);margin-bottom:18px}.hero h1{font-size:2.2rem;margin:0 0 8px;color:white;font-weight:900}.hero p{margin:0;color:#D6E9F5;font-size:1.02rem;line-height:1.55}.eyebrow{color:#F3C84B;text-transform:uppercase;letter-spacing:.12em;font-weight:800;font-size:.75rem;margin-bottom:.55rem}
.section-title{font-size:1.4rem;font-weight:900;color:#0B2545;margin:18px 0 8px}.concept-card{background:white;border:1px solid #D9E5EF;border-top:5px solid #0B5CAD;padding:17px 18px;border-radius:15px;box-shadow:0 5px 16px rgba(18,54,84,.07);min-height:160px}.concept-card h3{color:#0B2545;font-size:1.04rem;margin:0 0 7px}.concept-card p{color:#3C5368;font-size:.9rem;line-height:1.5;margin:0}.formula{background:linear-gradient(135deg,#FFF9E6,#FFF1B8);border:1px solid #E8C45B;border-left:6px solid #D4A017;padding:14px 18px;border-radius:12px;color:#3D3006;font-weight:800;margin:8px 0 14px}.teaching-note{background:#EAF7F5;border-left:5px solid #13A89E;padding:13px 16px;border-radius:10px;color:#153C3A;margin:10px 0}.warning-note{background:#FFF3E8;border-left:5px solid #F28E2B;padding:13px 16px;border-radius:10px;color:#57300A;margin:10px 0}
.selected-confirmation{margin:-4px 0 10px;padding:7px 10px;background:#F3C84B;border:1px solid #D4A017;border-radius:8px;color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;font-size:.84rem;font-weight:800}.profile-card{background:linear-gradient(135deg,#071A2F,#123B65);border:1px solid rgba(243,200,75,.42);border-radius:14px;padding:17px;margin:15px 0 8px;box-shadow:0 7px 20px rgba(0,0,0,.18)}.profile-card .name{color:#F3C84B!important;font-weight:850;font-size:1rem;margin:0 0 5px}.profile-card .title{color:#D7E9FA!important;font-size:.81rem;line-height:1.4}.profile-card .stats{color:#AFC7DE!important;font-size:.76rem}.profile-card a{color:#F3C84B!important;text-decoration:none;font-size:.78rem;font-weight:750;margin-right:10px}
.about-section{background:linear-gradient(125deg,#0B2545,#123F69);color:#EAF3FC;border:1px solid rgba(212,160,23,.45);border-radius:17px;padding:26px 30px;margin:24px 0 12px}.about-section h3{color:#F3C84B!important}.about-section p{color:#EAF3FC;line-height:1.62}.highlight{color:#F3C84B;font-weight:800}.academy-link{display:inline-block;margin-top:10px;padding:8px 16px;background:#D4A017;color:#071A2F!important;border-radius:8px;text-decoration:none;font-weight:850}.mp-footer{text-align:center;padding:23px 0 8px;border-top:1px solid rgba(212,160,23,.4);color:#64778B;font-size:.84rem}.mp-footer .brand{color:#0B2545;font-size:1.12rem;font-weight:850}.mp-footer a{color:#0B4F86;text-decoration:none;font-weight:750;margin:0 7px}
[data-testid="stMetric"]{background:#FFF;border:1px solid #DFE9F1;padding:14px;border-radius:14px;box-shadow:0 5px 16px rgba(18,54,84,.06)}.stTabs [data-baseweb="tab-list"]{gap:10px!important;flex-wrap:wrap!important;background:#D7E1EC!important;padding:10px!important;border:1px solid #B8C8D8!important;border-radius:14px!important;box-shadow:0 4px 14px rgba(11,37,69,.12)!important}.stTabs button[data-baseweb="tab"]{flex:1 1 165px!important;min-height:52px!important;background:#0B2545!important;border:2px solid #F3C84B!important;border-radius:10px!important;color:#F3C84B!important;box-shadow:0 3px 8px rgba(11,37,69,.22)!important}.stTabs button[data-baseweb="tab"] p{color:#F3C84B!important;-webkit-text-fill-color:#F3C84B!important;font-weight:850!important}.stTabs button[data-baseweb="tab"]:hover{background:#164E7A!important;transform:translateY(-1px)!important}.stTabs button[data-baseweb="tab"][aria-selected="true"]{background:linear-gradient(135deg,#F3C84B,#D4A017)!important;border-color:#A97908!important}.stTabs button[data-baseweb="tab"][aria-selected="true"] p{color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;font-weight:900!important}.stTabs [data-baseweb="tab-highlight"]{display:none!important}
.stButton button,.stDownloadButton button{background:#0B3B67!important;color:white!important;border-radius:10px!important;font-weight:800!important}.stButton button:hover,.stDownloadButton button:hover{background:#D4A017!important;color:#071A2F!important}section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"]>div{background:#FFF!important;border:2px solid #F3C84B!important;border-radius:10px!important}section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] *{color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;font-weight:800!important}section[data-testid="stSidebar"] div[data-testid="stButton"] button{background:linear-gradient(135deg,#F3C84B,#D4A017)!important;color:#071A2F!important;border:2px solid #F9DC79!important;min-height:46px!important;font-weight:850!important}
/* Sidebar labels must remain visible; field values stay navy on white. */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > label p,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] label p,
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] label p{color:#F3C84B!important;-webkit-text-fill-color:#F3C84B!important;background:transparent!important;font-weight:850!important;opacity:1!important}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] p,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] svg{color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;fill:#071A2F!important;opacity:1!important}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div *,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [role="button"],
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [role="button"] *,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] input,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] input::placeholder{color:#071A2F!important;-webkit-text-fill-color:#071A2F!important;caret-color:#071A2F!important;fill:#071A2F!important;stroke:#071A2F!important;font-weight:850!important;opacity:1!important}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"]{background:#FFF!important;color:#071A2F!important;-webkit-text-fill-color:#071A2F!important}
</style>""", unsafe_allow_html=True)

MATURITY_ORDER=["1 Mo","3 Mo","6 Mo","1 Yr","2 Yr","3 Yr","5 Yr","7 Yr","10 Yr","20 Yr","30 Yr"]
XML_TAGS={"BC_1MONTH":"1 Mo","BC_3MONTH":"3 Mo","BC_6MONTH":"6 Mo","BC_1YEAR":"1 Yr","BC_2YEAR":"2 Yr","BC_3YEAR":"3 Yr","BC_5YEAR":"5 Yr","BC_7YEAR":"7 Yr","BC_10YEAR":"10 Yr","BC_20YEAR":"20 Yr","BC_30YEAR":"30 Yr"}
FISCAL_BASE="https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

def section(title): st.markdown(f"<div class='section-title'>{title}</div>",unsafe_allow_html=True)
def note(text,warning=False): st.markdown(f"<div class='{'warning-note' if warning else 'teaching-note'}'>{text}</div>",unsafe_allow_html=True)
def card(title,body,color=BLUE): return f"<div class='concept-card' style='border-top-color:{color}'><h3>{title}</h3><p>{body}</p></div>"
def style_fig(fig,height=430):
    fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="white",font=dict(family="Inter",color=NAVY),margin=dict(l=35,r=25,t=60,b=35),legend=dict(orientation="h",y=1.08),hovermode="x unified"); fig.update_xaxes(gridcolor="#E7EEF4"); fig.update_yaxes(gridcolor="#E7EEF4"); return fig
def trillions(x): return f"${x/1e12:,.2f}T"

class _TableParser(HTMLParser):
    """Small dependency-free HTML table reader for official Treasury/Fed tables."""
    def __init__(self):
        super().__init__(); self.tables=[]; self.table=None; self.row=None; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=="table": self.table=[]
        elif tag=="tr" and self.table is not None: self.row=[]
        elif tag in ("td","th") and self.row is not None: self.cell=[]
    def handle_data(self,data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ("td","th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split())); self.cell=None
        elif tag=="tr" and self.row is not None:
            if any(self.row): self.table.append(self.row)
            self.row=None
        elif tag=="table" and self.table is not None:
            if self.table: self.tables.append(self.table)
            self.table=None

def html_tables(text):
    parser=_TableParser(); parser.feed(text); return parser.tables

@st.cache_data(ttl=1800,show_spinner=False)
def fiscal_api(path,params):
    response=requests.get(f"{FISCAL_BASE}/{path}",params=params,timeout=25); response.raise_for_status(); payload=response.json(); data=payload.get("data",[])
    if not data: raise ValueError(f"Fiscal Data returned no observations for {path}.")
    return pd.DataFrame(data)

@st.cache_data(ttl=1800,show_spinner=False)
def load_debt_history(years):
    start=(date.today()-timedelta(days=365*years+20)).isoformat()
    df=fiscal_api("v2/accounting/od/debt_to_penny",{"filter":f"record_date:gte:{start}","sort":"record_date","page[size]":"10000"})
    df["record_date"]=pd.to_datetime(df["record_date"])
    for c in ["debt_held_public_amt","intragov_hold_amt","tot_pub_debt_out_amt"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    return df.set_index("record_date").sort_index()

@st.cache_data(ttl=21600,show_spinner=False)
def load_historical_debt():
    df=fiscal_api("v2/accounting/od/debt_outstanding",{"sort":"record_date","page[size]":"500"})
    df["record_date"]=pd.to_datetime(df["record_date"]); df["debt_outstanding_amt"]=pd.to_numeric(df["debt_outstanding_amt"],errors="coerce"); return df.set_index("record_date").sort_index()

@st.cache_data(ttl=21600,show_spinner=False)
def load_interest_expense(years):
    start=(date.today()-timedelta(days=365*years+20)).isoformat()
    df=fiscal_api("v2/accounting/od/interest_expense",{"filter":f"record_date:gte:{start}","sort":"record_date","page[size]":"10000"})
    df["record_date"]=pd.to_datetime(df["record_date"])
    amount_col=next(c for c in ["interest_expense_amt","month_expense_amt","fytd_expense_amt"] if c in df.columns)
    df[amount_col]=pd.to_numeric(df[amount_col],errors="coerce")
    return df,amount_col

@st.cache_data(ttl=3600,show_spinner=False)
def load_curve(years):
    frames=[]
    for year in range(date.today().year-years,date.today().year+1):
        url=f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value={year}"
        response=requests.get(url,timeout=20); response.raise_for_status(); root=ET.fromstring(response.content); rows=[]
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            props=entry.find(".//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties")
            if props is None: continue
            record={child.tag.split("}")[-1]:child.text for child in props}
            if "NEW_DATE" not in record: continue
            row={"Date":pd.to_datetime(record["NEW_DATE"])}
            for source,label in XML_TAGS.items(): row[label]=pd.to_numeric(record.get(source),errors="coerce")
            rows.append(row)
        if rows: frames.append(pd.DataFrame(rows))
    if not frames: raise ValueError("Treasury curve feed returned no data.")
    return pd.concat(frames).drop_duplicates("Date").set_index("Date").sort_index()[MATURITY_ORDER]

@st.cache_data(ttl=21600,show_spinner=False)
def load_foreign_holders():
    """Latest Treasury TIC Major Foreign Holders table, billions of dollars."""
    url="https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/slt_table5.html"
    response=requests.get(url,timeout=25); response.raise_for_status(); tables=html_tables(response.text)
    rows=next(t for t in tables if any(any("Country" in cell for cell in row) for row in t) and len(t)>5)
    header_index=next(i for i,row in enumerate(rows) if any("Country" in cell for cell in row)); header=rows[header_index]
    width=len(header); data=[row[:width]+[""]*max(0,width-len(row)) for row in rows[header_index+1:] if len(row)>=2]
    table=pd.DataFrame(data,columns=header)
    country_col=next(c for c in table.columns if "country" in c.lower()); value_cols=[c for c in table.columns if c!=country_col and pd.to_numeric(table[c].astype(str).str.replace(",",""),errors="coerce").notna().sum()>3]
    if not value_cols: raise ValueError("TIC table did not contain a numeric holdings column.")
    latest_col=value_cols[0]; out=table[[country_col,latest_col]].rename(columns={country_col:"Country",latest_col:"Holdings ($bn)"})
    out["Country"]=out["Country"].astype(str).str.replace(r"\s*\d+/.*$","",regex=True).str.strip(); out["Holdings ($bn)"]=pd.to_numeric(out["Holdings ($bn)"].astype(str).str.replace(",",""),errors="coerce")
    out=out.dropna().query("`Holdings ($bn)` > 0"); out=out[~out["Country"].str.contains("Total|All Other|Grand",case=False,na=False)]
    return out.sort_values("Holdings ($bn)",ascending=False),str(latest_col)

@st.cache_data(ttl=21600,show_spinner=False)
def load_stakeholder_holdings():
    """Latest Federal Reserve Financial Accounts F3.2.s holder levels, $bn."""
    url="https://www.federalreserve.gov/releases/z1/current/html/F3_2_s.htm"
    response=requests.get(url,timeout=25); response.raise_for_status(); tables=html_tables(response.text)
    rows=next(t for t in tables if any(any("Series"==cell or "Series" in cell for cell in row) for row in t) and len(t)>10)
    header_index=next(i for i,row in enumerate(rows) if any("Series"==cell or "Series" in cell for cell in row)); header=rows[header_index]; width=len(header)
    data=[row[:width]+[""]*max(0,width-len(row)) for row in rows[header_index+1:] if len(row)>=3]; table=pd.DataFrame(data,columns=header)
    series_col=next(c for c in table.columns if "series" in c.lower()); desc_col=next(c for c in table.columns if "description" in c.lower())
    numeric_cols=[c for c in table.columns if c not in [series_col,desc_col] and "line" not in c.lower() and pd.to_numeric(table[c].astype(str).str.replace(",",""),errors="coerce").notna().sum()>5]
    if not numeric_cols: raise ValueError("Federal Reserve table did not contain quarterly levels.")
    latest_col=numeric_cols[-1]
    targets={
        "LM153061105":"Households & nonprofits","FL103061103":"Nonfinancial corporations","FL113061003":"Noncorporate business","FL213061103":"State & local governments","FL763061100":"U.S.-chartered banks","FL743061103":"Affiliated-area banks","FL753061103":"Foreign banking offices","FL403061105":"Government-sponsored enterprises","FL583061105":"Insurance & pension funds","FL473061105":"Credit unions","FL663061105":"Brokers & dealers","FL633061105":"Money market funds","FL653061105":"Mutual funds","FL553061103":"Closed-end funds","FL563061103":"ETFs","FL673061103":"Asset-backed issuers","FL733061103":"Holding companies","FL263061105":"Rest of world","FL713061103":"Federal Reserve","FL503061123":"Other financial business",
    }
    rows=[]
    for code,label in targets.items():
        match=table[table[series_col].astype(str).str.contains(code,regex=False,na=False)]
        if not match.empty:
            value=pd.to_numeric(str(match.iloc[0][latest_col]).replace(",",""),errors="coerce")
            if pd.notna(value): rows.append({"Stakeholder":label,"Holdings ($bn)":float(value)})
    if len(rows)<5: raise ValueError("Federal Reserve holder rows could not be identified.")
    out=pd.DataFrame(rows)
    category_map={"U.S.-chartered banks":"Banks & credit unions","Affiliated-area banks":"Banks & credit unions","Foreign banking offices":"Banks & credit unions","Credit unions":"Banks & credit unions","Mutual funds":"Investment funds","Money market funds":"Investment funds","Closed-end funds":"Investment funds","ETFs":"Investment funds","Insurance & pension funds":"Insurance & pensions","Households & nonprofits":"Households & nonprofits","Nonfinancial corporations":"Businesses","Noncorporate business":"Businesses","State & local governments":"State & local governments","Government-sponsored enterprises":"Other financial institutions","Brokers & dealers":"Other financial institutions","Asset-backed issuers":"Other financial institutions","Holding companies":"Other financial institutions","Other financial business":"Other financial institutions","Rest of world":"Rest of world","Federal Reserve":"Federal Reserve"}
    out["Category"]=out["Stakeholder"].map(category_map).fillna("Other")
    grouped=out.groupby("Category",as_index=False)["Holdings ($bn)"].sum().sort_values("Holdings ($bn)",ascending=False)
    return grouped,out,str(latest_col)

def demo_data(years):
    rng=np.random.default_rng(27); idx=pd.bdate_range(end=pd.Timestamp.today(),periods=max(252*years,260)); total=np.linspace(31e12,38e12,len(idx))+np.cumsum(rng.normal(0,9e9,len(idx))); public=total*.79+np.cumsum(rng.normal(0,1e9,len(idx))); debt=pd.DataFrame({"debt_held_public_amt":public,"intragov_hold_amt":total-public,"tot_pub_debt_out_amt":total},index=idx)
    annual_idx=pd.date_range("1995-09-30",pd.Timestamp.today(),freq="YE-SEP"); hist=pd.DataFrame({"debt_outstanding_amt":5e12*np.exp(np.linspace(0,np.log(7.4),len(annual_idx)))},index=annual_idx)
    curve_base=np.array([4.4,4.35,4.25,4.1,4.0,3.95,4.05,4.2,4.4,4.85,4.78]); curve=pd.DataFrame([curve_base+rng.normal(0,.12,len(curve_base)) for _ in idx],index=idx,columns=MATURITY_ORDER)
    interest=pd.DataFrame({"record_date":pd.date_range(end=pd.Timestamp.today(),periods=years*12,freq="ME"),"interest_expense_amt":np.linspace(45e9,90e9,years*12)}); return debt,hist,interest,"interest_expense_amt",curve

def demo_holders():
    countries=pd.DataFrame({"Country":["Japan","China","United Kingdom","Belgium","Luxembourg","Cayman Islands","Canada","France","Ireland","Switzerland"],"Holdings ($bn)":[1130,780,760,410,405,390,365,345,330,300]})
    stakeholders=pd.DataFrame({"Category":["Rest of world","Investment funds","Households & nonprofits","Federal Reserve","Insurance & pensions","Banks & credit unions","State & local governments","Businesses","Other financial institutions"],"Holdings ($bn)":[8900,5200,3040,4300,1800,1600,1500,300,1200]})
    return countries,"Classroom snapshot",stakeholders,stakeholders.copy(),"Classroom quarter"

def excel_download(debt,historical,interest,interest_col,curve,countries,stakeholders,source):
    out=io.BytesIO()
    with pd.ExcelWriter(out,engine="xlsxwriter",datetime_format="dd-mmm-yyyy") as writer:
        book=writer.book; title=book.add_format({"bold":True,"font_color":"#FFFFFF","bg_color":NAVY,"font_size":18}); header=book.add_format({"bold":True,"font_color":"#FFFFFF","bg_color":NAVY,"align":"center"}); currency=book.add_format({"num_format":"$#,##0,,\"M\";[Red]($#,##0,,\"M\")"}); note_fmt=book.add_format({"bg_color":"#FFF1B8","font_color":NAVY,"text_wrap":True})
        latest=debt.iloc[-1]; summary=book.add_worksheet("Debt Dashboard"); summary.hide_gridlines(2); summary.set_column("A:A",30); summary.set_column("B:B",22); summary.merge_range("A1:F1","U.S. Government Debt Analytics",title); summary.write("A3","Latest official date",header); summary.write_datetime("B3",debt.index[-1].to_pydatetime(),book.add_format({"num_format":"dd-mmm-yyyy"})); labels=[("Total public debt outstanding",latest["tot_pub_debt_out_amt"]),("Debt held by the public",latest["debt_held_public_amt"]),("Intragovernmental holdings",latest["intragov_hold_amt"])]
        for i,(label,value) in enumerate(labels,5): summary.write(i,0,label); summary.write_number(i,1,value,currency)
        summary.merge_range("D3:F8",f"Source: {source}. Debt to the Penny is reported daily with the previous business day's data. Educational analysis only.",note_fmt)
        for name,df in [("Daily Debt",debt.reset_index()),("Historical FY Debt",historical.reset_index()),("Interest Expense",interest),("Treasury Curve",curve.reset_index()),("Foreign Holders",countries),("Stakeholder Holdings",stakeholders)]:
            df.to_excel(writer,sheet_name=name,index=False,startrow=1); ws=writer.sheets[name]; ws.freeze_panes(2,1); ws.autofilter(1,0,len(df)+1,len(df.columns)-1); ws.merge_range(0,0,0,len(df.columns)-1,name,title); ws.set_column(0,0,15); ws.set_column(1,len(df.columns)-1,20)
        guide=book.add_worksheet("Learning Guide"); guide.hide_gridlines(2); guide.set_column("A:A",28); guide.set_column("B:B",90); guide.merge_range("A1:B1","U.S. Government Debt Learning Guide",title); guide.write_row("A3",["Concept","Meaning"],header)
        lessons=[("Debt held by the public","Federal debt held outside federal government accounts, including investors, the Federal Reserve, foreign holders and other entities."),("Intragovernmental holdings","Treasury securities held by federal trust funds, revolving funds and special funds."),("Total public debt outstanding","Debt held by the public plus intragovernmental holdings; it is a stock, not the annual deficit."),("Deficit","Annual flow by which spending exceeds revenue; deficits generally add to debt."),("Interest expense","Budget cost influenced by the debt stock, maturity mix and rates at which securities are issued or refinanced."),("Yield curve","Market financing context across Treasury maturities; it is not the same as the government's average interest cost.")]
        for i,(a,b) in enumerate(lessons,3): guide.write(i,0,a,book.add_format({"bold":True,"bg_color":"#EAF1F7"})); guide.write(i,1,b,book.add_format({"text_wrap":True})); guide.set_row(i,40)
    return out.getvalue()

with st.sidebar:
    st.markdown("## 🏛️ Government Debt Controls")
    years=st.selectbox("Daily analysis window",[1,3,5,10],index=1,format_func=lambda x:f"{x} year" if x==1 else f"{x} years")
    growth_window=st.selectbox("Growth comparison",[30,90,365],index=2,format_func=lambda x:f"{x} days")
    focus_maturity=st.selectbox("Treasury financing context",MATURITY_ORDER,index=8)
    st.markdown(f'<div class="selected-confirmation">Focus: Federal debt · {focus_maturity} yield context</div>',unsafe_allow_html=True)
    use_demo=st.toggle("Use classroom simulation",False)
    if st.button("↻ Refresh Official Data",use_container_width=True): st.cache_data.clear(); st.rerun()
    st.caption("Primary sources: U.S. Treasury Fiscal Data and U.S. Treasury daily par yield curve. Data is published on source schedules, not tick-by-tick.")
    st.markdown("""<div class='profile-card'><p class='name'>Prof. V. Ravichandran</p><p class='title'>Visiting Professor &amp; Professor of Practice at Leading Business Schools<br>Founder — The Mountain Path Academy</p><p class='stats'>28+ years industry experience · 12+ years teaching Finance &amp; Financial Analytics</p><a href='https://themountainpathacademy.com' target='_blank'>🏔️ Academy</a><a href='https://www.linkedin.com/in/trichyravis' target='_blank'>LinkedIn</a><a href='https://github.com/trichyravis' target='_blank'>GitHub</a></div>""",unsafe_allow_html=True)

source="U.S. Treasury Fiscal Data + Treasury yield-curve feed"
if use_demo: debt,historical,interest,interest_col,curve=demo_data(years); source="Reproducible classroom simulation"
else:
    try:
        debt=load_debt_history(years)
    except Exception as exc:
        debt,historical,interest,interest_col,curve=demo_data(years); source="Reproducible classroom simulation"; st.warning(f"The primary Debt to the Penny feed is unavailable ({exc}). Showing classroom data.")
    else:
        demo_debt,demo_historical,demo_interest,demo_interest_col,demo_curve=demo_data(years)
        try: historical=load_historical_debt()
        except Exception as exc: historical=demo_historical; st.warning(f"Historical fiscal-year debt is temporarily unavailable ({exc}). Other official data remains live.")
        try: interest,interest_col=load_interest_expense(max(years,3))
        except Exception as exc: interest,interest_col=demo_interest,demo_interest_col; st.warning(f"Interest-expense data is temporarily unavailable ({exc}). Other official data remains live.")
        try: curve=load_curve(years)
        except Exception as exc: curve=demo_curve; st.warning(f"Treasury yield-curve data is temporarily unavailable ({exc}). Other official data remains live.")

if use_demo:
    countries,country_period,stakeholders,stakeholder_detail,stakeholder_period=demo_holders()
else:
    demo_countries,demo_country_period,demo_stakeholders,demo_stakeholder_detail,demo_stakeholder_period=demo_holders()
    try: countries,country_period=load_foreign_holders()
    except Exception as exc: countries,country_period=demo_countries,demo_country_period; st.warning(f"Country-holder data is temporarily unavailable ({exc}). A clearly labelled classroom snapshot is shown in that tab.")
    try: stakeholders,stakeholder_detail,stakeholder_period=load_stakeholder_holdings()
    except Exception as exc: stakeholders,stakeholder_detail,stakeholder_period=demo_stakeholders,demo_stakeholder_detail,demo_stakeholder_period; st.warning(f"Federal Reserve stakeholder data is temporarily unavailable ({exc}). A clearly labelled classroom snapshot is shown in that tab.")

latest=debt.iloc[-1]; comparison=debt.iloc[max(0,len(debt)-growth_window-1)]; debt_change=latest["tot_pub_debt_out_amt"]-comparison["tot_pub_debt_out_amt"]; public_share=latest["debt_held_public_amt"]/latest["tot_pub_debt_out_amt"]
st.markdown("""<div class='hero'><div class='eyebrow'>The Mountain Path Academy · Sovereign Finance Analytics</div><h1>U.S. Government Debt — Real-Time Analysis & Learning Studio</h1><p>Track the federal debt stock, public versus intragovernmental holdings, long-run growth, interest cost and Treasury financing environment using official government data.</p></div>""",unsafe_allow_html=True)
k1,k2,k3,k4,k5=st.columns(5); k1.metric("Total federal debt",trillions(latest["tot_pub_debt_out_amt"])); k2.metric("Held by the public",trillions(latest["debt_held_public_amt"])); k3.metric("Intragovernmental",trillions(latest["intragov_hold_amt"])); k4.metric(f"Change · {growth_window}D",trillions(debt_change)); k5.metric("Public share",f"{public_share:.1%}")
st.caption(f"Latest debt date: {debt.index[-1]:%d %b %Y} · {source}")

tabs=st.tabs(["📊 Analysis", "🧩 Debt composition", "🌍 Who holds the debt?", "💸 Interest cost", "📈 Financing context", "🎓 Educative", "🧪 Practice & download"])

with tabs[0]:
    section("Federal debt dashboard")
    fig=go.Figure(); fig.add_trace(go.Scatter(x=debt.index,y=debt["debt_held_public_amt"]/1e12,name="Held by public",stackgroup="one",line=dict(color=BLUE))); fig.add_trace(go.Scatter(x=debt.index,y=debt["intragov_hold_amt"]/1e12,name="Intragovernmental",stackgroup="one",line=dict(color=GOLD))); fig.update_layout(title="Daily federal debt outstanding"); fig.update_yaxes(title="$ trillion"); st.plotly_chart(style_fig(fig,500),use_container_width=True)
    a,b,c=st.columns(3); a.markdown(card("Debt is a stock",f"The latest total is {trillions(latest['tot_pub_debt_out_amt'])}. It accumulates past borrowing and changes daily with financing operations.",BLUE),unsafe_allow_html=True); b.markdown(card("The deficit is a flow","A fiscal deficit measures spending minus revenue over a period. It usually increases debt, but cash-balance and financing adjustments can make the daily link less direct.",ORANGE),unsafe_allow_html=True); c.markdown(card("Who holds it?",f"About {public_share:.1%} is held by the public; the remainder is mainly held by federal government accounts.",TEAL),unsafe_allow_html=True)
    section("Long-run fiscal-year debt history")
    fig=go.Figure(go.Bar(x=historical.index,y=historical["debt_outstanding_amt"]/1e12,marker_color=BLUE)); fig.update_layout(title="Debt outstanding at fiscal year-end"); fig.update_yaxes(title="$ trillion"); st.plotly_chart(style_fig(fig),use_container_width=True)
    hist=historical["debt_outstanding_amt"].dropna(); years_elapsed=max((hist.index[-1]-hist.index[0]).days/365.25,1); cagr=(hist.iloc[-1]/hist.iloc[0])**(1/years_elapsed)-1; note(f"Across the available fiscal-year history, nominal debt grew at approximately {cagr:.1%} per year. Nominal growth should be interpreted alongside inflation, GDP, revenue and debt-service capacity.")

with tabs[1]:
    section("Public and intragovernmental components")
    pie=go.Figure(go.Pie(labels=["Debt held by the public","Intragovernmental holdings"],values=[latest["debt_held_public_amt"],latest["intragov_hold_amt"]],hole=.58,marker_colors=[BLUE,GOLD],textinfo="label+percent")); pie.update_layout(title=f"Composition as of {debt.index[-1]:%d %b %Y}"); st.plotly_chart(style_fig(pie,450),use_container_width=True)
    changes=debt[["debt_held_public_amt","intragov_hold_amt","tot_pub_debt_out_amt"]].resample("ME").last().diff()/1e9; changes.columns=["Held by public","Intragovernmental","Total debt"]
    fig=go.Figure();
    for name,color in [("Held by public",BLUE),("Intragovernmental",GOLD),("Total debt",PURPLE)]: fig.add_trace(go.Bar(x=changes.index,y=changes[name],name=name,marker_color=color))
    fig.update_layout(title="Month-end change in debt components",barmode="group"); fig.update_yaxes(title="$ billion"); st.plotly_chart(style_fig(fig,480),use_container_width=True)
    note("Debt held by the public includes Treasury securities held by investors, Federal Reserve Banks, foreign governments and other entities outside federal government accounts. It is not synonymous with foreign-held debt.",warning=True)

with tabs[2]:
    section("Who holds marketable U.S. Treasury securities?")
    note("This ownership view uses Federal Reserve Financial Accounts levels for marketable Treasury securities. It differs from Debt to the Penny in scope, valuation and publication date, so the amounts should not be expected to reconcile exactly.",warning=True)
    left,right=st.columns([1.25,1])
    with left:
        fig=go.Figure(go.Bar(x=stakeholders["Holdings ($bn)"],y=stakeholders["Category"],orientation="h",marker_color=[BLUE,TEAL,GOLD,PURPLE,RED,ORANGE,GREEN,"#64748B","#94A3B8"][:len(stakeholders)])); fig.update_layout(title=f"Investor sectors · latest available {stakeholder_period}"); fig.update_xaxes(title="$ billion"); fig.update_yaxes(categoryorder="total ascending"); st.plotly_chart(style_fig(fig,520),use_container_width=True)
    with right:
        fig=go.Figure(go.Pie(labels=stakeholders["Category"],values=stakeholders["Holdings ($bn)"],hole=.55,textinfo="label+percent")); fig.update_layout(title="Share of reported marketable Treasury holdings"); st.plotly_chart(style_fig(fig,520),use_container_width=True)
    s1,s2,s3,s4=st.columns(4)
    def holder_value(label):
        row=stakeholders.loc[stakeholders["Category"]==label,"Holdings ($bn)"]; return float(row.iloc[0]) if not row.empty else 0.0
    s1.metric("Rest of world",f"${holder_value('Rest of world')/1000:,.2f}T"); s2.metric("Federal Reserve",f"${holder_value('Federal Reserve')/1000:,.2f}T"); s3.metric("Investment funds",f"${holder_value('Investment funds')/1000:,.2f}T"); s4.metric("Households & nonprofits",f"${holder_value('Households & nonprofits')/1000:,.2f}T")

    section("Major foreign holders by country")
    top_n=st.slider("Number of countries to display",5,20,12,key="country_count")
    top_countries=countries.head(top_n).sort_values("Holdings ($bn)")
    fig=go.Figure(go.Bar(x=top_countries["Holdings ($bn)"],y=top_countries["Country"],orientation="h",marker_color=TEAL,text=top_countries["Holdings ($bn)"].map(lambda x:f"${x:,.0f}B"),textposition="outside")); fig.update_layout(title=f"Major foreign holders of U.S. Treasury securities · {country_period}"); fig.update_xaxes(title="$ billion"); st.plotly_chart(style_fig(fig,560),use_container_width=True)
    c1,c2,c3=st.columns(3); c1.metric("Countries shown",f"{len(top_countries)}"); c2.metric("Top-country holdings",f"${countries.iloc[0]['Holdings ($bn)']:,.1f}B"); c3.metric("Top-country name",str(countries.iloc[0]["Country"]))
    note("TIC country attribution is generally based on the location of the foreign holder or custodian reported to the system. Holdings routed through financial centres can obscure the ultimate beneficial owner. Country data covers foreign holdings of Treasury securities—not each country's share of total federal debt.",warning=True)
    with st.expander("Detailed Federal Reserve stakeholder rows"):
        st.dataframe(stakeholder_detail.style.format({"Holdings ($bn)":"${:,.1f}"}),use_container_width=True,hide_index=True)

with tabs[3]:
    section("Interest expense and refinancing pressure")
    monthly=interest.copy(); monthly["record_date"]=pd.to_datetime(monthly["record_date"]); monthly=monthly.set_index("record_date").sort_index(); series=monthly[interest_col].dropna()
    fig=go.Figure(go.Bar(x=series.index,y=series/1e9,marker_color=RED)); fig.update_layout(title="Reported interest expense on the public debt"); fig.update_yaxes(title="$ billion"); st.plotly_chart(style_fig(fig,480),use_container_width=True)
    recent12=series.tail(12).sum(); prior12=series.iloc[-24:-12].sum() if len(series)>=24 else np.nan; i1,i2,i3=st.columns(3); i1.metric("Latest reported period",f"${series.iloc[-1]/1e9:,.1f}B"); i2.metric("Sum of latest 12 records",f"${recent12/1e9:,.1f}B"); i3.metric("Change vs prior 12",f"{recent12/prior12-1:+.1%}" if pd.notna(prior12) and prior12 else "—")
    c1,c2,c3=st.columns(3); c1.markdown(card("Debt stock", "More principal outstanding generally raises interest cost, all else equal.",BLUE),unsafe_allow_html=True); c2.markdown(card("Average financing rate", "Interest cost reprices gradually as bills, notes and bonds mature and are refinanced at prevailing rates.",RED),unsafe_allow_html=True); c3.markdown(card("Maturity structure", "A shorter maturity profile transmits rate changes faster; longer maturities lock funding costs for more time.",PURPLE),unsafe_allow_html=True)
    note("Do not divide one monthly expense observation by total debt to infer an annual effective rate. Fiscal-year totals, accrual conventions and average debt balances must be aligned.",warning=True)

with tabs[4]:
    section("Treasury yield environment")
    current=curve.iloc[-1]; fig=go.Figure(go.Scatter(x=MATURITY_ORDER,y=current.values,mode="lines+markers",line=dict(color=GOLD,width=3),marker=dict(size=9))); fig.update_layout(title=f"Current Treasury par yield curve · {curve.index[-1]:%d %b %Y}"); fig.update_yaxes(title="Yield (%)"); st.plotly_chart(style_fig(fig,450),use_container_width=True)
    fig=go.Figure(go.Scatter(x=curve.index,y=curve[focus_maturity],line=dict(color=BLUE,width=2.5))); fig.update_layout(title=f"{focus_maturity} Treasury yield history"); fig.update_yaxes(title="Yield (%)"); st.plotly_chart(style_fig(fig,430),use_container_width=True)
    spread=(current["10 Yr"]-current["2 Yr"])*100; f1,f2,f3=st.columns(3); f1.metric("Selected yield",f"{current[focus_maturity]:.2f}%"); f2.metric("2s10s spread",f"{spread:+.0f} bp"); f3.metric("Curve date",f"{curve.index[-1]:%d %b %Y}")
    note("Current market yields affect new borrowing immediately and the existing debt stock gradually through refinancing. The par curve is not the government's weighted-average interest rate.")

with tabs[5]:
    section("Understanding U.S. government debt")
    lessons=[[("Why debt exists","The federal government borrows when spending and other outflows exceed revenues and other inflows. Treasury securities finance the resulting cash need.",BLUE),("Debt held by public","Held outside federal government accounts. This component is central to analysis of market financing needs and macroeconomic crowding-out risk.",TEAL),("Intragovernmental","Claims held by trust funds and other government accounts. They are real Treasury obligations but represent internal government financing relationships.",GOLD)],[("Bills, notes and bonds","Bills mature within one year; notes generally span 2–10 years; bonds extend longer. TIPS and FRNs add inflation-linked and floating-rate structures.",PURPLE),("Debt sustainability","Depends on growth, primary balances, interest rates, inflation, maturity structure and institutional credibility—not on the nominal debt number alone.",RED),("Debt limit","A statutory borrowing constraint; it does not itself authorise spending. Appropriations, revenues and prior obligations determine financing needs.",ORANGE)]]
    for row in lessons:
        cols=st.columns(3)
        for col,item in zip(cols,row): col.markdown(card(*item),unsafe_allow_html=True)
    section("Analytical framework")
    st.markdown("<div class='formula'>Change in debt ≈ Primary deficit + Interest expense + Other financing adjustments</div>",unsafe_allow_html=True)
    q1,q2,q3,q4=st.columns(4); q1.markdown(card("Scale","Compare debt held by public with GDP and federal revenue.",BLUE),unsafe_allow_html=True); q2.markdown(card("Flow","Track primary deficit and interest expense.",ORANGE),unsafe_allow_html=True); q3.markdown(card("Cost","Assess average rate, refinancing and maturity mix.",RED),unsafe_allow_html=True); q4.markdown(card("Demand","Monitor auctions, investor demand and term premium.",TEAL),unsafe_allow_html=True)
    with st.expander("Common misconceptions"):
        st.markdown("- The national debt is not the same as the annual deficit.\n- Debt held by the public is not all foreign-owned.\n- Intragovernmental holdings are not eliminated from total debt outstanding.\n- A household analogy is incomplete because the federal government taxes, issues currency-denominated debt and operates without a fixed lifespan.\n- A rising nominal debt level does not by itself measure sustainability; debt service and economic capacity matter.")

with tabs[6]:
    section("Knowledge check")
    questions=[("Total public debt outstanding equals…",["debt held by public plus intragovernmental holdings","annual spending minus revenue only","foreign holdings only"],0),("The federal deficit is…",["a flow measured over a period","the same as total debt","Treasury interest rate"],0),("Higher market yields affect interest cost…",["gradually as debt is issued and refinanced","never","only after all debt matures"],0),("Debt held by the public includes…",["domestic, foreign and Federal Reserve holdings outside federal accounts","only foreign governments","only commercial banks"],0)]
    answers=[st.radio(f"{i+1}. {q}",opts,index=None,key=f"q{i}") for i,(q,opts,_) in enumerate(questions)]
    if st.button("Score my answers"):
        if any(a is None for a in answers): st.warning("Please answer every question.")
        else: st.success(f"Score: {sum(a==opts[c] for a,(_,opts,c) in zip(answers,questions))}/{len(questions)}")
    section("Download the formatted government-debt workbook")
    workbook=excel_download(debt,historical,interest,interest_col,curve,countries,stakeholders,source)
    st.download_button("⬇ Download U.S. Government Debt Analysis",workbook,"US_Government_Debt_Analysis.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
    st.caption("Includes dashboard metrics, daily Debt to the Penny history, fiscal-year debt, interest expense, Treasury curve history and a learning guide.")

st.markdown("""<div class='about-section'><h3>About This Project</h3><p>Developed by <span class='highlight'>Prof. V. Ravichandran</span>, Visiting Professor &amp; Professor of Practice at Leading Business Schools and founder of <span class='highlight'>The Mountain Path Academy</span>.</p><p>Drawing on <span class='highlight'>28+ years of industry experience</span> and <span class='highlight'>12+ years of teaching</span>, this dashboard turns official U.S. fiscal and Treasury data into a practical, classroom-ready sovereign-debt learning experience.</p><a class='academy-link' href='https://themountainpathacademy.com' target='_blank'>🏔️ Visit The Mountain Path Academy</a></div><div class='mp-footer'><div class='brand'>🏔️ The Mountain Path Academy</div><div>Prof. V. Ravichandran · Applied Finance &amp; Financial Analytics</div><div><a href='https://themountainpathacademy.com' target='_blank'>Academy</a><a href='https://www.linkedin.com/in/trichyravis' target='_blank'>LinkedIn</a><a href='https://github.com/trichyravis' target='_blank'>GitHub</a></div><div style='margin-top:10px'>Educational analytics project · Not policy or investment advice · © 2026</div></div>""",unsafe_allow_html=True)
