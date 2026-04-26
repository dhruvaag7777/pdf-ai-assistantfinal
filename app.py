import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

nltk.download('punkt')

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

def summarize_text(text, n=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    freq = Counter(words)

    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[word]

    summary = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]
    return summary

def answer_question(text, question):
    sentences = sent_tokenize(text)
    for sent in sentences:
        if any(word.lower() in sent.lower() for word in question.split()):
            return sent
    return "Answer not found in document."

def main():
    pdf_path = "sample.pdf"

    text = extract_text(pdf_path)

    if not text.strip():
        print("No text found in PDF. Try another PDF.")
        return

    print("\nPDF Loaded Successfully")

    while True:
        print("\nChoose option:")
        print("1. Ask Question")
        print("2. Generate Summary")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            q = input("Ask your question: ")
            ans = answer_question(text, q)
            print("\nAnswer:", ans)

        elif choice == "2":
            summary = summarize_text(text)
            print("\nSummary:")
            for s in summary:
                print("-", s)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()