import OpenAI
import streamlit as st
import pandas as pd
from io import StringIO
import re

# Initialize OpenAI client with the specified model
client = OpenAI(
    api_key=st.secrets['OPENAI_API_KEY']
)  # This is also the default, it can be omitted

# Configure the Streamlit page
st.set_page_config(page_title="👩‍💻 Customer Service Assistant", layout="wide")

# Title
st.title("👩‍💻 Customer Service Assistant")

# Collapsible Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown(
        """
        This app generates professional and empathetic responses to customer inquiries. 
        - **Input Type:** Choose between a full customer message or a brief phrase.
        - **Generate:** Click the "Generate" button to receive a response and a tailored interaction blueprint.
        - **Copy:** Use the provided buttons to copy the generated content for use in your communications.
        """
    )

# Layout with two columns: Input and Output
input_col, output_col = st.columns([1, 2])

with input_col:
    st.header("📝 Input")
    # User interface and input
    input_type = st.radio(
        "Choose the type of input",
        ("Customer's Message", "Brief Phrase"),  # "Create Keyphrase"),
        key="input_type",
    )
    input_text = st.text_area(
        "Enter Your Input",
        key="input_text",
        height=200,
    )
    generate_button = st.button(label='Generate', key='generate_button')

with output_col:
    if generate_button:
        if not input_text.strip():
            st.warning("Please enter some input to generate a response.")
        else:
            with st.spinner("Generating response and blueprint..."):
                # Function to generate AI response
                def generate_response(input_type, input_text):
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
                    
                    try:
                        response = client.chat.completions.create(
                            model="gpt4o-mini",
                            messages=[
                                {"role": "system", "content": system_message},
                                {"role": "user", "content": user_message}
                            ],
                            temperature=0.3,
                            max_tokens=4000,  # Adjusted as per original code
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
                    except OpenAI.InvalidRequestError as e:
                        st.error(f"Invalid Request: {e}")
                    except OpenAI.AuthenticationError as e:
                        st.error(f"Authentication Error: {e}")
                    except OpenAI.APIConnectionError as e:
                        st.error(f"API Connection Error: {e}")
                    except OpenAI.OpenAIError as e:
                        st.error(f"An error occurred: {e}")
                    return None
                
                # Function to generate Blueprint
                def generate_blueprint(input_type, input_text):
                    if input_type == "Customer's Message":
                        user_message = f"Based on the following customer message, provide a step-by-step interaction blueprint focusing on loyalty, ownership, and trust. Present it in a table format with columns: Step, Action, Example.\n\nCustomer Message: {input_text}"
                    elif input_type == "Brief Phrase":
                        user_message = f"Based on the following brief phrase, provide a step-by-step interaction blueprint focusing on loyalty, ownership, and trust. Present it in a table format with columns: Step, Action, Example.\n\nBrief Phrase: {input_text}"
                    
                    system_message = (
                        "You are an expert in customer service interactions. Based on the provided input, create a detailed "
                        "blueprint that outlines a step-by-step strategy for handling the interaction. Focus on fostering loyalty, "
                        "ownership, and trust. Present the blueprint in a clear table format with three columns: Step, Action, Example. "
                        "Ensure each step is actionable and includes specific examples to guide the agent."
                    )
                
                    try:
                        blueprint_response = client.chat.completions.create(
                            model="gpt4o-mini",
                            messages=[
                                {"role": "system", "content": system_message},
                                {"role": "user", "content": user_message}
                            ],
                            temperature=0.3,
                            max_tokens=4000,  # Adjusted as per original code
                            n=1,
                            stop=None,
                            presence_penalty=0,
                            frequency_penalty=0,
                            user="user-identifier"
                        ).choices[0].message.content.strip()
                
                        return blueprint_response
                    except OpenAI.InvalidRequestError as e:
                        st.error(f"Invalid Request: {e}")
                    except OpenAI.AuthenticationError as e:
                        st.error(f"Authentication Error: {e}")
                    except OpenAI.APIConnectionError as e:
                        st.error(f"API Connection Error: {e}")
                    except OpenAI.OpenAIError as e:
                        st.error(f"An error occurred: {e}")
                    return None
                
                # Function to parse markdown table to DataFrame
                def parse_markdown_table(md_table):
                    # Extract the markdown table using regex
                    table_match = re.findall(r'\|.*\|', md_table)
                    if not table_match:
                        return None
                
                    # Join the table lines
                    table_str = "\n".join(table_match)
                
                    # Read the table into a DataFrame
                    try:
                        df = pd.read_csv(StringIO(table_str), sep='|').dropna(axis=1, how='all').dropna(axis=0, how='all')
                        # Remove leading and trailing whitespace from headers and columns
                        df.columns = [col.strip() for col in df.columns]
                        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                        return df
                    except Exception as e:
                        st.error(f"Error parsing the blueprint table: {e}")
                        return None
                
                # Generate AI Response and Blueprint
                response = generate_response(input_type, input_text)
                blueprint = generate_blueprint(input_type, input_text) if response else None
                
                # Display AI Response
                if response:
                    with st.container():
                        st.markdown("### 📝 AI Response:")
                        st.markdown(
                            response.replace('\n', '<br>'),
                            unsafe_allow_html=True
                        )
                        # Copy Button for AI Response
                        st.markdown(
                            """
                            <div style="margin-top:10px;">
                                <button onclick="copyToClipboard('aiResponse')" style="padding:5px 10px; background-color:#4CAF50; color:white; border:none; border-radius:4px; cursor:pointer;">
                                    📋 Copy Response
                                </button>
                                <textarea id="aiResponse" style="opacity:0; position:absolute; left:-9999px;">{}</textarea>
                            </div>
                            <script>
                            function copyToClipboard(elementId) {{
                                var copyText = document.getElementById(elementId);
                                copyText.style.display = "block";
                                copyText.select();
                                copyText.setSelectionRange(0, 99999); /* For mobile devices */
                                document.execCommand("copy");
                                copyText.style.display = "none";
                                alert("AI Response copied to clipboard!");
                            }}
                            </script>
                            """.format(response)
                        )
                
                # Display Blueprint
                if blueprint:
                    with st.container():
                        st.markdown("### 📋 Interaction Blueprint:")
                        st.markdown(
                            """
                            The following blueprint provides a tailored step-by-step strategy to handle this customer interaction effectively, focusing on fostering loyalty, ownership, and trust.
                            """
                        )
                        # Attempt to parse the blueprint_response into a DataFrame
                        blueprint_df = parse_markdown_table(blueprint)
                
                        if blueprint_df is not None:
                            st.table(blueprint_df)
                        else:
                            st.warning("Could not parse the blueprint table. Please ensure the AI provides a valid markdown table.")
                            st.text(blueprint)
                
                        # Copy Button for Blueprint
                        st.markdown(
                            """
                            <div style="margin-top:10px;">
                                <button onclick="copyToClipboard('blueprintResponse')" style="padding:5px 10px; background-color:#4CAF50; color:white; border:none; border-radius:4px; cursor:pointer;">
                                    📋 Copy Blueprint
                                </button>
                                <textarea id="blueprintResponse" style="opacity:0; position:absolute; left:-9999px;">{}</textarea>
                            </div>
                            <script>
                            function copyToClipboard(elementId) {{
                                var copyText = document.getElementById(elementId);
                                copyText.style.display = "block";
                                copyText.select();
                                copyText.setSelectionRange(0, 99999); /* For mobile devices */
                                document.execCommand("copy");
                                copyText.style.display = "none";
                                alert("Blueprint copied to clipboard!");
                            }}
                            </script>
                            """.format(blueprint)
                        )
    
# Collapsible Privacy Statement
with st.expander('🔒 Data Privacy Statement', expanded=False):
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
