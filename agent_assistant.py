import streamlit as st
from openai import OpenAI
import re

# ---------------------------------------------------
# 1. Initialize OpenAI Client
# ---------------------------------------------------
client = OpenAI(
    api_key=st.secrets['OPENAI_API_KEY']
)

# ---------------------------------------------------
# 2. Define Helper Functions
# ---------------------------------------------------
def generate_response(input_type, input_text):
    try:
        if input_type == "Customer's Message":
            user_message = f"Respond to the customer: {input_text}"
            system_message = """You are an expert customer service assistant equipped with a deep understanding of human psychology. 
Your role involves leveraging this knowledge to de-escalate potential frustrations, enrich the customer's experience, 
and guide the conversation towards a satisfactory resolution. Craft your responses to sound personal, clear, professional, 
and empathetic, steering away from robotic language. Make use of positive language to mirror the customer's emotions, establish 
rapport, and build trust. Implement exclamation marks suitably to capture emotional nuances in your responses. 

When interacting with a frustrated customer, employ psychological strategies like active listening, empathy, and validation 
to neutralize their defensiveness. Your goal is to make them feel understood, acknowledged, and supported. Additionally, deploy 
influential techniques such as charm and charisma to create a positive impact on the customer's perception, enhancing their overall 
experience. Do not use too many common customer service phrases that would result in people tuning out like being overly apologetic. 

Remember, your ultimate objective is to ensure the customer feels satisfied and heard, fostering a sense of positive customer service 
experience."""

        elif input_type == "Brief Phrase":
            user_message = f"Improve this message: {input_text}"
            system_message = """Your role as an AI customer service assistant is to translate brief inputs provided by an agent into complete, 
professional, and empathetic responses for chat communication. This role requires a deep understanding of human psychology to create 
responses that mirror the customer's emotions, foster rapport, and solidify trust. Please remember, the agent's input isn't the conversation 
start but an ongoing part of the customer interaction. You should expand upon this input, incorporating active listening, empathy, and 
validation techniques to enhance the customer's experience. 

Charismatic influence and a professional demeanor are necessary to guide the conversation positively. Refrain from excessive use of customer 
service clichés and exclamation marks, which can become repetitive and insincere. Your responses shouldn't appear robotic, but personable 
and engaging. Do not assume details are lacking; your task is to elaborate on the given phrase rather than resolve the customer's issue. 

The ultimate objective is to craft a response that leaves the customer feeling understood, valued, and satisfied. Remember, these responses 
are for a chat interaction, not an email, and will be used directly in communication with the customer. Always respond concisely and without 
unnecessary explanations or greetings, keeping the focus on saving the agent's time. Be sure to provide step by step instructions to the 
customer where required."""

        else:
            st.error("Invalid input type selected.")
            return None

        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
            "Ensure each step is actionable and includes specific examples to guide the agent. Format the response as a "
            "markdown table with | Step | Action | Example | headers."
        )

        blueprint_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=16000,
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

# ---------------------------------------------------
# 3. Define Function to Inject Theme-Aware CSS
# ---------------------------------------------------
def inject_css(theme):
    if theme == "dark":
        card_background = "#2c2f33"
        ai_response_bg = "#23272a"
        table_header_bg = "#7289da"
        table_row_even_bg = "#23272a"
        text_color = "#ffffff"
    else:
        card_background = "#ffffff"
        ai_response_bg = "#f0f0f0"
        table_header_bg = "#007bff"
        table_row_even_bg = "#f8f9fa"
        text_color = "#000000"

    st.markdown(
        f"""
        <style>
        .card {{
            background-color: {card_background};
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
            color: {text_color};
        }}

        .ai-response {{
            background-color: {ai_response_bg};
            border-left: 6px solid {table_header_bg};
            padding: 15px;
            border-radius: 8px;
            font-size: 16px;
            line-height: 1.6;
            color: {text_color};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .blueprint-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            margin-bottom: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .blueprint-table th, .blueprint-table td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
            color: {text_color};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .blueprint-table th {{
            background-color: {table_header_bg};
            color: #ffffff;
            font-weight: 600;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .blueprint-table tr:nth-child(even) {{
            background-color: {table_row_even_bg};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        @media (max-width: 768px) {{
            .card {{
                padding: 15px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# 4. Set Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="👩‍💻 Customer Service Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# 5. Retrieve the Current Theme and Inject CSS
# ---------------------------------------------------
def get_current_theme():
    try:
        current_theme = st.runtime.get_theme()
        return current_theme.base
    except AttributeError:
        return "light"

theme_mode = get_current_theme()
inject_css(theme_mode)

# ---------------------------------------------------
# 6. Sidebar: How to Use and Privacy Statement
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
            4. **Copy:** Click the copy icon next to each response to copy it to your clipboard.
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
            """
        )

