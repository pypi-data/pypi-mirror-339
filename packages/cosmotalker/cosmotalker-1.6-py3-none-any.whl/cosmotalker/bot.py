from deeppavlov import configs, build_model
import os

# Step 1: Load and process ss.txt
def parse_ss_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    # Sample logic: split into entries based on double newlines or "Bot (Topic):"
    entries = content.split("Bot (")
    qa_pairs = []

    for entry in entries[1:]:  # skip anything before first 'Bot ('
        try:
            topic, answer = entry.split("):", 1)
            question = f"Tell me about {topic.strip()}"
            qa_pairs.append({"q": question, "a": answer.strip()})
        except ValueError:
            continue  # in case the split fails

    return qa_pairs

# Step 2: Get Q&A from ss.txt
ss_path = os.path.join(os.path.dirname(__file__), "ss.txt")
faq_data = parse_ss_file(ss_path)

# Step 3: Build the model
faq_bot = build_model(configs.faq.tfidf_logreg_en_faq, download=True)

# Step 4: Fit the model
questions = [item['q'] for item in faq_data]
answers = [item['a'] for item in faq_data]
faq_bot.fit(questions, answers)

# Step 5: Start the chat
print("🔭 AstroBot AI: Ask me about planets, moons, or telescopes.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Bot: Goodbye 🚀")
        break
    response = faq_bot([user_input])
    print(f"\nBot:\n{response[0]}\n")
