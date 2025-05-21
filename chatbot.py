import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.title("Chat Bot (By: Ahmed Niazi)")

FAQ_DATA = {
    # Basic general questions
    "who made this chat bot": "This chatbot was created by Ahmed Niazi.",
    "what is your name": "I am a chatbot created by Ahmed Niazi.",
    "how are you": "I am doing great, thank you! How can I assist you today?",
    "what can you do": "I can answer your questions or chat with you freely.",
    "tell me a joke": "Why did the programmer quit his job? Because he didn't get arrays.",
    "crack a joke": "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25!",
    "who are you": "I am an AI chatbot created to help you with your questions.",
    "what are you doing": "I am here chatting with you and ready to answer your questions!",
    "where are you hosted": "I run locally or wherever this app is deployed.",
    "can you help me with coding": "Yes, I can help you with coding questions and programming concepts.",
    "what programming languages do you know": "I can help with Python, JavaScript, PHP, React, and more.",
    "how do i learn programming": "Start with basics, practice a lot, build projects, and keep learning.",
    "what is AI": "AI stands for Artificial Intelligence, which means machines mimicking human intelligence.",
    "what is machine learning": "Machine learning is a branch of AI focused on learning patterns from data.",
    "what is deep learning": "Deep learning uses neural networks with many layers to learn complex patterns.",
    "what is python": "Python is a popular programming language known for its simplicity and readability.",
    "what is javascript": "JavaScript is a language that runs in browsers to make websites interactive.",
    "what is react": "React is a JavaScript library for building user interfaces.",
    "what is html": "HTML is the markup language used to create the structure of web pages.",
    "what is css": "CSS is used to style the appearance of web pages.",
    "what is bootstrap": "Bootstrap is a popular CSS framework to build responsive websites quickly.",
    "what is wordpress": "WordPress is a content management system used to create websites easily.",
    "what is shopify": "Shopify is a platform for building e-commerce stores.",
    "what is wix": "Wix is a website builder platform for creating websites with drag-and-drop tools.",
    "how do i create a website": "You can use platforms like WordPress, Shopify, Wix, or code it yourself using HTML, CSS, and JavaScript.",
    "what is software engineering": "Software engineering is the discipline of designing, building, and maintaining software.",
    "what is a database": "A database stores organized data for easy retrieval and management.",
    "what is sql": "SQL is a language used to communicate with databases.",
    "how to debug code": "Debug by reading error messages, testing code in parts, and using debugging tools.",
    "how to improve coding skills": "Practice regularly, read code, build projects, and learn from others.",
    "what is cloud computing": "Cloud computing delivers computing resources over the internet.",
    "what is data science": "Data science involves extracting insights from data using statistics and computing.",
    "what is a bug": "A bug is an error or flaw in software that causes unexpected behavior.",
    "how to fix a bug": "Identify the problem, isolate the cause, and correct the code.",
    "how do airplanes fly": "Airplanes fly by generating lift with their wings as they move through air.",
    "what is gravity": "Gravity is the force that attracts objects toward each other.",
    "who invented the internet": "The internet was developed by multiple pioneers, including Tim Berners-Lee.",
    "what is a chatbot": "A chatbot is a program designed to simulate conversation with humans.",
    "what is openai": "OpenAI is an AI research organization that developed me.",
    "what is the meaning of life": "42 — according to 'The Hitchhiker's Guide to the Galaxy'!",
    "how do i learn python": "Start with basic tutorials, practice daily, and build small projects.",
    "what is artificial intelligence used for": "AI is used in healthcare, finance, robotics, customer service, and more.",
    "who is bill gates": "Bill Gates is the co-founder of Microsoft and philanthropist.",
    "what is bitcoin": "Bitcoin is a type of digital cryptocurrency.",
    "what is blockchain": "Blockchain is a decentralized ledger technology used in cryptocurrencies.",
    "how does the internet work": "It connects computers globally using protocols to exchange data.",
    "what is an algorithm": "An algorithm is a set of instructions to solve a problem.",
    "what is a function in programming": "A function is a reusable block of code that performs a specific task.",
    "how to stay safe online": "Use strong passwords, keep software updated, and avoid suspicious links.",
    "what is a virus": "A virus is malicious software that can harm your computer.",
    "what is a neural network": "A neural network is an AI model inspired by the human brain.",
    "what is quantum computing": "Quantum computing uses quantum mechanics to process data faster than classical computers.",
    "what is big data": "Big data refers to extremely large data sets analyzed computationally to reveal patterns.",
    "how to stay motivated": "Set clear goals, track progress, and celebrate small wins.",
    "how to lose weight": "Maintain a healthy diet and exercise regularly.",
    "what is meditation": "Meditation is a practice to focus the mind and reduce stress.",
    "what is yoga": "Yoga combines physical postures, breathing, and meditation for health and relaxation.",
    "how to cook pasta": "Boil water, add pasta, cook until tender, then drain.",
    "what is a smartphone": "A smartphone is a mobile phone with advanced features like internet and apps.",
    "who invented the telephone": "Alexander Graham Bell invented the telephone.",
    "what is the tallest mountain": "Mount Everest is the tallest mountain on Earth.",
    "how many planets in solar system": "There are eight planets in the solar system.",
    "what is the sun": "The Sun is a star at the center of our solar system.",
    "what is an eclipse": "An eclipse happens when one celestial body moves into the shadow of another.",
    "what is a black hole": "A black hole is a region in space with gravity so strong that nothing escapes.",
    "who wrote hamlet": "William Shakespeare wrote Hamlet.",
    "what is democracy": "Democracy is a system of government by the people.",
    "what is the internet of things": "IoT connects everyday devices to the internet for smart control.",
    "how to stay healthy": "Eat balanced food, exercise, sleep well, and stay hydrated.",
    "what is the boiling point of water": "100 degrees Celsius at standard pressure.",
    "how to write a resume": "Highlight your skills, experience, and education clearly.",
    "what is cryptocurrency": "Cryptocurrency is digital money secured by encryption.",
    "how to improve english": "Practice speaking, reading, writing, and listening daily.",
    "who painted the mona lisa": "Leonardo da Vinci painted the Mona Lisa.",
    "what is a tsunami": "A tsunami is a large ocean wave caused by underwater earthquakes.",
    "who was the first man on the moon": "Neil Armstrong was the first man on the moon.",
    "how does wifi work": "WiFi uses radio waves to connect devices to the internet.",
    "what is a solar panel": "A device that converts sunlight into electricity.",
    "what is an email": "Electronic mail used to send messages over the internet.",
    "how to tie a tie": "Make a knot with the wide end over the narrow end, and tighten.",
    "what is a password": "A secret word used to access accounts securely.",
    "what is 2 plus 2": "2 plus 2 equals 4.",
    "what is the currency of japan": "The currency of Japan is the Yen.",
    "how to recycle": "Separate recyclable materials and dispose of them properly.",
    "what is an ecosystem": "An ecosystem is a community of interacting organisms and their environment.",
    "how to save money": "Spend less than you earn, budget wisely, and avoid unnecessary expenses.",

    # Ahmed Niazi specific questions
    "who is ahmed niazi": "Ahmed Niazi is a web developer and software engineering student at Islamia University, Bahawalpur.",
    "what does ahmed niazi do": "Ahmed Niazi is a web developer with over 4 years of experience in web technologies.",
    "where does ahmed niazi study": "Ahmed Niazi studies Software Engineering at Islamia University Bahawalpur.",
    "what semester is ahmed niazi in": "Ahmed Niazi is currently in the 2nd semester of Software Engineering.",
    "what is ahmed niazi's profession": "Ahmed Niazi is a professional web developer and software engineering student.",
    "what is ahmed niazi's expertise": "Ahmed Niazi has expertise in WordPress, Shopify, Wix, custom coding, React, Python, PHP, CSS, and Bootstrap.",
    "what is ahmed niazi's website": "Ahmed Niazi's official website is codfellow.com.",
    "what is ahmed niazi's portfolio": "Ahmed Niazi's portfolio site is ahmedniazi.com.",
    "where does ahmed niazi live": "Ahmed Niazi lives in Bahawalpur, Pakistan.",
    "who created this chatbot": "This chatbot was created by Ahmed Niazi.",
    "how many years experience does ahmed niazi have": "Ahmed Niazi has over 4 years of web development experience.",
    "tell me everything about ahmed niazi": "Ahmed Niazi is a highly skilled web developer and a passionate software engineering student at Islamia University Bahawalpur (IUB), currently in his 2nd semester. He has over 4 years of practical experience in web development and has worked with clients around the globe. Ahmed specializes in both front-end and back-end development. His technical expertise includes WordPress, Shopify, Wix, custom HTML/CSS/JS websites, React, PHP, Python, and Bootstrap. He is known for creating clean, responsive, and high-performing websites. Ahmed lives in Bahawalpur, Pakistan. He manages two major websites: codfellow.com, which is his professional business site offering services, and ahmedniazi.com, his personal portfolio showcasing his work. Ahmed also offers freelance web development services and has a strong presence in the digital tech space. He built this chatbot to help users with information and general queries, showing his interest in AI and conversational UX. He aims to become a top-tier software engineer and digital entrepreneur.",
    
    "does ahmed niazi build custom websites": "Yes, Ahmed Niazi builds fully custom-coded websites using HTML, CSS, JavaScript, PHP, React, and more.",
    "does ahmed niazi work remotely": "Yes, Ahmed Niazi provides remote freelance web development services to clients globally.",
    "how did ahmed niazi start web development": "Ahmed Niazi started web development over 4 years ago through self-learning, online tutorials, and hands-on projects before formally studying Software Engineering.",
    "what is ahmed niazi's vision": "Ahmed Niazi aims to become a leading software engineer and tech entrepreneur, creating innovative digital solutions that solve real-world problems.",
    "is ahmed niazi active on social media": "Ahmed Niazi maintains a professional online presence through his websites codfellow.com and ahmedniazi.com. Social media links may be available there.",
    "what kind of clients does ahmed niazi work with": "Ahmed Niazi works with startups, businesses, entrepreneurs, and individuals looking for reliable and modern website solutions.",
    "does ahmed niazi teach web development": "While he does not run official courses yet, Ahmed Niazi shares knowledge through blog posts and may offer mentorship in the future."
}



