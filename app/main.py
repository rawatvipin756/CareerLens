# import os
# import time
# from pathlib import Path
# from dotenv import load_dotenv
# from groq import Groq
# from pydantic import BaseModel,Field

# load_dotenv()
# my_api_key=os.getenv("GROQ_API_KEY")

# if not my_api_key:
#   raise ValueError("Api key not found")

# client=Groq(api_key=my_api_key)
# model="openai/gpt-oss-120b"

# job_description='''
#   Description:
#   Do you want to solve real customer problems through innovative technology? Do you enjoy working on scalable services in a collaborative team environment? Do you want to see your code directly impact millions of customers worldwide?

#   At Amazon, we hire the best minds in technology to innovate and build on behalf of our customers. Customer obsession is part of our company DNA, which has made us one of the world's most beloved brands.

#   Our Software Development Engineers (SDEs) use modern technology to solve complex problems while seeing their work's impact first-hand. The challenges SDEs solve at Amazon are meaningful and influence millions of customers, sellers, and products globally. We seek individuals passionate about creating new products, features, and services while managing ambiguity in an environment where development cycles are measured in weeks, not years.

#   At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the entire lifecycle of your code - from design through deployment and ongoing operations. This ownership mindset, combined with our commitment to operational excellence, ensures we deliver the highest quality solutions for our customers.

#   We're looking for curious minds who think big and want to define tomorrow's technology. At Amazon, you'll grow into the high-impact engineer you know you can be, supported by a culture of learning and mentorship. Every day brings exciting new challenges and opportunities for personal growth.
  
#   Key job responsibilities:
#   • Collaborate and communicate effectively with experienced cross-disciplinary Amazonians to design, build, and operate innovative products and services that delight our customers, while participating in technical discussions to drive solutions forward.
#   • Design and develop scalable solutions using cloud-native architectures and microservices in a large distributed computing environment.
#   • Participate in code reviews and contribute to technical documentation.
#   • Build and maintain resilient distributed systems that are scalable, fault-tolerant, and cost-effective.
#   • Leverage and contribute to the development of GenAI and AI-powered tools to enhance development productivity while staying current with emerging technologies.
#   • Write clean, maintainable code following best practices and design patterns.
#   • Work in an agile environment practicing CI/CD principles while participating in operational responsibilities including on-call duties.
#   • Demonstrate operational excellence through monitoring, troubleshooting, and resolving production issues.
  
#   Basic Qualifications:
#   - Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript
#   - Experience with data structure implementation, basic algorithm development, and/or object-oriented design principles
#   - Currently has, or is in the process of obtaining a bachelor’s degree in Computer Science, Computer Engineering, Data Science, Information Systems, or related STEM fields
#   - Must be 18 years of age of older.

#   Preferred Qualifications:
#   - Experience from previous technical internship(s) or demonstrated project experience
#   - Experience with one or more of the following: AI tools for development productivity, Cloud platforms (preferably AWS), Database systems (SQL and NoSQL), Contributing to open-source projects, Version control systems, Debugging and troubleshooting complex systems
#   - Demonstrated ability to learn and adapt to new technologies quickly
#   - Basic understanding of software development lifecycle (SDLC)
#   - Strong problem-solving and analytical skills
#   - Excellent written and verbal communication skills
# '''

# class job_desc(BaseModel):
#   company_name:str | None=None
#   job_title:str | None=None
#   required_skills:list[str]=Field(default_factory=list)
#   preferred_skills:list[str]=Field(default_factory=list)
#   responsiblities:list[str]=Field(default_factory=list)
#   qualifications:list[str]=Field(default_factory=list)
#   minimum_experience:str | None=None
#   education:list[str]=Field(default_factory=list)

# jobd_schema=job_desc.model_json_schema()

# system_prompt=f'''
#   You are an expert HR assistant.

#   Your job is to analyze job descriptions and extract
#   structured information from them.

#   Return ONLY valid JSON matching this schema:
#   {jobd_schema}

#   IMPORTANT:
#   Do NOT return the schema itself.
#   Do NOT return fields like "properties", "title" or "type".
#   Fill the schema with actual information extracted from the job description.

#   If minimum experience is not mentioned, return null.
#   If information for a list is missing, return an empty list.
#   Do not invent information.
# '''

# user_prompt=f'''
#   Analyze the following job description
#   {job_description}
# '''

# message_system={
#   "role":"system",
#   "content":system_prompt
# }

# message_user={
#   "role":"user",
#   "content":user_prompt
# }

# response_format={
#   "type":"json_object"
# }

# messages=[message_system,message_user]

# response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)

# answer=response.choices[0].message.content
# raw_json=answer

