import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="Khan's Desi Dhaba - AI Assistant",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Fully responsive
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #1a472a 0%, #2d5016 100%);
        padding: 1rem;
    }
    
    /* Responsive font sizes */
    .stChatMessage {
        font-size: clamp(0.95rem, 2vw, 1.1rem) !important;
        line-height: 1.7 !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        border-radius: 15px !important;
    }
    
    [data-testid="stChatMessageContent"] {
        font-size: clamp(0.95rem, 2vw, 1.1rem) !important;
        line-height: 1.7 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        font-size: clamp(0.95rem, 2vw, 1.1rem) !important;
        margin-bottom: 0.7rem !important;
    }
    
    /* Header - responsive */
    .header-container {
        text-align: center;
        padding: clamp(1.5rem, 4vw, 3rem) clamp(1rem, 3vw, 2rem);
        background: linear-gradient(135deg, #01411C 0%, #0a6b3a 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .header-container h1 {
        font-size: clamp(1.8rem, 5vw, 3.5rem);
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-container h2 {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        margin: 0.8rem 0;
    }
    
    .header-container p {
        font-size: clamp(1rem, 2.5vw, 1.4rem);
        opacity: 0.95;
        margin: 0.5rem 0;
    }
    
    /* Sidebar adjustments */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #01411C 0%, #0a6b3a 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        font-size: clamp(0.9rem, 2vw, 1.05rem) !important;
    }
    
    /* Buttons - responsive */
    .stButton > button {
        font-size: clamp(0.9rem, 2vw, 1.05rem) !important;
        padding: clamp(0.6rem, 1.5vw, 0.8rem) clamp(1rem, 3vw, 2rem) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 45px !important;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] textarea {
        font-size: clamp(0.95rem, 2vw, 1.1rem) !important;
        min-height: 50px !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        font-size: clamp(0.95rem, 2vw, 1.05rem) !important;
    }
    
    h3 {
        font-size: clamp(1.2rem, 3vw, 1.6rem) !important;
        font-weight: 600 !important;
    }
    
    /* Info boxes */
    .stAlert {
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        padding: 1rem !important;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .header-container {
            padding: 1.5rem 1rem;
            margin-bottom: 1rem;
        }
        
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
        }
        
        .stButton > button {
            margin-bottom: 0.5rem;
        }
    }
    
    /* Desktop - ensure columns work properly */
    @media (min-width: 769px) {
        [data-testid="column"]:first-child {
            padding-right: 1rem !important;
        }
        
        [data-testid="column"]:last-child {
            padding-left: 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    if not api_key:
        st.error("⚠️ Groq API key not found. Please add it to your secrets.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# Restaurant information
RESTAURANT_INFO = """
You are a helpful and friendly AI assistant for Khan's Desi Dhaba, an authentic Pakistani restaurant in Lahore.
Be warm, welcoming, and naturally mix English, Urdu words, and Roman Urdu in your responses.

IMPORTANT LANGUAGE RULES:
- When user writes in Roman Urdu (like "kuch chatpata"), respond mixing Roman Urdu WITH English
- Use Roman Urdu phrases naturally: "Bilkul!", "Zaroor", "Mashallah", "Bohot acha", "Sahi hai", "Kya baat hai"
- Keep responses conversational and desi in style
- Examples of good responses:
  * "Bilkul! Humara Chicken Karahi bohot hi chatpata hai!"
  * "Zaroor, aap ko yeh pasand ayega!"
  * "Mashallah! Great choice!"
  * "Sahi farmaya aap ne!"

MENU (All prices in PKR):

STARTERS & SNACKS:
- Samosas (2 pcs) - Rs. 80
- Pakoras (Aloo/Pyaz/Mixed) - Rs. 120
- Seekh Kabab (2 pcs) - Rs. 250
- Chapli Kabab - Rs. 280
- Chicken Tikka (6 pcs) - Rs. 450
- Dahi Bhalla - Rs. 150

MAIN COURSES:
- Chicken Karahi (Half/Full) - Rs. 800/1,500
- Mutton Karahi (Half/Full) - Rs. 1,200/2,200
- Nihari (Beef/Mutton) - Rs. 450/550
- Haleem - Rs. 400
- Biryani (Chicken/Mutton) - Rs. 350/450
- Korma (Chicken/Mutton) - Rs. 800/1,200
- Palak Paneer - Rs. 350
- Dal Makhani - Rs. 280
- Aloo Gosht - Rs. 750

BREADS:
- Naan - Rs. 30
- Tandoori Roti - Rs. 20
- Garlic Naan - Rs. 50
- Keema Naan - Rs. 100
- Paratha (Plain/Aloo) - Rs. 40/60

RICE & RAITA:
- Plain Rice - Rs. 150
- Pulao - Rs. 200
- Raita - Rs. 80

DRINKS:
- Lassi (Sweet/Salty) - Rs. 120
- Mango Lassi - Rs. 150
- Fresh Juice (Seasonal) - Rs. 180
- Soft Drinks - Rs. 80
- Kashmiri Chai - Rs. 100
- Green Tea - Rs. 60

DESSERTS:
- Kheer - Rs. 150
- Gajar Halwa - Rs. 180
- Gulab Jamun (2 pcs) - Rs. 100
- Ras Malai (2 pcs) - Rs. 150
- Kulfi - Rs. 120

TIMING:
- Daily: 11:00 AM - 12:00 AM (Midnight)
- Friday: 1:00 PM - 12:00 AM (After Jummah prayers)

LOCATION: 
Main Boulevard, Gulberg III, Lahore

CONTACT: 
- Phone: 042-35714567
- WhatsApp: 0300-1234567

SPECIAL FEATURES:
- Family dining area (separate section)
- Outdoor seating with shisha
- Home delivery available (Foodpanda, Careem)
- Catering for events and weddings
- Halal certified
- Fresh ingredients daily
- Special BBQ nights on weekends

POPULAR COMBOS:
- Family Deal: Chicken Karahi + 6 Naans + Raita + 1.5L Drink = Rs. 1,400
- BBQ Platter: Mixed Tikka + Seekh Kabab + Chapli + Naans = Rs. 1,200
- Breakfast Special: Halwa Puri + Channay + Lassi = Rs. 250

RESPONSE STYLE EXAMPLES:
User: "kuch chatpata khana hai"
You: "Mashallah! Chatpata khane ka mood hai! Bilkul sahi jagah aaye hain aap. Humara Chicken Karahi bohot hi zabardast hai - masaledar aur teekha! Ya phir Chapli Kabab try karein, full desi flavor ke saath! Aap ko kitna teekha pasand hai? Hum adjust kar sakte hain bilkul!"

User: "biryani kaisi hai"
You: "Arrey wah! Biryani ki baat kar rahe hain? Humari Chicken Biryani mashoor hai puri Lahore mein! Full of flavor, sona rice, aur masala se puri bharpur. Mutton bhi available hai agar aap prefer karein. Raita aur salad ke saath serve hoti hai. Zaroor try karein!"

User: "family ke liye kuch recommend karo"
You: "Bilkul! Family ke liye hamara Family Deal best hai: Full Chicken Karahi + 6 Naans + Raita + 1.5L Drink = sirf Rs. 1,400! Ya phir BBQ Platter bhi bohot acha hai. Sab ko pasand ayega, pakka!"

Always be warm, mix Roman Urdu naturally with English, and sound like a desi person talking to friends!
If someone asks about spice levels, say "Hum adjust kar sakte hain bilkul!"
For reservations, provide phone/WhatsApp. Always be hospitable - Pakistani style!
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "**السلام علیکم! Welcome to Khan's Desi Dhaba!** 🍛\n\nI'm your AI assistant, here to help you!\n\n**How can I serve you today?**\n- 🍽️ Browse our Pakistani menu\n- ⏰ Check timings\n- 📍 Get directions\n- 📞 Make a reservation\n- 🎉 Ask about catering\n\n**Just ask me anything about authentic desi khana!**"}
    ]

# Header
st.markdown("""
    <div class="header-container">
        <h1>🍛 خان کا دیسی ڈھابہ</h1>
        <h2>Khan's Desi Dhaba</h2>
        <p>Authentic Pakistani Cuisine | AI-Powered Service 24/7</p>
        <p style="margin-top: 0.8rem;">🇵🇰 Serving Lahore's Best Since 1995</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with quick actions
with st.sidebar:
    st.markdown("### 🎯 Quick Menu")
    
    if st.button("🍗 BBQ Items"):
        st.session_state.messages.append({"role": "user", "content": "Show me all BBQ items"})
        st.rerun()
    
    if st.button("🍛 Karahi Options"):
        st.session_state.messages.append({"role": "user", "content": "What karahi do you have?"})
        st.rerun()
    
    if st.button("🍚 Biryani & Rice"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about your biryani"})
        st.rerun()
    
    if st.button("🥤 Drinks & Desserts"):
        st.session_state.messages.append({"role": "user", "content": "What drinks and desserts do you have?"})
        st.rerun()
    
    if st.button("💰 Family Deals"):
        st.session_state.messages.append({"role": "user", "content": "Show me your family deals"})
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Why This Bot?")
    st.success("""
**✅ 24/7 Available**  
Never miss customers

**✅ Instant Replies**  
No waiting time

**✅ Bilingual**  
Urdu & English

**✅ Cost Effective**  
70% cheaper than staff
    """)
    
    st.markdown("---")
    
    st.markdown("### 💼 Perfect For:")
    st.info("""
🍽️ **Restaurants**  
☕ **Cafes & Bakeries**  
🏪 **Retail Stores**  
🏥 **Clinics**  
🏢 **Any Business**
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "**السلام علیکم! Welcome back!** 🍛\n\nHow can I help you today?"}
        ]
        st.rerun()

# Main chat area
st.markdown("### 💬 Chat with our AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("پوچھیں... Ask me anything!"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Prepare messages for Groq
            groq_messages = [
                {"role": "system", "content": RESTAURANT_INFO}
            ]
            
            # Add conversation history
            for msg in st.session_state.messages[-10:]:
                if msg["role"] != "system":
                    groq_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Call Groq API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_messages,
                temperature=0.7,
                max_tokens=800,
                top_p=0.9
            )
            
            assistant_response = response.choices[0].message.content
            message_placeholder.markdown(assistant_response)
            
            # Add to session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response
            })
            
        except Exception as e:
            error_msg = f"⚠️ **Sorry, encountered an error:** {str(e)}\n\nPlease try again or contact: 042-35714567"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