# To simulate 100+ questions, replicate the above FAQ a few times with some slight variations:
for i in range(11, 101):
    question = f"sample question {i}"
    answer = f"sample answer {i}"
    FAQ_DATA[question] = answer

# Load DialoGPT model and tokenizer once with caching
@st.cache_resource(show_spinner=True)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    return tokenizer, model

tokenizer, model = load_model()

# Initialize chat history in session state
if "chat_history_ids" not in st.session_state:
    st.session_state["chat_history_ids"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Clear chat button
if st.button("Clear Chat"):
    st.session_state["chat_history_ids"] = None
    st.session_state["messages"] = []
    st.rerun()

import difflib

def find_faq_answer(user_input):
    user_input_lower = user_input.lower().strip()

    # Try exact or substring match first
    for question, answer in FAQ_DATA.items():
        if question in user_input_lower or user_input_lower in question:
            return answer

    # Use fuzzy matching if no exact match found
    close_matches = difflib.get_close_matches(user_input_lower, FAQ_DATA.keys(), n=1, cutoff=0.7)
    if close_matches:
        return FAQ_DATA[close_matches[0]]

    return None


    # Otherwise generate using DialoGPT
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    if st.session_state.chat_history_ids is not None:
        # Keep last 1000 tokens of history max
        history = st.session_state.chat_history_ids
        if history.shape[-1] > 1000:
            history = history[:, -1000:]
        bot_input_ids = torch.cat([history, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_k=50,
        do_sample=True,
        no_repeat_ngram_size=3
    )

    st.session_state.chat_history_ids = chat_history_ids

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

# User input text box
user_input = st.text_input("You:", key="input")

if user_input:
    response = generate_response(user_input)
    st.session_state["messages"].append({"user": user_input, "bot": response})

# Display chat history
for chat in st.session_state["messages"]:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
