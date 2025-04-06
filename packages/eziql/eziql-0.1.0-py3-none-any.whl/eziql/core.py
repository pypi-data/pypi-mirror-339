from groq import Groq
from typing import Optional
import os 
from dotenv import load_dotenv
load_dotenv()


class GrokSQL:
    """
        A class to generate SQL queries from natural language using Groq's LLaMA model.
    
        You must either:
        1. Create a `.env` file in your project root and define the API key as:
            eziql_key=your_groq_api_key
        OR
        2. Pass the API key directly when initializing the class:
            grok = GrokSQL(api_key="your_groq_api_key")
    
        Args:
            api_key (Optional[str]): Groq API key. If not provided, will try to load from environment variable 'eziql_key'.
    
        Raises:
            ValueError: If no API key is provided via argument or environment variable.
    """
    def __init__(self, api_key:Optional[str] = None):
        
        self.api_key = api_key or os.getenv('eziql_key')
        if not self.api_key:
            raise ValueError("API key must be provided or set in the environment as 'eziql_key'.")
        
    def generate_sql(self, user_query:str, table_schema : Optional[str] = None)-> str:
        """
            This method sends a prompt to the Groq API asking it to convert a natural language
            query into a syntactically correct SQL statement. You can optionally provide the
            table schema to improve query accuracy.

            Args:
                user_query (str): A plain English query that describes what you want in SQL.
                table_schema (Optional[str]): An optional string containing table structure or column info 
                                              to help the model generate better SQL queries.

            Returns:
                str: A cleaned SQL query as a string with no explanations, formatted in a single line.

            Raises:
                RuntimeError: If the Groq API request fails or any unexpected error occurs during processing.
    """
        try:
            client = Groq()
            prompt = f"Generate an SQL query only (without explanation) and return string contains only query for: {user_query} "

            if table_schema:
                prompt += f"\nTable Schema: {table_schema}"

            completion = client.chat.completions.create(
                    model = "llama-3.3-70b-versatile",
                    messages = [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0,
                    top_p=0.9,
                    stream=False,
                    stop=None,
            )


            return completion.choices[0].message.content.removeprefix('```sql').removesuffix('```').replace('\n',' ').strip()
        except Exception as e:
            raise RuntimeError(f"Error generating SQL query: {e}")
