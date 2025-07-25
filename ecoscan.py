import streamlit as st
import base64
from openai import OpenAI
import os
import random
import time
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load the Lottie animation from a URL
def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Eco tips list
eco_tips = [
    "Consider choosing clothing made from organic cotton to reduce environmental impact.",
    "Buy second-hand clothes to contribute to a more sustainable fashion economy.",
    "Wash clothes in cold water to save energy and reduce carbon emissions.",
    "Avoid fast fashion; invest in timeless, durable pieces for your wardrobe.",
    "Recycle your old clothes instead of throwing them away to reduce textile waste.",
    "Look for clothing brands that use sustainable and eco-friendly materials.",
    "Opt for clothing made from recycled or biodegradable fabrics to minimize waste.",
    "Air dry your clothes instead of using a tumble dryer to save energy."
]

# Function to change the eco tip every 10 seconds
def eco_tip():
    while True:
        yield random.choice(eco_tips)
        time.sleep(5)

# Start eco-tip generator
eco_tip_generator = eco_tip()
# Set your OpenAI API Key directly in the script
# Secure API key handling
def get_openai_key():
    """Get OpenAI API key from environment or Streamlit secrets"""
    try:
        # Try Streamlit secrets first (for cloud deployment)
        return st.secrets["OPENAI_API_KEY"]
    except:
        # Fall back to environment variable (for local development)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OpenAI API key not found! Please set up your API key.")
            st.info("For local development: Set OPENAI_API_KEY environment variable")
            st.info("For Streamlit Cloud: Add OPENAI_API_KEY to app secrets")
            st.stop()
        return api_key
OPENAI_API_KEY = get_openai_key()
client = OpenAI(api_key=OPENAI_API_KEY)

# Configure Streamlit
st.set_page_config(layout="wide",page_icon="🌿",page_title="Eco Scan Dashboard")
# Custom CSS for title and tabs
st.markdown("""
    <style>
        /* Title styling */
        .main-title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 5px; /* Reduce space below */
        }

        .main-title {
            font-size: 36px; /* Increase title size */
            font-weight: bold;
            color: #28a745; /* Green color for the title */
            margin: 0;
        }

        .caption {
            text-align: center;
            font-size: 18px; /* Slightly smaller size for caption */
            color: #777; /* Light grey for the caption */
            margin-top: -5px; /* Reduce spacing between title and caption */
        }
    </style>
    
    <!-- Title container -->
    <div class="main-title-container">
        <img src="https://cdn.shopify.com/app-store/listing_images/276906bc96e4ef0fe3a050fee383ce9e/icon/CLzgldO9uvwCEAE=.png", 
             width="60" alt="Logo"> <!-- Compact logo size -->
        <h1 class="main-title">Reewild ECO-SCAN</h1>
    </div>
    <!-- Caption -->
    <div class="caption">Analyze the Carbon Footprint of Your Clothing 🌱</div>
""", unsafe_allow_html=True)

# Set the API Key in the environment variable (for OpenAI SDK compatibility)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# Helper function to encode image to base64
def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

