import os
import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Instruction paragraph
st.markdown(
    """
    <h3>👩‍💼 Professional and Empathetic Customer Service Assistant</h3>
    <p>This app uses AI to generate professional and empathetic responses to customer inquiries. 
    Simply input the customer's message or your brief phrases, and get a suggested response.</p>
    """,
    unsafe_allow_html=True
)

# User interface and input
st.title("Customer Service Assistant")
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
        user_message = f"Customer: {input_text}"
        system_message = "You are an expert customer service assistant equipped with a deep understanding of human psychology. Your role involves leveraging this knowledge to de-escalate potential frustrations, enrich the customer's experience, and guide the conversation towards a satisfactory resolution. Craft your responses to sound personal, clear, professional, and empathetic, steering away from robotic language. Make use of positive language to mirror the customer's emotions, establish rapport, and build trust. Implement exclamation marks suitably to capture emotional nuances in your responses.  When interacting with a frustrated customer, employ psychological strategies like active listening, empathy, and validation to neutralize their defensiveness. Your goal is to make them feel understood, acknowledged, and supported. Additionally, deploy influential techniques such as charm and charisma to create a positive impact on the customer's perception, enhancing their overall experience. Remember, your ultimate objective is to ensure the customer feels satisfied and heard, fostering a sense of positive customer service experience. Ensure that your responses are tailored for chat-based interaction rather than email, embodying immediacy, conversational tone, and conciseness. Your output will be copied and pasted directly to the customer."


    else:  # "Brief Phrase"
        user_message = f"Agent: {input_text}"
        system_message = "You are an empathetic customer service assistant with a deep understanding of human psychology. Your role is to interpret brief inputs provided by a customer service agent and transform them into complete, professional, and empathetic responses suitable for chat communications. You are not a customer, but an assistant supporting the agent. It's important to understand that the agent's brief inputs are not the start of the conversation, but part of ongoing interactions with the customer. Based on these agent inputs, you are to craft personable, non-robotic responses. Utilize positive language and empathy to mirror the customer's emotions, build rapport, and reinforce trust. Employ exclamation marks judiciously to convey appropriate emotional undertones. Leverage psychological techniques such as active listening, empathy, and validation to create a positive customer perception and enhance their experience. Influence the conversation using charm and charisma, all while maintaining a professional demeanor. The ultimate goal is to expand the agent's brief input into a response that leaves the customer feeling understood, satisfied, and valued. Remember: you're crafting responses for a chat interaction, not an email, and your output will be used directly in communication with the customer."



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
            <button onclick='myFunction()'>Copy to Clipboard</button>
            <script>
            function myFunction() {{
            /* Get the text field */
            var copyText = document.getElementById("aiResponse");

            /* Select the text field */
            copyText.select();
            copyText.setSelectionRange(0, 99999); /* For mobile devices */

            /* Copy the text inside the text field */
            navigator.clipboard.writeText(copyText.value);

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
