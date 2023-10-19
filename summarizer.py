# Tika setup
from tika import parser
from transformers import pipeline
# Streamlit UI
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

# Set page title and favicon
st.set_page_config(page_title='My Beautiful Streamlit App', page_icon='🌼')

# Set a title for your app
st.title('🌼 My Beautiful Streamlit App 🌼')

# Add a subtitle
st.header('This is a subtitle with an emoji 🚀')

# Add text with markdown
st.markdown('''
This is a **markdown** text block. You can use markdown to format your text.
You can also use emojis in your markdown. For example: 😊👍💻📊🚀
''')

# Summarization code
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
    st.write("Supported documents are PDF, Docx and txt!")

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
    # text = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)

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



# This function takes in all the chunks, find the summary of each chunk and return all the summaries of chunks in list form.
def transformers_summary(chunks):
    st.write("Summarizing the text. Please wait .......")
    global all_transformers_summaries
    # Pre-allocate summaries list
    count = 1
    all_transformers_summaries = [{} for i in range(len(chunks))]
    # Allow user to set summary length
    summary_length = st.slider("Select summary length", min_value=30, max_value=150, value=30)
    for chunk in chunks: #for chunk in tqdm(chunks, desc ="Summarizing your document: ")

        # Summarize chunk
        try:
            res1 = summarizer(chunk, max_length=150, min_length= summary_length, do_sample=False)
        except Exception as e:
            # st.write("Skipped chunk", count, "Error:", e)
            count += 1
            continue

        # Add summary to list
        if len(all_transformers_summaries) <= count-1:
            all_transformers_summaries.append({})

        all_transformers_summaries[count-1] = res1

        # st.write summary
        # Summarize chunk
        chunk_sum = res1[0]['summary_text']
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', chunk_sum)
        sentences = [sentence.strip().replace(' .', '.') for sentence in sentences]
        bullet_points = [f"• {sentence}" for sentence in sentences]
        bullet_list = "\n".join(bullet_points)
        st.write(bullet_list)

        count += 1

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


raw_text = '''
You're about to create your first Streamlit app, or maybe you've found an awesome Streamlit app you want to dive into. In both scenarios, you can't begin building or examine the code without a local development setup.
What if you could do all of this without the need for a local Python environment?
Now, it's all in your browser 🪄
With GitHub Codespaces, you can skip the local environment and enjoy:
Instant setup: Create, fork, and deploy data apps in a single click.
Frictionless editing: Explore and debug source code, with libraries pre-configured.
Develop anywhere: Enjoy the flexibility to build Streamlit apps from any browser.
There are three ways to use Codespaces: creating a new app, editing an existing app, and forking an existing one.
#1: Create a new app
To see it in action, simply log onto Community Cloud and create a new app. (See docs for step-by-step guide.) You can also edit an existing app in your browser.
How to create a new app with Codespaces in one click
#2: Fork an existing app
From any public Streamlit app, click “Fork this app''. Copy the app or explore how it works all within your browser. Then, deploy to Community Cloud to share what you have built!
You can also fork and spin up a Codespace directly from an app's repository. Just select the "Create codespace on master" button.
#3 Edit an existing app
Flexible development is not limited to creating new apps or forking existing ones. Simply select "Edit" in Community Cloud and click the "Create Codespace" button. For a more detailed walkthrough, check out our docs.
Watch Codespaces in action
In this video, @DataProfessor puts it all together! Watch step-by-step how you can use GitHub Codespaces to build Streamlit apps in the browser.
Why Github Codespaces
We wanted to give developers an in-browser editor that is free, powerful, easy and secure.
With GitHub Codespaces, you'll have access to
Ample free tier: Each month, you'll have 60 hours of run time on 2 core Codespaces, plus 15 GB of storage.
A real Linux operating system: develop and deploy on the same system.
Seamless tech stack: use the tools you already love, like Visual Studio Code.
Convenient hosting: Easily host and share your app with Community Cloud.
GitHub's world class security: have the peace of mind that your code and networks are secure.
'''


# Allow user to upload file
uploaded_file = st.file_uploader("Choose a file") 

if uploaded_file is not None:
    file_details = {"Filename":uploaded_file.name, "FileSize":uploaded_file.size}
    st.write(file_details)
    # Summarize 
    summary = find_summary_transformers(uploaded_file.name)
    # Display summary
    st.write(summary)
else:
   st.write("Please upload a file")