# import json
# job_data=json.loads(raw_json)
# job=job_desc(**job_data)
# print(job.minimum_experience)
# print(job.education)

# class MatchResult(BaseModel):
#   score:float
#   details:dict

# class Experience(BaseModel):
#   company:str | None=None
#   role:str | None=None
#   duration:str | None=None
#   description:str | None=None
#   skills_used:list[str]=[]

# class Resume(BaseModel):
#   name: str | None = None
#   email: str | None = None
#   phone: str | None = None
#   location: str | None = None
#   education: list[str] = Field(default_factory=list)
#   skills: list[str] = Field(default_factory=list)
#   experience: list[str] = Field(default_factory=list)
#   projects: list[str] = Field(default_factory=list)
#   certifications: list[str] = Field(default_factory=list)

# resume_schema=Resume.model_json_schema()

# def final_score(job,resume):
#   match_schema=MatchResult.model_json_schema()

#   prompt = f'''
#     You are an HR recruiter.
#     Compare the candidate's resume with the job description.

#     {match_schema}

#     Give me:
#     1. Candidate name
#     2. Matching skills
#     3. Missing important skills
#     4. Whether experience requirement is met
#     5. Overall match percentage from 0 to 100
#     6. A short final verdict

#     Keep the response concise and easy to read.
#   '''

#   message={
#     "role":"user",
#     "content":prompt
#   }
#   messages=[message]

#   response_format={
#     "type":"json_object"
#   }

#   response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
  
#   result=json.loads(response.choices[0].message.content)
#   return MatchResult(**result)

# def parse_resume(resume_text):
#   system_prompt=f'''
#     You are an expert resume parser.
#     Extract information from the resume based on its meaning,
#     not only based on exact section headings.

#     Different resumes may use different headings.
#     For example:
#     - Experience
#     - Professional Experience
#     - Work History
#     - Employment
#     - Internships
#     These may all contain relevant experience.

#     Skills may also appear in the skills section, work experience,
#     internships or projects.
#     Return ONLY valid JSON matching this schema:
#     {resume_schema}

#     Important rules:
#     1. Do not invent information.
#     2. If a value is not available, return null.
#     3. If a list has no information, return an empty list.
#     4. Include internships inside experiences.
#     5. Extract skills mentioned across the entire resume.
#   '''

#   user_prompt=f'''
#     Parse the following resume:
#     {resume_text}
#   '''

#   message_system={
#     "role":"system",
#     "content":system_prompt
#   }
#   message_user={
#     "role":"user",
#     "content":user_prompt
#   }
#   messages=[message_system,message_user]

#   response_format={
#     "type":"json_object"
#   }

#   response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
#   raw_output=response.choices[0].message.content
#   data=json.loads(raw_output)
#   resume=Resume(**data)
#   return resume

# from pypdf import PdfReader
# from docx import Document

# def read_pdf(file_path):
#   reader=PdfReader(file_path)
#   text=""
#   for page in reader.pages:
#     page_text=page.extract_text()
#     if page_text:
#       text+=page_text + "\n"
#   return text

# def read_docx(file_path):
#   document=Document(file_path)
#   text=""
#   for paragraph in document.paragraphs:
#     if paragraph.text.strip():
#       text+=paragraph.text + "\n"
#   for table in document.tables:
#     for row in table.rows:
#       for cell in row.cells:
#         if cell.text.strip():
#           text+=cell.text + "\n"
#   return text

# def read_resume(file_path):
#   if file_path.suffix.lower()==".pdf":
#     return read_pdf(file_path)
#   elif file_path.suffix.lower()==".docx":
#     return read_docx(file_path)
#   else:
#     return None

# resume_folder=Path("resumes")
# all_results=[]
# for file_path in resume_folder.iterdir():
#   if file_path.suffix.lower() not in [".pdf", ".docx"]:
#     continue

#   print("\n Processing",file_path.name)
#   resume_text=read_resume(file_path)
#   parsed_resume=parse_resume(resume_text)
#   time.sleep(5)
#   result=final_score(job,parsed_resume)
#   time.sleep(5)
#   print("Score:",result.score)
#   all_results.append({
#     "name":parsed_resume.name,
#     "score":result.score,
#     "details":result.details
#   })
# all_results.sort(
#   key=lambda candidate:candidate["score"],
#   reverse=True
# )
# top_2 = all_results[:2]
# worst_2 = all_results[-2:]

# print("TOP 2 candidate")
# for candidate in top_2:
#   print(
#     candidate["name"],"-",
#     candidate["score"],"%"
#   )
#   print(candidate["details"])

# print("LOWEST 2 candidate")
# for candidate in worst_2:
#   print(
#     candidate["name"],
#     "-",
#     candidate["score"],
#     "%"
#   )
#   print(candidate["details"])