# Function to analyze the uploaded image using OpenAI API
def analyze_image(image_data: str) -> str:
    prompt_instruction = """
    You are an intelligent assistant whose task is to analyse the clothing items and calculate the carbon footprint.
    Instructions:
    Analyze and recognize the clothing items in the image, calculate the carbon footprint, and display in the format below.
    Also, Take this approximations.The estimated carbon footprints for various clothing items, in terms of kilograms of CO₂, vary depending on the material and manufacturing process. For example, a cotton T-shirt has an estimated carbon score of 5 kg CO₂, while denim jeans have a higher score of 10 kg CO₂. Wool or polyester jackets have a carbon score of 15 kg CO₂, and cotton shirts typically have a score of 4 kg CO₂. Other clothing items such as wool or acrylic sweaters come in at around 7 kg CO₂, and cotton or synthetic dresses have an estimated carbon footprint of 8 kg CO₂. Shorts made of cotton, hoodies made of cotton, and pajamas made of cotton are generally around 4 kg CO₂. For outerwear, wool or synthetic coats have a carbon score of 18 kg CO₂, while a wool suit is significantly higher at 20 kg CO₂. Other items like skirts (cotton) have a footprint of 6 kg CO₂, and socks (cotton or wool) are around 1.5 kg CO₂. Underwear made from cotton has a minimal impact, with only 1 kg CO₂, while tights made of nylon are approximately 2 kg CO₂. Sportswear made from polyester contributes 7 kg CO₂. Footwear also varies, with leather or synthetic boots having a carbon footprint of 14 kg CO₂, and leather or synthetic sneakers and sandals coming in at 8 and 5 kg CO₂, respectively. Accessories like wool scarves are estimated at 3 kg CO₂, while leather gloves and bags are around 2 and 15 kg CO₂, respectively. Nylon backpacks have an estimated carbon footprint of 6 kg CO₂.
    Example:
    ANALYSIS:
    The Image consists of "3 T-Shirts".
    T-Shirts Carbon Footprint = 5
    Total Carbon Footprint = 3* 5 = 15kg CO2.
    If there are NO clothing Items .Respond NO clothing Items in the image.

    """

    client = OpenAI(api_key=OPENAI_API_KEY)  # Initialize OpenAI client with API key
    MODEL = "gpt-4o"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_instruction},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# Load the Lottie animation
lottie_animation = load_lottieurl("https://lottie.host/309d9935-979c-4b29-827f-92ebb3846e54/PKdHbTQhxU.json")

# Sidebar Content
with st.sidebar:
    # Title with Leaf Icon
    st.markdown(
        """
        <div >
            <h1 style="font-size: 28px; color: #f2e7c9; font-weight: bold; margin-bottom: 10px;">
                🌿 Welcome to ECO SCAN 
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Quote with proper HTML formatting
    quote = """
<span style="font-size:16px; color:lightblue; line-height:1.5; text-align:center;">
    Every new garment we buy has a <span style="color: white; font-weight: bold;">hidden cost .</span> So, let’s 
    <span style="color: white; font-weight: bold;">choose wisely</span> and reduce our 
    <span style="color: white; font-weight: bold;">carbon debt</span>.
</span>
"""
    st.markdown(quote,unsafe_allow_html=True,)
    # Lottie Animation
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="eco_scan_animation")
    else:
        st.error("Failed to load animation.")

    # Instructions Section
    st.markdown(
        """
        <div style="font-size: 16px; line-height: 1.6;">
            <p style="color: #008080; font-weight: bold;">
                🌍 <span style="color: #BDD7A7;">Using ECO_SCAN You Can:</span>
            </p>
            <ul style="color: #a3c4bc;">
                <li><b style="color: #a3c4bc;">Scan your clothing items</b> and calculate the <b>carbon footprint</b>.</li>
                <li><b style="color: #a3c4bc;">Earn Eco Reward Points</b> for sustainable choices.</li>
                <li><b style="color: #a3c4bc;">Claim exciting offers</b> using your Eco Reward Points!</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="font-size: 16px; line-height: 1.6; text-align: center;">
            <p style="color: #BDD870; font-weight: bold;">
                "The Earth is like a rental car —  
                you'd care more if your credit card was on file!😉"
            </p>
            <p style="color: #73E16F; font-style: italic;">
                Every choice you make leaves a carbon footprint...  
                and the planet isn’t taking any refunds.🍃
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["Home", "About", "Upload", "Quiz"])

