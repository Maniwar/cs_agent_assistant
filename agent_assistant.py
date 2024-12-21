from openai import OpenAI
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

# Title and Description
st.title("👩‍💻 Customer Service Assistant")

st.markdown(
    """
    <p>This app leverages AI to generate professional and empathetic responses to customer inquiries.
    Input the customer's message or your brief phrases, and receive a suggested response.
    Additionally, receive a tailored blueprint to guide your interaction towards fostering loyalty, ownership, and trust.</p>
    """,
    unsafe_allow_html=True
)

# Agent Prompt Suggestions Section
st.header("💡 Agent Prompt Suggestions")
agent_prompt = """
- **Acknowledge** the customer's concern to show understanding.
- **Express empathy** to connect on an emotional level.
- **Take ownership** by assuring the customer you will address their issue.
- **Provide a clear solution** or the next steps to resolve the problem.
- **Invite further communication** to reinforce trust and loyalty.
"""

st.markdown(agent_prompt)

st.divider()

# User Input Section
st.header("📝 Input Section")
input_type = st.radio(
    "Choose the type of input",
    ("Customer's Message", "Brief Phrase"),  # "Create Keyphrase"),
    key="input_type",
)

input_text = st.text_area(
    "Enter Your Input",
    key="input_text",
)

# Function to generate AI response
def generate_response(input_type, input_text):
    if input_type == "Customer's Message":
        user_message = f"Respond to the customer: {input_text}"
        system_message = (
            "You are an expert customer service assistant with a strong foundation in human psychology. "
            "Your objective is to de-escalate any frustrations, enhance the customer's experience, and guide the "
            "conversation towards a satisfactory resolution. Emphasize loyalty, ownership, and trust in your responses. "
            "Use personal, clear, professional, and empathetic language. Avoid robotic phrasing and excessive apologies. "
            "Incorporate positive language to mirror the customer's emotions, build rapport, and establish trust. "
            "When addressing a frustrated customer, utilize active listening, empathy, and validation to make them feel "
            "understood and supported. Apply charismatic and charming techniques to positively influence the customer's perception. "
            "Ensure responses are concise, conversational, and tailored for chat-based interaction."
        )
    elif input_type == "Brief Phrase":
        user_message = f"Improve this message: {input_text}"
        system_message = (
            "As an AI customer service assistant, your role is to expand brief inputs from agents into complete, "
            "professional, and empathetic responses for chat communication. Focus on loyalty, ownership, and trust. "
            "Incorporate active listening, empathy, and validation to enhance the customer's experience. "
            "Avoid overused customer service clichés and excessive exclamation marks to maintain sincerity. "
            "Ensure responses are personable, engaging, and concise, suitable for direct communication with customers."
        )
    # Uncomment and adjust if "Create Keyphrase" is needed in the future
    # elif input_type == "Create Keyphrase":
    #     user_message = f"Generate keyphrases for the following subcategories: {input_text}"
    #     system_message = (
    #         "Your task is to generate keyphrases or short sentences that customers might use to discuss or inquire "
    #         "about the given subcategories. These should reflect common customer service complaints or NPS detractor comments. "
    #         "Ensure relevance, conciseness, and alignment with each subcategory's essence. Format the output as a dictionary."
    #     )

    response = client.chat.completions.create(
        model="gpt4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=800,  # Adjusted for gpt4o-mini
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

# Function to generate Blueprint
def generate_blueprint(input_type, input_text):
    if input_type == "Customer's Message":
        user_message = f"Based on the following customer message, provide a step-by-step interaction blueprint focusing on loyalty, ownership, and trust. Present it in a table format with columns: Step, Action, Example.\n\nCustomer Message: {input_text}"
    elif input_type == "Brief Phrase":
        user_message = f"Based on the following brief phrase, provide a step-by-step interaction blueprint focusing on loyalty, ownership, and trust. Present it in a table format with columns: Step, Action, Example.\n\nBrief Phrase: {input_text}"
    # elif input_type == "Create Keyphrase":
    #     # Adjust accordingly if needed
    #     user_message = f"Generate a blueprint based on the following keyphrase: {input_text}"
    #     # Define system_message if necessary

    system_message = (
        "You are an expert in customer service interactions. Based on the provided input, create a detailed "
        "blueprint that outlines a step-by-step strategy for handling the interaction. Focus on fostering loyalty, "
        "ownership, and trust. Present the blueprint in a clear table format with three columns: Step, Action, Example. "
        "Ensure each step is actionable and includes specific examples to guide the agent."
    )

    response = client.chat.completions.create(
        model="gpt4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=1000,  # Adjusted for gpt4o-mini
        n=1,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0,
        user="user-identifier"
    )

    blueprint_response = response.choices[0].message.content.strip()
    return blueprint_response

# Function to parse markdown table to DataFrame
def parse_markdown_table(md_table):
    # Extract the markdown table using regex
    table_match = re.findall(r'\|.*\|', md_table)
    if not table_match:
        return None

    # Join the table lines
    table_str = "\n".join(table_match)

    # Read the table into a DataFrame
    df = pd.read_csv(StringIO(table_str), sep='|').dropna(axis=1, how='all').dropna(axis=0, how='all')
    # Remove leading and trailing whitespace from headers and columns
    df.columns = [col.strip() for col in df.columns]
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

# Place form
with st.form(key='response_form'):
    generate_button = st.form_submit_button(label='Generate Response')
    if generate_button:
        if not input_text.strip():
            st.warning("Please enter some input to generate a response.")
        else:
            with st.spinner("Generating response and blueprint..."):
                response = generate_response(input_type, input_text)
                blueprint = generate_blueprint(input_type, input_text)

            # Display the AI Response
            st.subheader("📝 AI Response:")
            response_with_line_breaks = response.replace('\n', '<br>')
            st.markdown(response_with_line_breaks, unsafe_allow_html=True)  # Render HTML line breaks

            # Create "Copy to Clipboard" button for AI Response
            st.components.v1.html(
                f"""
                <textarea id='aiResponse' style='opacity: 0; position: absolute; z-index: -1;'>{response}</textarea>
                <button onclick='copyToClipboard("aiResponse")' style='margin-top:10px;'>📋 Copy Response</button>
                <script>
                function copyToClipboard(elementId) {{
                    var copyText = document.getElementById(elementId);
                    if (navigator.clipboard) {{
                        navigator.clipboard.writeText(copyText.value).then(function() {{
                            alert('Response copied to clipboard!');
                        }}, function(err) {{
                            alert('Failed to copy text: ' + err);
                        }});
                    }} else {{
                        copyText.select();
                        document.execCommand("copy");
                        alert('Response copied to clipboard!');
                    }}
                }}
                </script>
                """,
                height=100,
            )

            st.divider()

            # Display the Dynamic Blueprint
            st.subheader("📋 Interaction Blueprint:")
            st.markdown(
                """
                <p>The following blueprint provides a tailored step-by-step strategy to handle this customer interaction effectively, focusing on fostering loyalty, ownership, and trust.</p>
                """,
                unsafe_allow_html=True
            )

            # Attempt to parse the blueprint_response into a DataFrame
            blueprint_df = parse_markdown_table(blueprint)

            if blueprint_df is not None:
                st.table(blueprint_df)
            else:
                st.warning("Could not parse the blueprint table. Please ensure the AI provides a valid markdown table.")
                st.text(blueprint)

            # Create "Copy to Clipboard" button for Blueprint
            st.components.v1.html(
                f"""
                <textarea id='blueprintResponse' style='opacity: 0; position: absolute; z-index: -1;'>{blueprint}</textarea>
                <button onclick='copyToClipboard("blueprintResponse")' style='margin-top:10px;'>📋 Copy Blueprint</button>
                <script>
                function copyToClipboard(elementId) {{
                    var copyText = document.getElementById(elementId);
                    if (navigator.clipboard) {{
                        navigator.clipboard.writeText(copyText.value).then(function() {{
                            alert('Blueprint copied to clipboard!');
                        }}, function(err) {{
                            alert('Failed to copy text: ' + err);
                        }});
                    }} else {{
                        copyText.select();
                        document.execCommand("copy");
                        alert('Blueprint copied to clipboard!');
                    }}
                }}
                </script>
                """,
                height=100,
            )

st.divider()

# Privacy Statement Section
privacy_expander = st.expander('🔒 Data Privacy Statement', expanded=False)
with privacy_expander:
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