import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

from pypdf import PdfReader
from docx import Document


# =====================================
# 1. ENVIRONMENT AND GROQ CONFIGURATION
# =====================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-120b"


# =====================================
# 2. JOB DESCRIPTION
# =====================================

# Keep your existing job_description string here.
# Paste your complete Amazon job description.

job_description='''
  Description:
  Do you want to solve real customer problems through innovative technology? Do you enjoy working on scalable services in a collaborative team environment? Do you want to see your code directly impact millions of customers worldwide?

  At Amazon, we hire the best minds in technology to innovate and build on behalf of our customers. Customer obsession is part of our company DNA, which has made us one of the world's most beloved brands.

  Our Software Development Engineers (SDEs) use modern technology to solve complex problems while seeing their work's impact first-hand. The challenges SDEs solve at Amazon are meaningful and influence millions of customers, sellers, and products globally. We seek individuals passionate about creating new products, features, and services while managing ambiguity in an environment where development cycles are measured in weeks, not years.

  At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the entire lifecycle of your code - from design through deployment and ongoing operations. This ownership mindset, combined with our commitment to operational excellence, ensures we deliver the highest quality solutions for our customers.

  We're looking for curious minds who think big and want to define tomorrow's technology. At Amazon, you'll grow into the high-impact engineer you know you can be, supported by a culture of learning and mentorship. Every day brings exciting new challenges and opportunities for personal growth.
  
  Key job responsibilities:
  • Collaborate and communicate effectively with experienced cross-disciplinary Amazonians to design, build, and operate innovative products and services that delight our customers, while participating in technical discussions to drive solutions forward.
  • Design and develop scalable solutions using cloud-native architectures and microservices in a large distributed computing environment.
  • Participate in code reviews and contribute to technical documentation.
  • Build and maintain resilient distributed systems that are scalable, fault-tolerant, and cost-effective.
  • Leverage and contribute to the development of GenAI and AI-powered tools to enhance development productivity while staying current with emerging technologies.
  • Write clean, maintainable code following best practices and design patterns.
  • Work in an agile environment practicing CI/CD principles while participating in operational responsibilities including on-call duties.
  • Demonstrate operational excellence through monitoring, troubleshooting, and resolving production issues.
  
  Basic Qualifications:
  - Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript
  - Experience with data structure implementation, basic algorithm development, and/or object-oriented design principles
  - Currently has, or is in the process of obtaining a bachelor’s degree in Computer Science, Computer Engineering, Data Science, Information Systems, or related STEM fields
  - Must be 18 years of age of older.

  Preferred Qualifications:
  - Experience from previous technical internship(s) or demonstrated project experience
  - Experience with one or more of the following: AI tools for development productivity, Cloud platforms (preferably AWS), Database systems (SQL and NoSQL), Contributing to open-source projects, Version control systems, Debugging and troubleshooting complex systems
  - Demonstrated ability to learn and adapt to new technologies quickly
  - Basic understanding of software development lifecycle (SDLC)
  - Strong problem-solving and analytical skills
  - Excellent written and verbal communication skills
'''

# =====================================
# 3. PYDANTIC MODELS
# =====================================

