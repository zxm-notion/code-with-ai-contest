import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

DATA_PATH = "data/signal_samples.csv"

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def get_color_by_rsrp(rsrp):
    if rsrp > -90:
        return [0, 255, 0, 200]
    elif rsrp > -110:
        ratio = (rsrp + 110) / 20
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        return [r, g, 0, 200]
    else:
        return [255, 0, 0, 200]

def create_2d_map(df):
    df_display = df.copy()
    df_display["color"] = df_display["RSRP_dBm"].apply(get_color_by_rsrp)

    layer = pdk.Layer(
        "ScatterplotLayer",
        df_display,
        get_position='[Longitude, Latitude]',
        get_color='color',
        get_radius=100,
        radius_scale=1,
        radius_min_pixels=8,
        radius_max_pixels=20,
    )

    view_state = pdk.ViewState(
        latitude=df_display["Latitude"].mean(),
        longitude=df_display["Longitude"].mean(),
        zoom=11,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v11',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "CellID: {CellID}\nBand: {Band}\nRSRP: {RSRP_dBm} dBm\nSINR: {SINR_dB} dB"}
    ))

def create_3d_map(df):
    df_display = df.copy()
    df_display["color"] = df_display["RSRP_dBm"].apply(get_color_by_rsrp)
    df_display["height"] = df_display["Download_Mbps"] * 2

    layer = pdk.Layer(
        "ColumnLayer",
        df_display,
        get_position='[Longitude, Latitude]',
        get_elevation='height',
        get_fill_color='color',
        elevation_scale=0.5,
        radius=80,
        pickable=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=df_display["Latitude"].mean(),
        longitude=df_display["Longitude"].mean(),
        zoom=11,
        pitch=45
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v11',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "CellID: {CellID}\nBand: {Band}\nRSRP: {RSRP_dBm} dBm\nDownload: {Download_Mbps} Mbps"}
    ))

def create_band_chart(df):
    band_counts = df["Band"].value_counts().reset_index()
    band_counts.columns = ["Band", "数量"]

    fig = px.bar(
        band_counts,
        x="Band",
        y="数量",
        title="各频段基站数量统计",
        color="Band",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

def create_terminal_pie(df):
    terminal_counts = df["TerminalType"].value_counts().reset_index()
    terminal_counts.columns = ["TerminalType", "数量"]

    fig = px.pie(
        terminal_counts,
        values="数量",
        names="TerminalType",
        title="不同类型终端占比",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

def create_sinr_rsrp_scatter(df):
    fig = px.scatter(
        df,
        x="RSRP_dBm",
        y="SINR_dB",
        color="Band",
        size="Download_Mbps",
        title="RSRP vs SINR 关系图（点大小表示下载速率）",
        hover_data=["CellID", "TerminalType"]
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

def main():
    df = load_data(DATA_PATH)

    st.sidebar.header("🔧 筛选控制")
    st.sidebar.markdown("---")

    all_bands = ["全部"] + sorted(df["Band"].unique().tolist())
    selected_band = st.sidebar.selectbox("选择频段", all_bands)

    rsrp_min, rsrp_max = st.sidebar.slider(
        "RSRP 范围 (dBm)",
        float(df["RSRP_dBm"].min()),
        float(df["RSRP_dBm"].max()),
        (float(df["RSRP_dBm"].min()), float(df["RSRP_dBm"].max()))
    )

    terminal_types = ["全部"] + sorted(df["TerminalType"].unique().tolist())
    selected_terminal = st.sidebar.selectbox("选择终端类型", terminal_types)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 数据概览")
    st.sidebar.metric("总记录数", len(df))
    st.sidebar.metric("基站数量", df["CellID"].nunique())
    st.sidebar.metric("RSRP 均值", f"{df['RSRP_dBm'].mean():.2f} dBm")

    if selected_band != "全部":
        df = df[df["Band"] == selected_band]
    df = df[(df["RSRP_dBm"] >= rsrp_min) & (df["RSRP_dBm"] <= rsrp_max)]
    if selected_terminal != "全部":
        df = df[df["TerminalType"] == selected_terminal]

    st.sidebar.markdown("---")
    st.sidebar.info(f"当前筛选后记录数: **{len(df)}**")

    tab1, tab2, tab3 = st.tabs(["📍 2D 信号地图", "🏗️ 3D 信号地图", "📊 数据统计"])

    with tab1:
        st.subheader("2D 信号分布地图")
        st.markdown("> 绿色：RSRP > -90 dBm（信号强） | 黄色：-110 < RSRP ≤ -90 dBm | 红色：RSRP ≤ -110 dBm（信号弱）")
        if len(df) > 0:
            create_2d_map(df)
        else:
            st.warning("当前筛选条件下无数据")

    with tab2:
        st.subheader("3D 信号柱状地图")
        st.markdown("> 柱状图高度表示下载速率（Download_Mbps），颜色表示信号强度")
        if len(df) > 0:
            create_3d_map(df)
        else:
            st.warning("当前筛选条件下无数据")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            create_band_chart(df)
        with col2:
            create_terminal_pie(df)
        create_sinr_rsrp_scatter(df)

    st.markdown("---")
    st.markdown("### 📋 数据明细表")
    st.dataframe(
        df[["Latitude", "Longitude", "CellID", "Band", "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps"]],
        use_container_width=True,
        height=300
    )

if __name__ == "__main__":
    main()