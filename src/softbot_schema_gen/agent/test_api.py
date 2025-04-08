from call_generate_schema_api import call_generate_schema_api

if __name__ == "__main__":
    instruction = "Design a soft robot that can crawl like a worm in its simplest form"
    schema = call_generate_schema_api(instruction)
    print("Generated schema:")
    print(schema)