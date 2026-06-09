import requests      # replaces ollama
import json
import os
import re
from tools.web_search import web_search
from tools.open_it import open_it

# Making a json file to store the memory of all my conversation sort of a diary

Memory_file = "memory.json"

# Helpful in storing current conversations sort of a RAM

conv = []

# LM Studio server address — runs locally on your Mac

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

# It will check whether any memory exists in json diary

def load_memory():

    if os.path.exists(Memory_file):
        with open(Memory_file, "r") as fin:
            return json.load(fin)
        
    return []

# It will now save the conversation that happens in json as a memory

def save_memory(history):

    with open(Memory_file, "w") as fin:
        json.dump(history, fin, indent=2)

# Preparation for a clean answer we don't want the thinking part of gemma 4 4b

def good_answer(text: str) -> str:

    text = re.sub(r'\*\*.*?\*\*', '', text)                           # remove **bold** text
    text = re.sub(r'Thinking Process:.*', '', text, flags=re.DOTALL)  # remove thinking process
    text = re.sub(r'\d+\.\s+\*\*.*?\*\*.*?\n', '', text)              # remove numbered bold items
    text = re.sub(r'\*\s+.*?\n', '', text)                            # remove bullet points
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)   # remove think tags
    text = text.strip()

    return text

# Making the answer proper so it could speak properly

def final_answer(reasoning: str) -> str:
    patterns = [
        r'(?:Draft the response|Final response|My response|The response|Response)[\s:\-]+(.+?)$',
        r'(?:n\d+\.\s+)(.+?)$',  # last numbered point like \n5. West Bengal is...
    ]

    for pattern in patterns:
        match = re.search(pattern, reasoning, re.IGNORECASE | re.DOTALL)
        if match:
            answer = match.group(1).strip()
            answer = good_answer(answer)
            if answer and len(answer) > 5:
                return answer
            
    lines = [l.strip() for l in reasoning.split('\n') if l.strip()]
    if lines:
        answer = good_answer(lines[-1])
        if answer and len(answer) > 5:
            return answer
 
    return ""

# Detecting which tool will be used

def detect_tool(question: str) -> str:

    # These are the keywords that will activate alice to open the particular app or website

    open_keywords = ["open", "go to", "launch", "show me", "take me to"]
    question_lower = question.lower()
    if any(keyword in question_lower for keyword in open_keywords): 
        site_hints = [
            "youtube", "google", "instagram", "whatsapp", "github",
            "netflix", "spotify", "amazon", "flipkart", "website",
            "twitter", "facebook", "reddit", ".com", "http",
            "discord", "telegram", "zoom", "notes", "calendar",
            "music", "photos", "settings", "vs code", "maps",
            "linkedin", "stackoverflow", "chatgpt", "flipkart"
        ]
        if any(hint in question_lower for hint in site_hints):
            return "open_it"     
        
    try:

        # Sending question to LM Studio instead of Ollama

        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": "google/gemma-4-e4b",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a tool detector for a voice assistant. "
                            "Reply with ONE word only from this list: "
                            "web_search, weather, spotify, gmail, calendar, whatsapp, none. "
                            "Reply web_search for: current news, recent events, today's info, "
                            "latest updates, current prices, sports scores, anything after 2024. "
                            "Reply weather for: weather, temperature, rain, forecast, hot, cold. "
                            "Reply spotify for: play music, pause, skip, next song, volume, what song is playing. "
                            "Reply gmail for: emails, inbox, send mail, read mail. "
                            "Reply calendar for: meetings, schedule, appointments, events, reminder. "
                            "Reply whatsapp for: whatsapp, send message to someone, text someone. "
                            "Reply none for: casual chat, greetings, math, general knowledge, "
                            "writing emails or letters, personal questions, definitions, history. "
                            "ONE word only. No explanation. No punctuation."
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 100,
            },
            timeout = 15
        )

        raw = response.json()
        tool = raw["choices"][0]["message"].get("content", " ").strip().lower()

        # Helpful in removing the full stops and all that get placed by fault

        tool= tool.split()[0] if tool else "none"
        tool = re.sub(r'[^a-z_]', '', tool)

        print(f"[Tool detected: {tool}]")
 
        valid_tools = ["web_search", "weather", "spotify", "gmail", "calendar", "whatsapp"]
        return tool if tool in valid_tools else "none"

    except Exception as e:
        print(f"Tool detection error: {e}")
        return "none"

# Now creating a function to run the tools

def run_tool(tool: str, question: str) -> str:

    if tool == "web_search":
        print("searching the web sir.....")
        return web_search(question)

    if tool == "open_it":
        print("Opening app or the website sir...")
        return open_it(question)
    
    return ""

# Now the main question answer part

def ask_Alice(question: str) -> str:

    global conv

    # It loads the past memory if it is the first message of the conversation

    if len(conv) == 0:
        conv = load_memory()

    tool = detect_tool(question)

    tool_result = ""

    if tool != "none":
        tool_result = run_tool(tool, question)

    if tool == "open_it":
        conv.append({
            "role" : "user", 
            "content": question
        })
        conv.append({
            "role" : "assistant", 
            "content": tool_result
        })
        save_memory(conv)
        return tool_result
    
    if tool_result:
        user_message = (
            f"The user asked: {question}\n"
            f"The relevant information can be found here: {tool_result}"
            f"Answer naturally using this information"
        )
        
    else:
        user_message = question

    conv.append({
        "role" : "user",
        "content" : user_message
    })
    
    # Add your current conversation to the conversation history

    success = False

    try:

        # Sending question to LM Studio instead of Ollama

        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": "google/gemma-4-e4b",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Alice, a personal voice assistant. "
                            "Always call the user 'sir'. "
                            "Never use markdown, asterisks, bullet points, or numbered lists. "
                            "Never show your thinking process. "
                            "Reply naturally like a human. "
                            "RULES FOR LENGTH: "
                            "For casual chat keep replies to 1-2 short sentences. "
                            "If the user asks you to draft, write, generate, or create content "
                            "(emails, letters, essays, code, lists, templates) then provide "
                            "the FULL content directly without any preamble. "
                            "If the user asks you to repeat or show again something you wrote earlier, "
                            "always show the FULL content not just acknowledge it."
                        )
                    }
                ] + conv,
                "temperature": 0.7,
                "max_tokens": 10000,
            },
            timeout=60
        )

        raw = response.json()
        # print(f"DEBUG RAW: {raw}")
        message = raw["choices"][0]["message"]

        answer = message.get("content", "").strip()

        if not answer:
            reasoning = message.get("reasoning_content", "")
            answer = final_answer(reasoning)

        answer = good_answer(answer)

        # Guard for no answer

        if not answer or answer.strip() == "":
            answer = "I am having some connection trouble sir. Please make sure LM Studio server is running."  

        else:
            success = True         

    except Exception as e:
        print(f"LM Studio error: {e}")
        answer = "Sorry sir, I am having trouble connecting. Please make sure LM Studio server is running."

    # Transferring the answers to the conversation history

    conv[-1] = {"role": "user", "content": question}
    conv.append({
        "role": "assistant",
        "content": answer
    })

    # Saving the conversation permanently to Alice's diary

    save_memory(conv)

    return answer

# Creating a functon for clearing Alice's memory

def clear_memory():
    global conv
    conv = []
    if os.path.exists(Memory_file):
        os.remove(Memory_file)
    print("Memory cleared !!!!!!")
