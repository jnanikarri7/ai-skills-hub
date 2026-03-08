import os
from PyPDF2 import PdfReader
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.interview import InterviewQ

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def parse_questions(text: str) -> list[dict]:
    import re
    questions = []
    lines = text.split('\n')
    current_q = None
    current_answer = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+\.', line):  # Starts with number.
            if current_q:
                current_q['answer_html'] = '<br>'.join(current_answer)
                questions.append(current_q)
            question_text = re.sub(r'^\d+\.\s*', '', line)
            current_q = {'question': question_text, 'difficulty': 'medium', 'answer_html': '', 'code': None}
            current_answer = []
        elif current_q and line:
            current_answer.append(line)
    if current_q:
        current_q['answer_html'] = '<br>'.join(current_answer)
        questions.append(current_q)
    return questions

def load_questions():
    source_dir = 'source_files'
    db: Session = SessionLocal()
    try:
        order_index = 0
        for filename in os.listdir(source_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(source_dir, filename)
                text = extract_text_from_pdf(pdf_path)
                print(f"Extracted text from {filename}:\n{text[:500]}...")  # Print first 500 chars
                questions = parse_questions(text)
                print(f"Parsed {len(questions)} questions from {filename}")
                for q_data in questions:
                    q = InterviewQ(
                        difficulty=q_data.get('difficulty', 'medium'),
                        question=q_data['question'],
                        answer_html=q_data['answer_html'],
                        code=q_data.get('code'),
                        order_index=order_index
                    )
                    db.add(q)
                    order_index += 1
        db.commit()
        print(f"Loaded {order_index} questions.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_questions()