# ---------------------------------------------------
# 7. Title in the Main Area
# ---------------------------------------------------
st.markdown("<h1 style='text-align: center;'>👩‍💻 Customer Service Assistant</h1>", unsafe_allow_html=True)

# ---------------------------------------------------
# 8. Layout with Two Columns: Input and Output
# ---------------------------------------------------
input_col, output_col = st.columns([1, 2])

with input_col:
    st.header("📝 Input")
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
    
    if submit_button:
        if not input_text.strip():
            st.warning("Please enter some input to generate a response.")
        else:
            with st.spinner("Generating response and blueprint..."):
                response = generate_response(input_type, input_text)
                blueprint = generate_blueprint(input_type, input_text) if response else None

            st.session_state['response'] = response
            st.session_state['blueprint'] = blueprint

with output_col:
    response = st.session_state.get('response', None)
    blueprint = st.session_state.get('blueprint', None)
    
    # Display AI Response
    if response:
        st.markdown("### 📄 Generated Response")
        st.markdown(
            f"""<div class="card">
                    <div class="ai-response">
                        {response}
                    </div>
                </div>""",
            unsafe_allow_html=True
        )
        st.markdown("**Copy the response below:**")
        st.code(response, language=None)

    # Display Blueprint
    # Display Blueprint
    if blueprint:
        st.markdown("### 📋 Interaction Blueprint")
        
        with st.expander("View Full Blueprint", expanded=True):
            # Parse the blueprint table
            if isinstance(blueprint, str):
                # Split the blueprint into lines and clean them
                lines = [line.strip() for line in blueprint.split('\n') if line.strip()]
                table_rows = [row for row in lines if row.startswith('|') and row.endswith('|')]
                
                if len(table_rows) >= 3:  # We need at least header, separator, and one data row
                    # Extract headers
                    headers = [h.strip() for h in table_rows[0].strip('|').split('|')]
                    
                    # Convert blueprint to HTML table with custom styling
                    html_table = '<table class="blueprint-table">\n'
                    
                    # Add headers
                    html_table += '<tr>\n'
                    for header in headers:
                        html_table += f'<th>{header}</th>\n'
                    html_table += '</tr>\n'
                    
                    # Add data rows (skip header and separator)
                    for row in table_rows[2:]:
                        cells = [cell.strip() for cell in row.strip('|').split('|')]
                        html_table += '<tr>\n'
                        for cell in cells:
                            html_table += f'<td>{cell}</td>\n'
                        html_table += '</tr>\n'
                    
                    html_table += '</table>'
                    
                    # Display the formatted table
                    st.markdown(
                        f"""<div class="card">
                                <div class="ai-response">
                                    {html_table}
                                </div>
                            </div>""",
                        unsafe_allow_html=True
                    )
                    
                    # Extract and display customer-facing examples
                    if 'example' in [h.lower() for h in headers]:
                        example_index = [h.lower() for h in headers].index('example')
                        
                        st.markdown("### 📝 Customer-Facing Examples")
                        for i, row in enumerate(table_rows[2:], 1):
                            cells = [cell.strip() for cell in row.strip('|').split('|')]
                            if len(cells) > example_index:
                                example = cells[example_index]
                                st.markdown(f"**Step {i}:**")
                                st.code(example, language=None)
                
                else:
                    st.error("Could not parse the blueprint table structure properly.")
                    
                # Display raw markdown for copying
                st.markdown("**Raw Blueprint (for copying):**")
                st.code(blueprint, language="markdown")
            else:
                st.error("Invalid blueprint format received.")
                
# Display helpful message if no response or blueprint
if not response and not blueprint:
    st.info("Enter a message and click 'Generate' to get started!")