class JobDescription(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    qualifications: list[str] = Field(default_factory=list)
    minimum_experience: str | None = None
    education: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    score: float = Field(ge=0, le=100)
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    experience_met: bool | None = None
    details: str
    verdict: str


# =====================================
# 4. GENERIC LLM JSON HELPER
# =====================================

def call_llm_json(system_prompt, user_prompt):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    raw_output = response.choices[0].message.content

    if not raw_output:
        raise ValueError("LLM returned an empty response")

    return json.loads(raw_output)


# =====================================
# 5. EXTRACT JOB DESCRIPTION
# =====================================

def extract_job_description(job_description):

    schema = JobDescription.model_json_schema()

    system_prompt = f"""
    You are an expert HR assistant.

    Extract structured information from the job description.

    Return only valid JSON matching this schema:

    {json.dumps(schema)}

    Rules:
    1. Do not invent information.
    2. If information is missing, use null.
    3. If a list has no information, return an empty list.
    4. Extract required and preferred skills separately.
    """

    data = call_llm_json(
        system_prompt,
        job_description
    )

    return JobDescription.model_validate(data)


# =====================================
# 6. PARSE RESUME USING LLM
# =====================================

def parse_resume(resume_text):

    schema = Resume.model_json_schema()

    system_prompt = f"""
    You are an expert resume parser.

    Extract candidate information from the resume.

    Return only valid JSON matching this schema:

    {json.dumps(schema)}

    Rules:
    1. Never invent information.
    2. Missing strings should be null.
    3. Missing lists should be empty lists.
    4. Include internships in experience.
    5. Extract skills from the entire resume.
    6. Represent experience as structured objects.
    7. Preserve the candidate's actual information.
    """

    data = call_llm_json(
        system_prompt,
        resume_text
    )

    return Resume.model_validate(data)


# =====================================
# 7. FINAL RESUME MATCHING
# =====================================

def final_score(job, resume):

    match_schema = MatchResult.model_json_schema()

    system_prompt = f"""
    You are an expert technical recruiter.

    Compare a candidate's resume with a job description.

    Return only valid JSON matching this schema:

    {json.dumps(match_schema)}

    Evaluation rules:

    1. Compare required skills with candidate skills.
    2. Identify matching skills.
    3. Identify important missing skills.
    4. Evaluate experience requirements.
    5. Consider education and projects.
    6. Do not assume missing information is present.
    7. Give a fair score between 0 and 100.
    8. Explain the score briefly.
    9. Do not reward a candidate for skills they do not demonstrate.
    10. Return a concise final verdict.

    The score must reflect evidence in the resume,
    not assumptions about the candidate.
    """

    user_prompt = f"""
    JOB DESCRIPTION:

    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:

    {resume.model_dump_json(indent=2)}

    Analyze the candidate against this job.
    """

    data = call_llm_json(
        system_prompt,
        user_prompt
    )

    return MatchResult.model_validate(data)


# =====================================
# 8. PDF EXTRACTION
# =====================================

def read_pdf(file_path):

    reader = PdfReader(str(file_path))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


# =====================================
# 9. DOCX EXTRACTION
# =====================================

def read_docx(file_path):

    document = Document(str(file_path))

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text += paragraph.text + "\n"

    for table in document.tables:

        for row in table.rows:

            for cell in row.cells:

                if cell.text.strip():
                    text += cell.text + "\n"

    return text.strip()


# =====================================
# 10. READ RESUME
# =====================================

def read_resume(file_path):

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf(file_path)

    elif suffix == ".docx":
        return read_docx(file_path)

    else:
        raise ValueError("Unsupported resume format")


# =====================================
# 11. MAIN APPLICATION
# =====================================

def main():

    resume_folder = Path(__file__).parent / "resumes"

    if not resume_folder.exists():
        raise FileNotFoundError(
            f"Resume folder not found: {resume_folder}"
        )

    resume_files = [
        file for file in resume_folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in [".pdf", ".docx"]
    ]

    if not resume_files:
        print("No PDF or DOCX resumes found.")
        return

    # Extract job description

    print("\nExtracting job description...")

    job = extract_job_description(job_description)

    print("\nJob:", job.job_title)
    print("Company:", job.company_name)
    print("Required skills:", job.required_skills)

    all_results = []

    # Process candidates

    for file_path in resume_files:

        print("\nProcessing:", file_path.name)

        try:

            resume_text = read_resume(file_path)

            if not resume_text:
                print("Skipping: No readable text found.")
                continue

            parsed_resume = parse_resume(resume_text)

            time.sleep(2)

            result = final_score(job, parsed_resume)

            print("Candidate:", parsed_resume.name)
            print("Score:", result.score)

            all_results.append({
                "name": parsed_resume.name,
                "score": result.score,
                "matching_skills": result.matching_skills,
                "missing_skills": result.missing_skills,
                "experience_met": result.experience_met,
                "details": result.details,
                "verdict": result.verdict
            })

            time.sleep(2)

        except Exception as error:

            print(
                f"Error processing {file_path.name}: {error}"
            )

    # =====================================
    # 12. RANK CANDIDATES
    # =====================================

    if not all_results:
        print("\nNo candidates were successfully processed.")
        return

    all_results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    print("\n========== ALL CANDIDATES ==========")

    for candidate in all_results:

        print(
            candidate["name"],
            "-",
            candidate["score"],
            "%"
        )

    # Top 2

    top_2 = all_results[:2]

    # Lowest 2 without overlapping top 2

    worst_2 = (
        all_results[2:][-2:]
        if len(all_results) > 2
        else []
    )

    print("\n========== TOP CANDIDATES ==========")

    for candidate in top_2:

        print("\nName:", candidate["name"])
        print("Score:", candidate["score"])
        print("Matching:", candidate["matching_skills"])
        print("Missing:", candidate["missing_skills"])
        print("Experience met:", candidate["experience_met"])
        print("Details:", candidate["details"])
        print("Verdict:", candidate["verdict"])

    print("\n========== LOWEST CANDIDATES ==========")

    for candidate in worst_2:

        print("\nName:", candidate["name"])
        print("Score:", candidate["score"])
        print("Verdict:", candidate["verdict"])


if __name__ == "__main__":
    main()
