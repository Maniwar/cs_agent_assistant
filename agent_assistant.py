import streamlit as st
import pandas as pd
from io import StringIO
import re
from openai import OpenAI

# ---------------------------------------------------
# 1. Initialize OpenAI Client
# ---------------------------------------------------
client = OpenAI(
    api_key=st.secrets['OPENAI_API_KEY']
)  # Ensure your OpenAI API key is correctly set in Streamlit secrets

# ---------------------------------------------------
# 2. Define Helper Functions
# ---------------------------------------------------
def generate_response(input_type, input_text):
    try:
        if input_type == "Customer's Message":
            user_message = f"Respond to the customer: {input_text}"
            system_message = (
                "You are an expert customer service assistant equipped with a deep understanding of human psychology. "
                "Your role involves leveraging this knowledge to de-escalate potential frustrations, enrich the customer's experience, "
                "and guide the conversation towards a satisfactory resolution. Craft your responses to sound personal, clear, professional, "
                "and empathetic, steering away from robotic language. Make use of positive language to mirror the customer's emotions, establish "
                "rapport, and build trust. Implement exclamation marks suitably to capture emotional nuances in your responses. "
                "When interacting with a frustrated customer, employ psychological strategies like active listening, empathy, and validation "
                "to neutralize their defensiveness. Your goal is to make them feel understood, acknowledged, and supported. Additionally, deploy "
                "influential techniques such as charm and charisma to create a positive impact on the customer's perception, enhancing their overall "
                "experience. Do not use too many common customer service phrases that would result in people tuning out like being overly apologetic. "
                "Remember, your ultimate objective is to ensure the customer feels satisfied and heard, fostering a sense of positive customer service "
                "experience. Ensure that your responses are tailored for chat-based interaction rather than email, embodying immediacy, conversational tone, "
                "and conciseness. Your output will be copied and pasted directly to the customer."
            )
        elif input_type == "Brief Phrase":
            user_message = f"Improve this message: {input_text}"
            system_message = (
                "Your role as an AI customer service assistant is to translate brief inputs provided by an agent into complete, professional, and empathetic responses "
                "for chat communication. This role requires a deep understanding of human psychology to create responses that mirror the customer's emotions, foster rapport, "
                "and solidify trust. Please remember, the agent's input isn't the conversation start but an ongoing part of the customer interaction. You should expand upon this input, "
                "incorporating active listening, empathy, and validation techniques to enhance the customer's experience. Charismatic influence and a professional demeanor are necessary "
                "to guide the conversation positively. Refrain from excessive use of customer service clichés and exclamation marks, which can become repetitive and insincere. "
                "Your responses shouldn't appear robotic, but personable and engaging. Do not assume details are lacking; your task is to elaborate on the given phrase rather than resolve the customer's issue. "
                "The ultimate objective is to craft a response that leaves the customer feeling understood, valued, and satisfied. Remember, these responses are for a chat interaction, not an email, and will be used directly "
                "in communication with the customer. Always respond concisely and without unnecessary explanations or greetings, keeping the focus on saving the agent's time. Be sure to provide step by step instructions to the customer where required."
            )
        else:
            st.error("Invalid input type selected.")
            return None

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure this is the correct model name
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
            max_tokens=16000,
            n=1,
            stop=None,
            presence_penalty=0,
            frequency_penalty=0,
            user="user-identifier"
        )

        ai_response = response.choices[0].message.content.strip()
        # Remove "Response: " prefix if present
        if ai_response.lower().startswith("response:"):
            ai_response = ai_response[len("response:"):].strip()

        return ai_response

    except Exception as e:
        st.error(f"An error occurred while generating the response: {e}")
        return None

def generate_blueprint(input_type, input_text):
    try:
        if input_type == "Customer's Message":
            user_message = (
                f"Based on the following customer message, provide a step-by-step interaction blueprint focusing on loyalty, ownership, and trust. "
                f"Present it in a table format with columns: Step, Action, Example.\n\nCustomer Message: {input_text}"
            )
        elif input_type == "Brief Phrase":
            user_message = (
                f"Based on the following brief phrase, provide a step-by-step interaction blueprint focusing on loyalty, ownership, and trust. "
                f"Present it in a table format with columns: Step, Action, Example.\n\nBrief Phrase: {input_text}"
            )
        else:
            st.error("Invalid input type selected.")
            return None

        system_message = (
            "You are an expert in customer service interactions. Based on the provided input, create a detailed "
            "blueprint that outlines a step-by-step strategy for handling the interaction. Focus on fostering loyalty, "
            "ownership, and trust. Present the blueprint in a clear table format with three columns: Step, Action, Example. "
            "Ensure each step is actionable and includes specific examples to guide the agent."
        )

        blueprint_response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure this is the correct model name
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=4000,
            n=1,
            stop=None,
            presence_penalty=0,
            frequency_penalty=0,
            user="user-identifier"
        ).choices[0].message.content.strip()

        return blueprint_response

    except Exception as e:
        st.error(f"An error occurred while generating the blueprint: {e}")
        return None

