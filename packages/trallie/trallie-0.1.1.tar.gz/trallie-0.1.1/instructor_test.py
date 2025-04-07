import instructor
from groq import Groq
from pydantic import BaseModel
import os 

from trallie.prompts.data_extraction_prompts import ZERO_SHOT_EXTRACTION_SYSTEM_PROMPT

os.environ["GROQ_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"

client = instructor.from_groq(Groq())


# Initialize the schema generator with a provider and model
schema_generator = SchemaGenerator(provider="openai", model_name="gpt-4o")
# Feed records to the LLM and discover schema
print("SCHEMA GENERATION IN ACTION ...")
schema = schema_generator.discover_schema(description, records)
print("Inferred schema", schema)

class ExtractUser(BaseModel):
    name: str
    age: int

resp = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_model=ExtractUser,
    messages=[{"role": "user", "content": "Extract Jason is 25 years old."}],
)

print(resp)


