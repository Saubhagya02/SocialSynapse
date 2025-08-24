import google.generativeai as genai
genai.configure(api_key="AIzaSyCAiv7EC6ScT3bfoOS_mNd6HNQsPcog_48")
print("Listing models...")
models = genai.list_models()
print("Models found:", models)
for m in models:
    print(m.name)