# Tab 1: Home
# Tab 1: Home
with tab1:
    # Custom CSS for styling the homepage
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #fafafa;
            color: #333;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        .hero-section {
            background-image: url('https://i.postimg.cc/Qd9TNbsB/pexels-artempodrez-6990484.jpg');
            background-size:cover;
            background-position: center;
            height: 80vh;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }
        .hero-title {
            
            font-size: 70px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5);
        }
        .hero-tagline {
            font-size: 26px;
            margin-bottom: 40px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        }
        .features-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            padding: 60px 20px;
        }
        .feature-card {
            background-color: #CCE8C2;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease-in-out;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
        }
        .feature-card img {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
        }
        .feature-card h3 {
            font-size: 22px;
            margin-bottom: 10px;
            color: #388e3c;
        }
        .feature-card p {
            color: #555;
            font-size: 16px;
        }
        .feature-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(to right, #4caf50, #388e3c);
            transform: scaleX(0);
            transform-origin: bottom right;
            transition: transform 0.5s ease;
        }
        .feature-card:hover::after {
            transform: scaleX(1);
            transform-origin: bottom left;
        }
        .cta-button {
            background: linear-gradient(45deg, #4caf50, #388e3c);
            color: white;
            border: none;
            font-size: 18px;
            padding: 15px 30px;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 60px;
            transition: all 0.3s ease;
            display: block;
            margin: 40px auto;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .cta-button:hover {
            background: linear-gradient(45deg, #388e3c, #4caf50);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            transform: translateY(-5px);
        }
        .footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 60px;
            padding: 20px;
            background-color: #f1f1f1;
        }
        .full-width-image {
            width: 100%;
            height: auto;
            margin-top: 60px;
        }
        html {
            scroll-behavior: smooth;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title" style="color:#388e3c;">Welcome to EcoScan</div>
            <div class="hero-tagline"style="color:#083D07;">Scan your clothing, understand your carbon footprint, and make eco-friendly choices!</div>
        </div>
    """, unsafe_allow_html=True)

# Display image from a URL
    st.image("https://images.squarespace-cdn.com/content/v1/5788b7b16a4963f2a542d038/1631176252253-RKZKFN6TH70Z4SQLG0KM/fashion-carbon-footprint.jpg", use_container_width=True)

    # Features Section
    st.markdown("<h2 style='text-align: center; color: #388e3c; font-size: 36px;'>How EcoScan Helps You</h2>", unsafe_allow_html=True)

    # Features Container (Cards in Grid)
    st.markdown("<div class='features-container'>", unsafe_allow_html=True)

    # Feature 1: Upload Your Clothing Item
    st.markdown("""
        <div class="feature-card">
            <img src="https://img.icons8.com/ios/452/camera.png" alt="Upload" />
            <h3>Upload Your Clothing Item</h3>
            <p>Upload a picture of your clothing item(s) to get started, either from your gallery or by snapping a photo directly from your camera.</p>
        </div>
    """, unsafe_allow_html=True)

    # Feature 2: Item Identification & Carbon Footprint
    st.markdown("""
        <div class="feature-card">
            <img src="https://img.icons8.com/ios/452/ai.png" alt="Identification" />
            <h3>Item Identification & Carbon Footprint</h3>
            <p>Our app identifies the clothing items and calculates the carbon footprint associated with each item to help you make eco-friendly decisions.</p>
        </div>
    """, unsafe_allow_html=True)

    # Feature 3: Track Eco-Rewards
    st.markdown("""
    <div class="feature-card">
        <img src="https://img.icons8.com/ios/452/environment.png" alt="Tracker" style="width: 80px; height: 80px; margin-bottom: 20px;" />
        <h3>Track Your Carbon Footprint</h3>
        <p>Monitor and reduce your carbon footprint over time as you make more sustainable fashion choices.</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature 4: Redeem Offers
    st.markdown("""
        <div class="feature-card">
            <img src="https://img.icons8.com/ios/452/gift.png" alt="Offers" />
            <h3>Redeem Offers</h3>
            <p>Use your eco-reward points to redeem exclusive offers and discounts on eco-friendly products.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


    # Full-width Image Section
    st.markdown("""
        <div class="full-width-image">
            <img src="https://i.postimg.cc/s2FN6Mx8/Screenshot-2024-11-24-11-59-51-PM.png" alt="Eco-Friendly Fashion" class="full-width-image" />
        </div>
    """, unsafe_allow_html=True)

    # Footer Section (Last)
    st.markdown('<div class="footer">EcoScan - Join us in reducing the fashion industry’s carbon footprint. Make smarter, eco-friendly choices!</div>', unsafe_allow_html=True)

import pandas as pd

with tab2:
    # Style Settings
    heading_color = "#808000"  # Olive Green
    text_color_1 = "#E7EFC5"
    text_color_2 = "#B4D6BA"
    text_color_3 = "#E3C3D3"
    background_color = "#F9F9F9"

    # Apply page-wide styles
    st.markdown(
        f"""
        <style>
            body {{
                background-color: {background_color};
                color: {text_color_1};
            }}
            h2, h3 {{
                color: {heading_color};
                font-weight: bold;
                text-transform: uppercase;
            }}
            p {{
                font-size: 20px;
                line-height: 1.8;
            }}
            .emoji-bullet {{
                font-size: 24px;
                margin-right: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title and Introduction Section
    

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<h2 style='text-align: center;'>🌿 Welcome to Eco-Scan </h2>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <p style="font-size: 22px; color: {text_color_1};">
            🌍 <b>Eco-Scan</b> is your ultimate tool to track the environmental impact of your fashion choices. 
            With just a photo, we provide insights into your clothing’s carbon footprint and help you earn exciting rewards! 🎉
            </p>
            <ul style="font-size: 20px; color: {text_color_2};">
            <li><span class="emoji-bullet">👗</span> Analyze clothing materials and their impact on the planet.</li>
            <li><span class="emoji-bullet">♻️</span> Encourage sustainable habits like recycling and buying secondhand.</li>
            <li><span class="emoji-bullet">🎁</span> Earn and redeem eco-reward points for greener fashion.</li>
            </ul>
            </p>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        
        st.image(
            "https://img.freepik.com/premium-vector/ecofriendly-woman-with-upcycled-clothing-piles-sustainable-fashion-concept_906149-129314.jpg",
            caption="Make sustainability fashionable! 👗♻️",
            use_container_width=False,
            
        )

    # How It Works Section
    

    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.image(
            "https://youthtimemag.com/wp-content/uploads/2022/03/shutterstock_2011615499.png",
            caption="Your sustainability journey starts here! 🌟",
            use_container_width=False,
            width=500,
            
        )

        
    with col4:
        st.markdown("<h2 style='text-align':center;>🔍 HOW IT WORKS</h2>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <ul style="font-size: 22px; color: {text_color_2};">
            <li><span class="emoji-bullet">📤</span> Upload an Image: Snap a photo of your clothing item.</li>
            <li><span class="emoji-bullet">📊</span> Carbon Footprint Analysis: Get detailed stats on the item's environmental impact.</li>
            <li><span class="emoji-bullet">🌟</span> Eco-Rewards: Earn points for adopting sustainable practices.</li>
            <li><span class="emoji-bullet">🎉</span> Redeem Rewards: Enjoy discounts, free shipping, or exclusive eco-deals.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    # Eco-Savings and Rewards Section
    

    col5, col6 = st.columns(2, gap="large")
    with col5:
        st.markdown("<h3 style='text-align'=center;>💚 ECO-SAVINGS AND REWARDS</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <p style="font-size: 22px; color: {text_color_3};">
            Every sustainable step you take counts! 🌟  
            <b>Here’s how you can earn:</b>
            </p>
            <ul style="font-size: 22px; color: {text_color_3};">
            <li><span class="emoji-bullet">🛍️</span> Buy sustainable fabrics: Saves 5 kg CO₂ → Earn 50 points.</li>
            <li><span class="emoji-bullet">♻️</span> Recycle clothes:Saves 6 kg CO₂ → Earn 60 points.</li>
            <li><span class="emoji-bullet">👚</span> Choose secondhand: Saves 10 kg CO₂ → Earn 100 points.</li>
            </ul>
            <p style="font-size: 22px;">🎁 Redeem Points for:</p>
            <ul style="font-size: 22px;">
            <li><span class="emoji-bullet">💸</span> Discounts up to 15% on eco-friendly brands.</li>
            <li><span class="emoji-bullet">🚚</span> Free shipping on sustainable products.</li>
            <li><span class="emoji-bullet">🎁</span> Exclusive offers on green fashion items.</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
    with col6:
        st.image(
            "https://img.freepik.com/free-vector/hand-drawn-sustainable-fashion-concept_52683-54792.jpg",
            caption="Identify and calculate your clothing's carbon footprint. 🌱",
            use_container_width=False,
            width=400
           
        )
    # Clothing Items and Carbon Footprint Table
    st.markdown("<h3>📊 ESTIMATED CARBON FOOTPRINT FOR CLOTHING ITEMS</h3>", unsafe_allow_html=True)

    data = {
        "Item": [
            "T-shirt (Cotton)", "Jeans (Denim)", "Jacket (Wool or Polyester)", "Shirt (Cotton)",
            "Sweater (Wool or Acrylic)", "Dress (Cotton or Synthetic)", "Shorts (Cotton)",
            "Hoodie (Cotton)", "Suit (Wool)", "Coat (Wool or Synthetic)", "Skirt (Cotton)",
            "Socks (Cotton or Wool)", "Underwear (Cotton)", "Tights (Nylon)", "Sportswear (Polyester)",
            "Boots (Leather or Synthetic)", "Sneakers (Leather or Synthetic)", "Sandals (Leather or Synthetic)",
            "Scarf (Wool)", "Gloves (Leather)", "Bag (Leather)", "Backpack (Nylon)", "Pajamas (Cotton)"
        ],
        "Estimated Carbon Score (kg CO₂)": [
            5, 10, 15, 4, 7, 8, 4, 8, 20, 18, 6, 1.5, 1, 2, 7, 14, 8, 5, 3, 2, 15, 6, 4
        ]
    }

    df = pd.DataFrame(data)
    st.dataframe(
        df.style.set_table_styles(
            [
                {"selector": "th", "props": [("background-color", heading_color), ("color", "white"), ("text-align", "center")]},
                {"selector": "td", "props": [("background-color", "#E7EFC5"), ("color", "black")]},
            ]
        )
    )

    # Conclusion
    st.markdown(
        f"""
        <h3 style='text-align: center;'>🎉 CONCLUSION</h3>
        <p style='font-size: 22px; text-align: justify; color: {text_color_1};'>
        At <b>Eco-Scan</b>, we believe in making sustainability accessible and fun! 🌟 
        With every action, you’re making a greener choice for the planet. Start your journey today 
        and be a hero for the environment! 🌿
        </p>
        """,
        unsafe_allow_html=True,
    )



# Tab 3: Upload
with tab3:
    st.markdown("### Upload Your Clothing Image")

    # Centered file uploader and camera input
    st.markdown('<div class="file-uploader-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    # File uploader section
    with col1:
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.success("Image uploaded successfully", icon="✅")

    # Camera input section with a toggle button
    with col2:
        st.markdown("""
        <style>
            .camera-toggle-container {
                margin-top: 20px;
                background-color: #e7f7ec;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #4CAF50;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }

            .camera-toggle-container:hover {
                background-color: #a7e5a7;
                border-color: #388e3c;
            }

            .stButton button {
                background-color: #4CAF50; /* Green background */
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 8px;
                font-weight: bold;
                border: none;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }

            .stButton button:hover {
                background-color: #45a049; /* Darker green on hover */
            }
        </style>
        """, unsafe_allow_html=True)

        # Toggle button for camera input
        camera_toggle = st.button("📸 Turn On Camera", key="camera_toggle")
        if camera_toggle:
            st.session_state.camera_enabled = True
            st.rerun()  # Refresh the app to show the camera
            

        if "camera_enabled" not in st.session_state:
            st.session_state.camera_enabled = False  # Initialize session state if not set

        # Camera input section, shown only if camera toggle is enabled
        if st.session_state.camera_enabled:
            st.markdown("""
            <style>
                .camera-input-container {
                    margin-top: 20px;
                    background-color: #e7f7ec;
                    padding: 10px;
                    border-radius: 8px;
                    border: 2px solid #4CAF50;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                }

                .camera-input-container:hover {
                    background-color: #a7e5a7;
                    border-color: #388e3c;
                }

                .stCameraInput {
                    width: 100%;
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #e7f7ec;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease-in-out;
                }

                .stCameraInput:hover {
                    transform: scale(1.05);
                }
            </style>
            """, unsafe_allow_html=True)
            
            with st.expander("📸 Capture your clothing image", expanded=False):
                st.write("Please position the camera to capture the image of the clothing item.")
                camera_photo = st.camera_input("Take a picture")

    st.markdown('</div>', unsafe_allow_html=True)

    # Customize file uploader styling with modern green color
    st.markdown("""
    <style>
        .stFileUploader {
            
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
        }

        .stFileUploader:hover {
            background-color: #a7e5a7;
            border-color: #388e3c;
        }

        .stFileUploader label {
            font-size: 18px;
            font-weight: bold;
            color: #4CAF50;
        }

        .stFileUploader .stSuccess {
            color: #4CAF50;
            font-weight: bold;
        }

        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton button:hover {
            background-color: #45a049;
        }

        .results-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            margin-top: 30px;
        }

        .result-box {
            width: 48%;
            padding: 25px;
            border-radius: 15px;
            background: linear-gradient(135deg, #4CAF50, #8BC34A);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            color: white;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .result-box:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .result-box h3 {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }

        .result-box p {
            font-size: 18px;
            line-height: 1.6;
        }

        .uploaded-image-box {
            width: 48%;
            text-align: center;
            border-radius: 15px;
            border: 2px solid #ddd;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .uploaded-image-box:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .uploaded-image-box h3 {
            font-size: 24px;
            font-weight: bold;
        }

        .uploaded-image-box img {
            width: 250px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    # Analyze button centered below inputs
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    analyze_button = st.button("🔍 Analyze Image", key="analyze", help="Click to analyze the image")
    st.markdown('</div>', unsafe_allow_html=True)

    # Displaying eco tip
    eco_tip_text = next(eco_tip_generator)
    st.markdown(f"### Eco Tip: {eco_tip_text}", unsafe_allow_html=True)

    # Results layout after analysis
    if analyze_button:
        input_image = uploaded_file if uploaded_file else camera_photo

        if input_image is not None:
            temp_image_path = "input_image.png"
            with open(temp_image_path, "wb") as f:
                f.write(input_image.getbuffer())

            base64_image = encode_image(temp_image_path)

            with st.spinner('Scanning image...'):
                result = analyze_image(base64_image)

            st.markdown("""
                <div class="results-container">
                    <div class="result-box">
                        <h3>Analysis Result</h3>
                        <p>{}</p>
                    </div>
                    <div class="uploaded-image-box">
                        <h3>Uploaded Image</h3>
                        <img src="data:image/png;base64,{}" alt="Uploaded Image">
                    </div>
                </div>
            """.format(result, base64_image), unsafe_allow_html=True)
        else:
            st.error("Please upload or capture an image of the clothing item(s).")
        # Footer
    
    st.info("Check Your Eco Rewards By Participating In the Eco Savings Quiz!!!")
    st.success("Navigate to the Eco Savings Quiz Tab!! ")
        


# Set custom CSS to increase font size
st.markdown("""
    <style>
        .stMarkdown {
            font-size: 18px;  /* Increase the font size for all text */
        }
        .stRadio label, .stCheckbox label {
            font-size: 18px;  /* Increase font size for radio and checkbox labels */
        }
        .stButton {
            font-size: 18px;  /* Increase font size for buttons */
        }
    </style>
""", unsafe_allow_html=True)

import streamlit as st

# Set custom CSS to increase font size
st.markdown("""
    <style>
        .stMarkdown {
            font-size: 18px;  /* Increase the font size for all text */
        }
        .stRadio label, .stCheckbox label {
            font-size: 18px;  /* Increase font size for radio and checkbox labels */
        }
        .stButton {
            font-size: 18px;  /* Increase font size for buttons */
        }
    </style>
""", unsafe_allow_html=True)

# Tab 4 Layout: Eco-Quiz inside Tab 4
with tab4:
    
        # Create a 2:1 layout
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            # Title and description
            # Introduction content with custom styling
            intro_content = """
        <p style="font-size: 20px; color: #AAB396; line-height: 1.5;">
        <strong>🌍 <span style="font-weight: bold; font-size: 24px;"> Welcome to the Eco-Quiz: Test Your Sustainability Knowledge!</span> 🌱</strong>
    </p>
        <p style="font-size: 17px; color: #AAB396; line-height: 1.5;">
        Are you ready to embark on a fun and educational journey to explore your eco-friendly habits? 🧐 This quiz will challenge your knowledge about sustainability, eco-savings, and how you can contribute to a greener world. 🌿<br>
        So, let's get started and see how green you truly are! 💚🌱
        Take the quiz now and claim your exciting rewards at the end! 🎉
        </p>
        
"""

# Displaying the content in Streamlit
            
            st.markdown(intro_content, unsafe_allow_html=True)

            # Initialize eco-points
            eco_points = 0

            # Track quiz progress
            progress = st.progress(0)
            total_questions = 9
            current_question = 0

            # Function to show a joke when an option is selected
            def show_joke(question_index, selected_option):
                jokes = {
                    0: {
                        "Yes": "You're rocking the thrift vibes! 😎",
                        "No": "It's okay, everyone starts somewhere! Maybe next time? 😇",
                    },
                    1: {
                        "Yes": "Sustainable materials? You're basically a fashion superhero! 🦸‍♂️",
                        "No": "Remember, even polyester has feelings...sort of. 😬",
                    },
                    2: {
                        "Yes": "Upcycle level: Picasso with fabric! 🎨",
                        "No": "Don't worry, duct tape fixes everything! 😂",
                    },
                    3: {
                        "Yes": "Cold water saves energy—and your utility bill! 🧊💧",
                        "No": "Hot water? Fancy! 🛁 Let's aim for chill next time. 😉",
                    },
                    4: {
                        "Always": "Carbon-neutral shipping? You deserve a standing ovation! 👏",
                        "Sometimes": "Every step counts! Keep choosing wisely. 🌍",
                        "Never": "No worries, maybe next delivery? 📦🌍",
                    },
                    5: {
                        "Yes": "Donating clothes = karma points unlocked! 🙌",
                        "No": "Think of it as spreading your fashion legacy! 👗👕",
                    },
                    6: {
                        "Yes": "You’re a recycling wizard! ♻️✨",
                        "No": "Hey, there’s always tomorrow to start! 🌱",
                    },
                    7: {
                        "Yes": "Bagging it up for the planet! 🌍💚",
                        "No": "Forget the bag, grab the planet! Next time? 😇",
                    },
                    8: {
                        "Yes": "You’re an eco-warrior! 🦸‍♀️🦸‍♂️",
                        "No": "Not yet, but one day! Keep trying! 💪",
                    },
                }
                st.info(jokes[question_index].get(selected_option, "Great choice! Keep it up! 😃"))

            # Question 1: Multiple Choice
            secondhand = st.radio(
                "1.Did you purchase your clothing items secondhand?", ["", "Yes", "No"],
                key="q1", index=0
            )
            if secondhand:
                eco_points += 100 if secondhand == "Yes" else 0
                show_joke(0, secondhand)
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 2: True or False
            sustainable_materials = st.radio(
                "2.Are your clothing items made from sustainable materials?", ["", "Yes", "No"],
                key="q2", index=0
            )
            if sustainable_materials:
                eco_points += 50 if sustainable_materials == "Yes" else 0
                show_joke(1, sustainable_materials)
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 3: Slider
            repair_upcycle = st.slider(
                "3.How often do you repair or upcycle your clothes? (0 = Never, 100 = Always)",
                min_value=0, max_value=100, step=10, key="q3"
            )
            if repair_upcycle > 0:
                eco_points += 40 if repair_upcycle > 50 else 20
                st.info("You're giving those clothes a second chance at life! 👕✨")
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 4: True or False
            wash_in_cold = st.radio(
                "4.Do you wash your clothes in cold water?", ["", "Yes", "No"],
                key="q4", index=0
            )
            if wash_in_cold:
                eco_points += 10 if wash_in_cold == "Yes" else 0
                show_joke(3, wash_in_cold)
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 5: Multiple Choice
            carbon_neutral_shipping = st.radio(
                "5.Do you choose carbon-neutral shipping when purchasing online?",
                ["", "Always", "Sometimes", "Never"], key="q5", index=0
            )
            if carbon_neutral_shipping:
                points = {"Always": 20, "Sometimes": 10, "Never": 0}
                eco_points += points.get(carbon_neutral_shipping, 0)
                show_joke(4, carbon_neutral_shipping)
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 6: Checkbox
            donate_recycle = st.radio(
                " 6.I donate or recycle my old clothing items.",["", "Yes", "No"], key="q6",index=0
            )
            if donate_recycle:
                eco_points += 30 if donate_recycle == "Yes" else 0
                show_joke(6,donate_recycle)
                st.success("You're spreading kindness and sustainability! 🌍💚")
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 7: Multiple Choice
            secondhand_purchase = st.radio(
                "7.How often do you purchase products made from recycled materials?",
                ["", "Always", "Sometimes", "Never"], key="q7", index=0
            )
            if secondhand_purchase:
                points = {"Always": 20, "Sometimes": 10, "Never": 0}
                eco_points += points.get(secondhand_purchase, 0)
                show_joke(6, secondhand_purchase)
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 8: Multiple Choice
            reusable_bags = st.radio(
                "8.Do you bring your own reusable shopping bags when you go grocery shopping?",
                ["", "Yes", "No"], key="q8", index=0
            )
            if reusable_bags:
                eco_points += 10 if reusable_bags == "Yes" else 0
                show_joke(7, reusable_bags)
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Question 9: Checkbox
            support_sustainable_brands = st.radio(
                "9.Do you prefer shopping from brands that promote sustainable practices?",["", "Yes", "No"], key="q9",index=0
            )
            if support_sustainable_brands:
                eco_points += 30 if support_sustainable_brands == "Yes" else 0
                show_joke(8, "Yes")
                current_question += 1
                progress.progress(int((current_question / total_questions) * 100))

            # Results and Claim Button
            if current_question == total_questions:
                st.markdown(f"### 🎉 Total Eco-Savings Points: {eco_points} points")
                if st.button("Claim Your Rewards", key="claim_rewards"):
                    st.balloons()
                    # Define the offers based on points
                    # Define the offers based on points
                    if eco_points >= 500:
                        offer = {"offer": "20% discount on full cart of sustainable clothing", "code": "ECO20"}
                    elif eco_points >= 201:
                        offer = {"offer": "15% discount on eco-friendly fashion brands", "code": "ECO15"}
                    elif eco_points >= 101:
                        offer = {"offer": "10% discount on sustainable clothing items", "code": "ECO10"}
                    elif eco_points >= 50:
                        offer = {"offer": "5% discount on eco-friendly brands", "code": "ECO5"}
                    else:
                        offer = {"offer": "Keep up the great work! More rewards to come!", "code": ""}

                    # Display the single offer
                    st.markdown("### 🎁 Your Reward:")
                    st.markdown(f"**{offer['offer']}**")

                    # Display the coupon code if applicable
                    if offer["code"]:
                        st.markdown(f"### 🎉 Coupon Code: **{offer['code']}**")
                        st.text_input("Coupon Code", value=offer["code"], key="coupon_code", disabled=True)
                        st.markdown("Use this code during checkout to redeem your reward!")
                    else:
                        st.markdown("Keep participating to unlock more rewards! 🌿")


                    
            with col_right:
                # Display images in equal proportion
                st.image(
                    "https://img.freepik.com/free-vector/flat-hand-drawn-sustainable-fashion-illustration-with-hanger-clothes_23-2148831897.jpg",
                    caption="Who needs a closet of clothes when you can have one full of conscious choices?💚", use_container_width=True
                )
                st.image(
                    "https://static.vecteezy.com/system/resources/previews/026/150/150/non_2x/eco-friendly-clothing-sustainable-recycling-textile-organic-cotton-fabric-recycle-and-environmental-care-concept-on-fashion-design-illustration-vector.jpg",
                    caption="When your clothes are more eco-friendly than your Wi-Fi connection.😅", use_container_width=True
                )
                st.image(
                    "https://img.freepik.com/free-vector/flat-design-illustration-sustainable-fashion-concept_52683-55505.jpg",
                    caption="Eco-friendly? More like eco-fabulous! 🌿✨", use_container_width=True
                )
                st.image("https://www.creativefabrica.com/wp-content/uploads/2021/03/24/Sustainable-Fashion-Infographic-Graphics-9905833-1-1-580x387.jpg",caption="Always Sustainable fashion",use_container_width=True)

