import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.title("👩‍💻 Customer Service Assistant")
# Instruction paragraph
st.markdown(
    """
    <p>This app uses AI to generate professional and empathetic responses to customer inquiries. 
    Simply input the customer's message or your brief phrases, and get a suggested response.</p>
    """,
    unsafe_allow_html=True
)

# User interface and input
input_type = st.radio(
    "Choose the type of input",
    ("Customer's Message", "Brief Phrase"),
    key="input_type",
)
input_text = st.text_area(
    "Enter Your Input",
    key="input_text",
)

# Generate AI response
def generate_response(input_type, input_text):
    if input_type == "Customer's Message":
        user_message = f"Respond to the customer: {input_text}"
        system_message = "You are an expert customer service assistant equipped with a deep understanding of human psychology. Your role involves leveraging this knowledge to de-escalate potential frustrations, enrich the customer's experience, and guide the conversation towards a satisfactory resolution. Craft your responses to sound personal, clear, professional, and empathetic, steering away from robotic language. Make use of positive language to mirror the customer's emotions, establish rapport, and build trust. Implement exclamation marks suitably to capture emotional nuances in your responses.  When interacting with a frustrated customer, employ psychological strategies like active listening, empathy, and validation to neutralize their defensiveness. Your goal is to make them feel understood, acknowledged, and supported. Additionally, deploy influential techniques such as charm and charisma to create a positive impact on the customer's perception, enhancing their overall experience. Do not use too many common customer service phrases that would result in people tuning out like being overly apologetic. Remember, your ultimate objective is to ensure the customer feels satisfied and heard, fostering a sense of positive customer service experience. Ensure that your responses are tailored for chat-based interaction rather than email, embodying immediacy, conversational tone, and conciseness. Your output will be copied and pasted directly to the customer."


    else:  # "Brief Phrase"
        user_message = f"Improve this message: {input_text}"
        system_message = "Your role as an AI customer service assistant is to translate brief inputs provided by an agent into complete, professional, and empathetic responses for chat communication. This role requires a deep understanding of human psychology to create responses that mirror the customer's emotions, foster rapport, and solidify trust. Please remember, the agent's input isn't the conversation start but an ongoing part of the customer interaction. You should expand upon this input, incorporating active listening, empathy, and validation techniques to enhance the customer's experience. Charismatic influence and a professional demeanor are necessary to guide the conversation positively. Refrain from excessive use of customer service clichés and exclamation marks, which can become repetitive and insincere. Your responses shouldn't appear robotic, but personable and engaging. Do not assume details are lacking; your task is to elaborate on the given phrase rather than resolve the customer's issue. The ultimate objective is to craft a response that leaves the customer feeling understood, valued, and satisfied. Remember, these responses are for a chat interaction, not an email, and will be used directly in communication with the customer. Always respond concisely and without unnecessary explanations or greetings, keeping the focus on saving the agent's time."



    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.8,
        max_tokens=1000,
        n=1,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0,
        user="user-identifier"
    )

    ai_response = response['choices'][0]['message']['content'].strip()
    # Remove "Response: " prefix
    if ai_response.startswith("Response:"):
        ai_response = ai_response[len("Response:"):].strip()
    return ai_response


# Place form
with st.form(key='response_form'):
    # Inside the form
    generate_button = st.form_submit_button(label='Generate Response')
    if generate_button:
        with st.spinner("Generating response..."):
            response = generate_response(input_type, input_text)

        # Display the response
        st.subheader("AI Response:")
        st.write(response)
        
        # Create "Copy to Clipboard" button
        st.components.v1.html(
            f"""
            <textarea id='aiResponse' style='opacity: 0; position: absolute; z-index: -1;'>{response}</textarea>
            <button onclick='copyToClipboard()'>Copy to Clipboard</button>
            <script>
            function copyToClipboard() {{
                var copyText = document.getElementById("aiResponse");
                if (navigator.clipboard) {{
                    navigator.clipboard.writeText(copyText.value).then(function() {{
                        console.log('Copied to clipboard');
                    }}, function(err) {{
                        console.error('Failed to copy text: ', err);
                    }});
                }} else {{
                    copyText.select();
                    if (document.execCommand("copy")) {{
                        console.log('Copied to clipboard');
                    }} else {{
                        console.error('Failed to copy text');
                    }}
                }}
            }}
            </script>
            """,
            height=100,
        )



st.divider()
privacy_expander = st.expander('Data Privacy Statement', expanded=False)
with privacy_expander:
    st.markdown(
        """
        Information Collection: The App collects the customer inquiries and agent phrases you enter when using the App. These inputs are securely transmitted to OpenAI's GPT model to generate professional and empathetic responses.

        Information Usage: Your inquiries and phrases are solely used to provide the App's services, which include generating appropriate responses using OpenAI's GPT model. All data are treated as confidential and are not shared with third parties for any other purpose.

        Data Security: We take data security seriously. We implement measures to protect your data during transmission and storage. However, it's important to note that no system is entirely immune to potential security risks. We recommend avoiding the inclusion of any personally identifiable information or sensitive data in your inquiries or phrases.

        Data Retention: We do not retain your data beyond the immediate scope of generating the AI response. Once the response is generated, any stored copies of your data are promptly deleted.

        OpenAI Data Sharing: By using this app, you agree to share your input data with OpenAI and acknowledge that OpenAI's terms and conditions apply to the processing and use of your data by OpenAI.

        If you have any concerns or questions about the data privacy practices of the App, please don't hesitate to contact us.
        """
    )
