import streamlit as st
from openai import OpenAI

# ==========================================
# 👇 这里是唯一需要你修改的地方
# 1. 去 https://platform.deepseek.com 申请一个 Key
# 2. 把你的 Key 填在下面的引号里，替换掉 sk-xxxx
# ==========================================
API_KEY = st.secrets["API_KEY"]
# 如果你用的是 DeepSeek，保持下面这个网址不变
BASE_URL = "https://api.deepseek.com"

# --- 页面 UI 设置 ---
st.set_page_config(page_title="小红书爆款文案生成器", page_icon="💰", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #FFF0F5; } /* 浅粉色背景 */
    .title { color: #FF1493; text-align: center; font-weight: bold; }
    .subtitle { color: #666; text-align: center; font-size: 14px; }
    .stButton button { 
        background-color: #FF1493; color: white; border-radius: 20px; 
        font-size: 18px; font-weight: bold; border: none; width: 100%;
    }
    .stButton button:hover { background-color: #C71585; color: white; }
    .result-box {
        background: white; padding: 20px; border-radius: 15px;
        border: 2px solid #FF1493; box-shadow: 5px 5px 0px #FF69B4;
        color: #333; font-size: 16px; line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- AI 核心逻辑 ---
def get_xhs_copy(text, tone):
    # 如果没有填 Key，直接报错
    if "sk-" not in API_KEY or len(API_KEY) < 10:
        return "⚠️ 请先在代码第 7 行填入正确的 API Key！"

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    prompt = f"""
    你是一个拥有百万粉丝的小红书博主。请将用户输入的【原始文本】改写成一篇极具吸引力的笔记。
    
    【语气风格】：{tone}
    【硬性要求】：
    1. 标题：必须采用“二极管标题法”，包含悬念或强烈情绪（如“绝了！”“哭死！”），不超过20字。
    2. 排版：使用大量Emoji（✨🌸🔥），多分段，视觉舒适。
    3. 标签：文末生成 5-8 个精准的 hashtag。
    
    【原始文本】：
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat", 
            messages=[{"role": "user", "content": prompt}],
            temperature=1.3, 
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 报错了：{e}"

# --- 前端展示 ---
st.markdown("<h1 class='title'>🚀 小红书爆款改写神器</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>专为搞钱人开发的 AI 助手 | 1秒生成种草文案</p>", unsafe_allow_html=True)

# 输入区
user_text = st.text_area("在此输入你的干货/大白话：", height=120, placeholder="例如：我想推荐一个很好用的洗面奶，洗完不紧绷，价格才30块钱...")

# 选项区
col1, col2 = st.columns(2)
with col1:
    tone_style = st.selectbox("选择笔记风格", ["💖 热情种草风", "📚 干货科普风", "✨ 清冷高级风", "😭 情绪共鸣风"])
with col2:
    length = st.radio("文案长度", ["短小精悍 (200字)", "详细深度 (500字)"])

# 按钮
if st.button("✨ 立即生成爆款文案 ✨"):
    if not user_text:
        st.warning("宝子，内容不能为空哦！")
    else:
        with st.spinner("AI 正在疯狂码字中... ☕️"):
            result = get_xhs_copy(user_text, tone_style)
            st.markdown(f"<div class='result-box'>{result.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            st.success("✅ 生成成功！点击右上角复制")