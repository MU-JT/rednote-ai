import streamlit as st
from openai import OpenAI

# --- 🔐 商业配置区 ---
# 1. 设置解锁密码 (默认8888)
ACCESS_PASSWORD = "0129" 

# 2. 获取 Key (云端/本地兼容写法)
try:
    API_KEY = st.secrets["API_KEY"]
except:
    API_KEY = "LOCAL_TEST_KEY" 

BASE_URL = "https://api.deepseek.com"

# --- 页面 UI ---
st.set_page_config(page_title="小红书爆款文案生成器", page_icon="💰", layout="centered")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp { background-color: #FFF0F5; }
.result-box {
    background: white; padding: 20px; border-radius: 15px;
    border: 2px solid #FF1493; box-shadow: 5px 5px 0px #FF69B4;
    color: #333; font-size: 16px; line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# --- 侧边栏 (密码锁) ---
with st.sidebar:
    st.header("🔓 解锁完整版")
    st.markdown("只需一杯咖啡钱，永久解锁。")
    st.link_button("👉 购买访问密码", "https://gumroad.com") 
    st.divider()
    user_password = st.text_input("请输入访问密码：", type="password")
    if user_password == ACCESS_PASSWORD:
        st.success("✅ 已解锁")
        auth_status = True
    else:
        st.warning("🔒 请输入密码")
        auth_status = False

# --- AI 核心 ---
def get_xhs_copy(text, tone):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = f"把这段话改写成小红书爆款文案，风格：{tone}。\n内容：{text}"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3, stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 错误：{e}"

# --- 主界面 ---
st.markdown("<h1 style='text-align: center; color: #FF1493;'>🚀 小红书爆款改写神器</h1>", unsafe_allow_html=True)

if auth_status:
    user_text = st.text_area("输入内容：", height=120)
    tone_style = st.selectbox("风格", ["热情种草", "干货科普", "清冷高级", "情绪共鸣"])
    if st.button("✨ 立即生成 (Pro) ✨", type="primary"):
        if not user_text:
            st.warning("请输入内容")
        else:
            with st.spinner("AI 正在思考..."):
                result = get_xhs_copy(user_text, tone_style)
                st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
else:
    st.info("👋 欢迎！请输入密码以使用 Pro 版功能。")
