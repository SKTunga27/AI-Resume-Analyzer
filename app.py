from flask import Flask,render_template,request
import pdfplumber
from openai import OpenAI

app=Flask(__name__)
client = OpenAI(api_key="YOUR_API_KEY")

def extract_text(pdf_path):
    text=" "
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text()+"\n"
    return text
@app.route("/",methods=["GET","POST"])
def index():
    report=" "

    if request.method == "POST":
        file = request.files["resume"]

        if file:
            filepath="uploads/"+file.filename
            file.save(filepath)

            resume_text=extract_text(filepath)
            prompt = f"""
            Analyse this resume and provide:
            1.Resume Score out of 100
            2.Strengths
            3.Missing Skills
            4.Improvement Suggestions
            5.Final verdict

            Resume:
            {resume_text}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"user","content":prompt}
                ]
            )

            report=response.choices[0].message.content
        return render_template("index.html",report=report)
    if __name__ == "__main__" :
        app.run(debug=True)