def parse_markdown_table(md_table):
    # Extract the markdown table using regex
    table_match = re.findall(r'\|.*\|', md_table)
    if not table_match:
        return None

    # Find the starting point of the table
    table_start = None
    for i, line in enumerate(table_match):
        if re.match(r'\|[-:]+\|', line):
            table_start = i
            break

    if table_start is None:
        return None

    # Extract the table from the matched lines
    table_str = "\n".join(table_match[table_start - 1:])

    # Read the table into a DataFrame
    try:
        df = pd.read_csv(StringIO(table_str), sep='|').dropna(axis=1, how='all').dropna(axis=0, how='all')
        # Remove leading and trailing whitespace from headers and columns
        df.columns = [col.strip() for col in df.columns]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"Error parsing table: {e}")
        return None

# ---------------------------------------------------
# 3. Define Helper Function for Copying to Clipboard
# ---------------------------------------------------
def get_clipboard_js(text):
    """
    Generates JavaScript code to copy the provided text to the clipboard.
    """
    clipboard_js = f"""
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            alert('Copied to clipboard!');
        }}, function(err) {{
            alert('Failed to copy text.');
        }});
    }}
    </script>
    """
    return clipboard_js

# ---------------------------------------------------
# 4. Define Function to Inject Theme-Aware CSS
# ---------------------------------------------------
def inject_css(theme):
    # Define colors based on the theme
    if theme == "dark":
        card_background = "#2c2f33"
        ai_response_bg = "#23272a"
        ai_response_border = "#7289da"
        table_header_bg = "#7289da"
        table_row_even_bg = "#23272a"
        button_bg = "#7289da"
        button_hover_bg = "#99aab5"
        text_color = "#ffffff"
    else:
        # Light theme colors
        card_background = "#ffffff"
        ai_response_bg = "#f0f0f0"
        ai_response_border = "#007bff"
        table_header_bg = "#007bff"
        table_row_even_bg = "#f8f9fa"
        button_bg = "#007bff"
        button_hover_bg = "#0056b3"
        text_color = "#000000"

    st.markdown(
        f"""
        <style>
        /* General Card Styling */
        .card {{
            background-color: {card_background};
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
            color: {text_color};
        }}

        /* AI Response Styling */
        .ai-response {{
            background-color: {ai_response_bg};
            border-left: 6px solid {ai_response_border};
            padding: 15px;
            border-radius: 8px;
            font-size: 16px;
            line-height: 1.6;
            color: {text_color};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* Blueprint Table Styling */
        table.blueprint-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        table.blueprint-table th, table.blueprint-table td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
            color: {text_color};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        table.blueprint-table th {{
            background-color: {table_header_bg};
            color: #ffffff;
            font-weight: 600;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        table.blueprint-table tr:nth-child(even) {{
            background-color: {table_row_even_bg};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* Button Styling */
        .copy-button {{
            background-color: {button_bg};
            color: white;
            border: none;
            padding: 10px 16px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin-top: 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        .copy-button:hover {{
            background-color: {button_hover_bg};
        }}

        /* Responsive Layout */
        @media (max-width: 768px) {{
            .card {{
                padding: 15px;
            }}

            .copy-button {{
                width: 100%;
                padding: 12px 0;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# 5. Set Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="👩‍💻 Customer Service Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# 6. Retrieve the Current Theme and Inject CSS
# ---------------------------------------------------
def get_current_theme():
    try:
        current_theme = st.runtime.get_theme()
        return current_theme.base  # 'dark' or 'light'
    except AttributeError:
        # Fallback for older Streamlit versions
        return "light"

theme_mode = get_current_theme()
inject_css(theme_mode)

# ---------------------------------------------------
# 7. Sidebar: How to Use and Privacy Statement
# ---------------------------------------------------
with st.sidebar:
    with st.sidebar.expander("ℹ️ How to Use"):
        st.markdown(
            """
            This app generates professional and empathetic responses to customer inquiries.

            **Steps to Use:**
            1. **Input Type:** Choose between a full customer message or a brief phrase.
            2. **Enter Input:** Provide the customer's message or the brief phrase.
            3. **Generate:** Click the "Generate" button to receive a response and a tailored interaction blueprint.
            4. **Copy:** Use the "Copy Response" and "Copy Blueprint" buttons to copy the generated content for your communications.
            """
        )
    
    with st.sidebar.expander("🔒 Data Privacy Statement"):
        st.markdown(
            """
            **Information Collection:** The App collects the customer inquiries and agent phrases you enter when using the App. These inputs are securely transmitted to OpenAI's GPT model to generate professional and empathetic responses.
            
            **Information Usage:** Your inquiries and phrases are solely used to provide the App's services, which include generating appropriate responses using OpenAI's GPT model. All data are treated as confidential and are not shared with third parties for any other purpose.
            
            **Data Security:** We take data security seriously. We implement measures to protect your data during transmission and storage. However, it's important to note that no system is entirely immune to potential security risks. We recommend avoiding the inclusion of any personally identifiable information or sensitive data in your inquiries or phrases.
            
            **Data Retention:** We do not retain your data beyond the immediate scope of generating the AI response. Once the response is generated, any stored copies of your data are promptly deleted.
            
            **OpenAI Data Sharing:** By using this app, you agree to share your input data with OpenAI and acknowledge that OpenAI's terms and conditions apply to the processing and use of your data by OpenAI.
            
            If you have any concerns or questions about the data privacy practices of the App, please don't hesitate to contact us.
            """
        )

# ---------------------------------------------------
# 8. Title in the Main Area
# ---------------------------------------------------
st.markdown("<h1 style='text-align: center;'>👩‍💻 Customer Service Assistant</h1>", unsafe_allow_html=True)

# ---------------------------------------------------
# 9. Layout with Two Columns: Input and Output
# ---------------------------------------------------
input_col, output_col = st.columns([1, 2])

with input_col:
    st.header("📝 Input")
    # Use Streamlit's form to handle input submission
    with st.form(key='input_form'):
        input_type = st.radio(
            "Choose the type of input",
            ("Customer's Message", "Brief Phrase"),
            key="input_type",
        )
        input_text = st.text_area(
            "Enter Your Input",
            key="input_text",
            height=200,
        )
        submit_button = st.form_submit_button(label='Generate')
    
    # Prevent empty submissions by validating input
    if submit_button:
        if not input_text.strip():
            st.warning("Please enter some input to generate a response.")
        else:
            with st.spinner("Generating response and blueprint..."):
                response = generate_response(input_type, input_text)
                blueprint = generate_blueprint(input_type, input_text) if response else None

            # Store responses in session state to prevent resets
            st.session_state['response'] = response
            st.session_state['blueprint'] = blueprint

with output_col:
    # Retrieve responses from session state
    response = st.session_state.get('response', None)
    blueprint = st.session_state.get('blueprint', None)
    
    # ---------------------------------------------------
    # 10. Display AI Response
    # ---------------------------------------------------
    if response:
        st.markdown("### 📄 Generated Response")
        response_div_id = "aiResponse"
        st.markdown(
            f"""<div class="ai-response" id="{response_div_id}">
                {response}
            </div>""",
            unsafe_allow_html=True
        )
        # Copy Response Button
        if st.button("📋 Copy Response"):
            st.write(f'<script>copyToClipboard("{response_div_id}")</script>', unsafe_allow_html=True)
            st.success("Response copied to clipboard!")

    # ---------------------------------------------------
    # 11. Display Blueprint
    # ---------------------------------------------------
    if blueprint:
        blueprint_df = parse_markdown_table(blueprint)
        if blueprint_df is not None:
            st.markdown("### 📋 Interaction Blueprint")
            blueprint_div_id = "blueprint"
            st.markdown(
                f"""<div class="card" id="{blueprint_div_id}">
                    {blueprint_df.to_html(index=False, classes='blueprint-table')}
                </div>""",
                unsafe_allow_html=True
            )
            # Copy Blueprint Button
            if st.button("📋 Copy Blueprint"):
                st.write(f'<script>copyToClipboard("{blueprint_div_id}")</script>', unsafe_allow_html=True)
                st.success("Blueprint copied to clipboard!")
        else:
            st.warning("Could not parse the blueprint table. Please ensure the AI provides a valid markdown table.")
            st.text(blueprint)

# ---------------------------------------------------
# 12. Inject JavaScript for Copy Functionality
# ---------------------------------------------------
def get_clipboard_js():
    clipboard_js = """
    <script>
    function copyToClipboard(elementId) {
        var element = document.getElementById(elementId);
        if (element) {
            var textarea = document.createElement("textarea");
            textarea.value = element.innerText;
            document.body.appendChild(textarea);
            textarea.select();
            try {
                var successful = document.execCommand('copy');
                if (successful) {
                    // Notify Streamlit about the successful copy
                    Streamlit.setComponentValue("copied");
                } else {
                    Streamlit.setComponentValue("failed");
                }
            } catch (err) {
                Streamlit.setComponentValue("failed");
            }
            document.body.removeChild(textarea);
        } else {
            Streamlit.setComponentValue("element_not_found");
        }
    }
    </script>
    """
    return clipboard_js

st.markdown(get_clipboard_js(), unsafe_allow_html=True)
