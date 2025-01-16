from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import argparse
import json
import os


client = OpenAI(
    api_key='add api key'
)

def generate_expression_image(prob, save_path=None):
    if prob <= 0.8:
        expression = "sad"
        bubble_msg = "Hello, it's time to work on your health!"
    else:
        expression = "happy"
        bubble_msg = "Hello, you're perfectly fine!"

    # save bubble msg
    json_path = os.path.join(os.path.dirname(save_path), f'{os.path.basename(save_path)[:-4]}.json') 
    data = {'bubbld_msg': bubble_msg}
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Create an image of a cartoon blood drop character, outlined in black to enhance its clarity. This character should be a light, vibrant red with a glossy finish, featuring large, expressive eyes that reflect a {expression} emotion. The character's posture is intentionally subdued, complementing its {expression} expression and forming a stark contrast to typically energetic poses. It wears simple white sneakers and is presented against a stark white background, drawing attention solely to the character's outlined form and its expressive features. The illustration style is aimed to be sharp and colorful, evoking the essence of classic cartoon animation. Only the character should be in the image.",
        n=1,
        size="1024x1024"
    )
    
    image_url = response.data[0].url
    
    image_content = requests.get(image_url).content
    
    if save_path:
        with open(save_path, 'wb') as f:
            f.write(image_content)
            print(f"Image saved at: {save_path}")
    else:
        image = Image.open(BytesIO(image_content))
        return image

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate image of a cartoon blood drop character with a happy or sad expression')
    parser.add_argument('--prob_path', type=str, help='Probability of the character having a happy expression',required=True)
    parser.add_argument('--save_dir', type=str, help='Path to save the generated image', required=True)
    args = parser.parse_args()

    with open(args.prob_path, 'r') as f:
        prob_dict = json.load(f)
    
    save_dir = args.save_dir

    keys = list(prob_dict.keys())   
    for i in range(len(keys)):
        save_path = os.path.join(save_dir, f"{keys[i][:-4]}_overall_expression.png")
        img_object = generate_expression_image(prob_dict[keys[i]][1], save_path)