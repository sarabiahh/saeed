from flask_cors import CORS


from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)
CORS(app)
  #Enable CORS for all routes
import os
openai.api_key = "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"

@app.route("/")
def home():
    return render_template('Home.html')

@app.route("/prompt")
def prompt():
    return render_template('prompt.html')

@app.route("/book")
def book():
    return render_template('book.html')

@app.route('/generateStory', methods=['POST'])
def generate_story():
    
        data = request.get_json()  #Extract JSON from the request

        user_input = data['text']
        user_age = data['age']
        Explanation = "'أريد أن تبدأ الحوارات في القصة باسم القائل، ثم الكلام، مثل: قال علي 'مرحبًا! كيف حالك؟"    
        
        ageImpact = ""
        if user_age == "1-3":
            ageImpact = "أكتب قصة قصيرة للأطفال من عمر 1 إلى 3 سنوات، تحتوي على 120-150 كلمة. يجب أن تكون القصة بسيطة جدًا، مترابطة، ومتسلسلة بشكل طبيعي. ركز على حدث واحد رئيسي فقط يمكن للأطفال فهمه بسهولة. تجنب التفاصيل الكثيرة أو التعقيد. اجعل اللغة سهلة ومباشرة، واستخدم مصطلحات يسهل على الأطفال فهمها، مع نهاية واضحة وسعيدة. اكتب العنوان مباشرةً ثم نص القصة دون إضافات مثل (عنوان القصة:) أو (العنوان:). يجب أن تكون القصة باللغة العربية الفصحى، صحيحة لغويًا ونحويًا وإملائيًا، ومناسبة لسردها للأطفال."
        elif user_age == "4-6":
            ageImpact = "أكتب قصة قصيرة للأطفال من عمر 4 إلى 6 سنوات، تحتوي على 200-250 كلمة يجب ان تكون القصة تميز بين الخير والشر، والخير ينتصر دائمًا يجب أن تكون القصة مترابطة، ومتسلسلة بشكل طبيعي، اجعل اللغة سهلة ومباشرة، واستخدم مصطلحات يسهل على الأطفال فهمها، مع نهاية واضحة وسعيدة. اكتب العنوان مباشرةً ثم نص القصة دون إضافات مثل (عنوان القصة:) أو (العنوان:). يجب أن تكون القصة باللغة العربية الفصحى، صحيحة لغويًا ونحويًا وإملائيًا، ومناسبة لسردها للأطفال."
        elif user_age == "7-10":
            ageImpact = "أكتب قصة قصيرة للأطفال من عمر 7 إلى 10 سنوات، تحتوي على 300-350 كلمة ، يجب أن تكون القصة مترابطة، ومتسلسلة بشكل طبيعي، اجعل اللغة سهلة ومباشرة، واستخدم مصطلحات يسهل على الأطفال فهمها، مع نهاية واضحة وسعيدة. اكتب العنوان مباشرةً ثم نص القصة دون إضافات مثل (عنوان القصة:) أو (العنوان:). يجب أن تكون القصة باللغة العربية الفصحى، صحيحة لغويًا ونحويًا وإملائيًا، ومناسبة لسردها للأطفال."

        reformatted_input = f" {ageImpact}.{Explanation}.{user_input}"



        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت مساعد متخصص في كتابة قصص ممتعة ومفيدة للأطفال و يجب أن تكون القصة باللغة العربية الفصحى، صحيحة لغويًا ونحويًا وإملائيًا."},
                {"role": "user", "content": reformatted_input}
            ]
        )

        story_content = response['choices'][0]['message']['content']  #Extract story content
        return jsonify({"story": story_content})  #Send it as JSON


@app.route('/generateImageFromStory', methods=['POST'])
def generate_image_from_story():
    data = request.get_json()  #Extract JSON from the request

    story_content = data['story']  #Original story
    max_length = 150  #Max length for summarization
    
    #Step 1: Translate the story to English
    story_translated = translate_to_english(story_content)
    
    #Step 2: Summarize the story
    story_summarized = summarize_text(story_translated, max_length=max_length)
    
    #Step 3: Generate Image based on the summarized story
    prompt = (
        f"illustrate an anime-style image representing the following story with FOUR panels, visually representing the key events of the story. "
        f"The image should capture the key events of the story with expressive characters, vibrant settings, and detailed visuals.  "
        f"Ensure the art style is warm, friendly, and suitable for young children. " 
        f"Ensure the style is playful and suitable for children, resembling classic illustrated storybooks. "
        f"DO NOT INCLUDE ANY TEXT, SPEECH BUBBLES, WORDS, EXPRESSIONS OR CAPTIONS. USE PURELY VISUAL STORYTELLING TO DEPICT THE EVENTS OF THE STORY. "
        f"Story: {story_summarized}"
    )
    
    image_urls = generate_image(prompt)
    if not image_urls:
        print("No image URLs generated")

    #Return the generated image URLs as JSON
    return jsonify({
        "image_urls": image_urls
    })



#Function to translate text to English
def translate_to_english(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a translator who translates Arabic text to English."},
                {"role": "user", "content": f"Translate the following text to English: {text}"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return text  #Return original text in case of error

#Function to summarize text
def summarize_text(text, max_length=150):
    if len(text) <= max_length:
        return text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following story to ensure it is no more than {max_length} characters: {text}"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return text  #Return original text in case of error

#Function to generate image based on prompt
def generate_image(prompt, n=1, size="1024x1024"):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=n,
            size=size
        )
        return [img["url"] for img in response["data"]]
    except Exception as e:
        print(f"\n An error occurred in generate_image: {e}")
        return []



if __name__ == "__main__":
    app.run(debug=True, port=8000)

