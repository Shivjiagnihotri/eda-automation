# Tika setup
import streamlit as st
from tika import parser
from transformers import pipeline
# Streamlit UI
import time
import streamlit as st
import warnings
warnings.simplefilter('ignore')
import nltk
from pdfminer.high_level import extract_text
import re
import tika
from tika import parser
from transformers import pipeline
nltk.download('punkt')


# [theme]
# backgroundColor = "#FFFFFF"



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.set_page_config(page_title='My Beautiful Streamlit App', page_icon='🌼')

st.title("AI Powered summarization tool by dotkonnekt 🚀")
# st.title('PDF Summarizer')

st.header(' \n')
# st.header('AI Powered summarization tool by Dotkonnekt')

st.markdown('''📣 Are you tired of reading through lengthy PDFs? Do you wish you could get the gist of a document in just a few sentences? Look no further! The PDF Summarizer Tool by DotKonnekt is here to revolutionize the way you consume information.

This innovative tool uses advanced AI algorithms to extract key points from your PDFs, providing you with a concise summary in seconds. No more sifting through pages of text - get the information you need quickly and efficiently.

Here's what makes our tool stand out:
- 🚀 **Fast**: Get your summaries in seconds.
- 🧠 **Smart**: Uses AI to understand context and extract key points.
- 📚 **Versatile**: Perfect for academic papers, reports, books, and more.
- 🔒 **Secure**: Your documents are safe with us. We respect your privacy.

So why wait? Give the PDF Summarizer Tool by DotKonnekt a try today and experience the future of reading! 🎉😊👍💻📊🚀''')

# global summary_length
global summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")  

def extract_doc_text(pdf_path):
  document_text = ""
  try:
    parsed = parser.from_file(pdf_path)
    document_text = parsed["content"]
    document_text = re.sub('([ \t]+)|([\n]+)', lambda m: ' ' if m.group(1) else '\n', document_text)
  except:
    document_text = extract_text(pdf_path, caching=True, codec='utf-8')

  return document_text

def prep_b4_save(text):
    text = re.sub('Gods', 'God\'s', text)
    text = re.sub('yours', 'your\'s', text)
    text = re.sub('dont', 'don\'t', text)
    text = re.sub('doesnt', 'doesn\'t', text)
    text = re.sub('isnt', 'isn\'t', text)
    text = re.sub('havent', 'haven\'t', text)
    text = re.sub('hasnt', 'hasn\'t', text)
    text = re.sub('wouldnt', 'wouldn\'t', text)
    text = re.sub('theyre', 'they\'re', text)
    text = re.sub('youve', 'you\'ve', text)
    text = re.sub('arent', 'aren\'t', text)
    text = re.sub('youre', 'you\'re', text)
    text = re.sub('cant', 'can\'t', text)
    text = re.sub('whore', 'who\'re', text)
    text = re.sub('whos', 'who\'s', text)
    text = re.sub('whatre', 'what\'re', text)
    text = re.sub('whats', 'what\'s', text)
    text = re.sub('hadnt', 'hadn\'t', text)
    text = re.sub('didnt', 'didn\'t', text)
    text = re.sub('couldnt', 'couldn\'t', text)
    text = re.sub('theyll', 'they\'ll', text)
    text = re.sub('youd', 'you\'d', text)
    return text

# This function split a huge corpus of text into small chunks or portions
def text_chunking(new_text):
  try:
    max_chunk = 250
    new_text = new_text.replace('.', '.')
    new_text = new_text.replace('?', '?')
    new_text = new_text.replace('!', '!')

    sentences = new_text.split(' ')
    current_chunk = 0
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
          # st.write(current_chunk)
          chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    # st.write("Total chunks of text are: ", len(chunks))
  except:
    chunks = 0
  return chunks

# This function takes in all the chunks, find the summary of each chunk.
def transformers_summary(chunks):
    global all_transformers_summaries
    # Pre-allocate summaries list
    count = 1
    bar = st.progress(0)
    all_transformers_summaries = [{} for i in range(len(chunks))]
    st.write("Summarizing the text. Please wait .......")
    
    for chunk in chunks: 
        try:
            res1 = summarizer(chunk, max_length=150, min_length= 30, do_sample=False)
            count += 1
            bar.progress(count - 1)
        except Exception as e:
            # st.write("Skipped chunk", count, "Error:", e)
            count += 1
            bar.progress(count - 1)
            continue

        # Add summary to list
        if len(all_transformers_summaries) <= count-1:
            all_transformers_summaries.append({})

        all_transformers_summaries[count-1] = res1

        # Summarize chunk
        chunk_sum = res1[0]['summary_text']
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', chunk_sum)
        sentences = [sentence.strip().replace(' .', '.') for sentence in sentences]
        bullet_points = [f"• {sentence}" for sentence in sentences]
        bullet_list = "\n".join(bullet_points)
        bullet_list = re.sub(r'(?<=\S) *\•', '\n•', bullet_list)
        st.code(bullet_list)
        # st.write(bullet_list)

        # count += 1
    st.write("Done Summarizing!!")
    return all_transformers_summaries

def find_summary_transformers(pdf_path):
    # Extract text using Tika
    document_text_part1 = extract_doc_text(pdf_path)
    global chunks
    chunks = text_chunking(document_text_part1)
    if len(chunks) != 1:
        if len(chunks) <= 1000:
            all_transformers_summaries = transformers_summary(chunks)

            joined_summary = ''
            for i in range(len(all_transformers_summaries)):
                try:
                    joined_summary = joined_summary + all_transformers_summaries[i][0]['summary_text']
                except:
                    continue

            txt_to_save = (joined_summary.encode('latin1','ignore')).decode("latin1")  # This ignore the "aphostrope" which is little problematic
            global summary_by_transformers
            summary_by_transformers = prep_b4_save(txt_to_save)
            return summary_by_transformers
        else:
            st.write("Please upload a pdf with less than 500 pages!" )
    else:
        st.write("Document too short to summarize!")

if 'description' not in st.session_state:
    st.session_state['description'] = ''

choice = st.radio(
    "Choose input type",
    ('Text field', 'File upload')
)

if choice == 'Text field':
    description = st.text_area('Have a story? I will summarize it for you. 😊', value=st.session_state['description'])
elif choice == 'File upload':
    uploaded_file = st.file_uploader("**Choose a PDF, Docx or a txt file.**")
# summary_length = st.slider("Select summary length", min_value=30, max_value=150, value=st.session_state['summary_length'])

if st.button('Start Summarization'):
    if uploaded_file is not None or description:
        if uploaded_file is not None:
            file_details = {"Filename":uploaded_file.name, "FileSize":uploaded_file.size}
            if uploaded_file.name.endswith(('.pdf', '.docx', '.txt')):
                st.write(file_details)
                summary = find_summary_transformers(uploaded_file.name)
            else:
                st.write("**Supported documents are PDF, Docx and txt!**")
        if description:
            if len(description.split()) >= 150:
                if len(description.split()) < 50000:
                    summary = transformers_summary(text_chunking(description))
                else:
                    st.write("Your text exceeds the 50,000 words limit. Please shorten your text.")
            else:
                st.write("**Too short to Summarize!**")
