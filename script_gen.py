import json
import math
from llm_client import generate_text

def generate_script(idea: str, tone: str, style: str, duration_seconds: int) -> dict:
    """
    Generates a high-retention script for a YouTube Short/Reel using Time-Based Prompting.
    """
    target_words = int(duration_seconds * 2.5)
    
    prompt = f"""
    You are an expert Content Creator for YouTube Shorts and TikTok.
    Your goal is to create a script that maximizes audience retention.

    VIDEO PARAMETERS:
    - Idea: "{idea}"
    - Tone: {tone}
    - Visual Style: {style}
    - Target Duration: {duration_seconds} seconds (~{target_words} words total)

    STRUCTURE REQUIREMENTS:
    1. Write one continuous, flowing narration script.
    2. Divide this script into logical visual scenes (approx 3-5 seconds per scene, or based on natural pauses).

    OUTPUT FORMAT:
    Return strictly valid JSON with this structure:
    {{
        "meta": {{
            "title": "Viral Video Title",
            "description": "SEO optimized description",
            "full_narration": "THE ENTIRE SCRIPT TEXT IN ONE CONTINUOUS STRING",
            "bgm_mood": "Pick ONE exactly from: funny, happy, inspirational, sad"
        }},
        "scenes": [
            {{
                "segment_text": "The specific spoken text for this visual segment.",
                "visual_prompt": "Highly detailed, cinematic prompt for AI image generator in style: {style}"
            }}
        ]
    }}
    - Output ONLY the raw JSON string.
    - DO NOT use markdown blocks like ```json.
    - DO NOT include any introductory or concluding text.
    - Ensure 'full_narration' exactly matches the combined 'segment_text' of all scenes.
    """

    print(f"Generating time-based script for '{idea}' ({duration_seconds}s)...")
    response_text = generate_text(prompt)

    import re
    # Extract JSON using regex from the response text
    json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
    
    if json_match:
        clean_text = json_match.group(1).strip()
    else:
        # Fallback to the original cleaning method if regex fails
        clean_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        script_data = json.loads(clean_text)
        if "scenes" not in script_data:
            raise ValueError("JSON missing 'scenes' key")
        return script_data
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        # Log parts of the failed response for debugging
        print("Raw response (start):", response_text[:500])
        print("Raw response (end):", response_text[-500:])
        raise ValueError("LLM did not return valid JSON. Check console for details.")

# Test
if __name__ == "__main__":
    idea = """Yasin’s family moved from Iraq to England when he was just a young boy. Yasin did not want to leave his home in Samarra but his father said that it was best for the family because it was not safe to live there anymore and he wanted his son to grow up in a country that was accepting of all people. Yasin’s father told his son that England was a multicultural country where people lived and worked together regardless of race or religious beliefs.

Although Yasin was not happy about leaving Iraq, he soon settled into his new life in a big city called London. London was very exciting with its tall buildings and museums, and Yasin especially liked the London Planetarium and the big River Thames with all of its old bridges.

Yasin even made friends with a boy who lived next door, called Andrew. All summer long, Andrew and Yasin played in the park or went to the zoo with Andrew’s mum. Andrew shared his toys and his comics with Yasin and told him all about his favourite superheroes. They even built a camp in Yasin’s back garden where they would hide from the grownups.

The summer was a fun time and young Yasin soon felt quite at home in London even though it was a very big city and not nearly as sunny and hot as it was in Samarra. His English got better and better, especially with help from Andrew, although there were a lot of words that Yasin did not understand and he often felt silly because he couldn’t speak as well as he would like.

When September finally came around and the leaves began to fall from the trees, Yasin’s father explained that it was time for his son to go to school. Yasin was seven years old so he would be going to year three of the local primary school – the same year as his friend Andrew!

Although Yasin was very nervous about going to school, his father and mother assured him that it would be a fun place where he would meet lots of new friends and learn lots of interesting new things.

‘English schools are supposed to be very good,’ said Yasin’s mother.

‘And your English will get better in no time,’ assured his father.

Yasin was still not convinced, but when Andrew knocked on the door that morning with a big smile on his face saying how fun it was going to be at school, Yasin felt much better because he trusted his friend.

The two boys chatted all the way to the school gates. Andrew told Yasin about the playground and who was the best teacher and what boys were the most fun and what girls were pretty and how they often served custard for pudding at lunchtimes. Yasin did not know what custard was, but Andrew looked very excited about it so Yasin thought it must taste very good.

But when the boys got to their class, things did not go how Yasin imagined they would. The teacher told Andrew to take a seat at the front of the class as she introduced Yasin to the rest of the children. He did not like standing up in front of the class and one boy shouted that he was a smelly foreigner. The boys and girls all laughed, and then another boy made fun of Yasin’s accent when he was asked to say his name and where he came from.

‘I can’t understand him, miss. He can’t even speak English,’ said the nasty boy.

Finally, Yasin was allowed to take a seat at the back of the class but he wished that he was sitting next to Andrew as he felt very alone. The girl sitting beside him kept looking at him in a strange way that made Yasin uncomfortable, and during the lesson she put her hand up and asked the teacher if she could move places. Yasin did not understand what he had done to offend the girl.

When the bell went, it was time to go out into the playground. All the children closed their books, put on their coats and headed out of the door into the bright autumn sunshine. The teacher kept Yasin back for a moment and gave him a badge with his name on which she pinned to his jumper.

‘There you go,’ she said with a smile. ‘Now all of the children will be able to learn your name.’

Yasin thought that the badge looked silly, and when he went out into the playground all of the children began pointing and laughing.

‘You’ve got a girl’s name,’ said a small boy with blond curly hair.

Yasin wanted to explain that it was not a girl’s name but he was too nervous. When Yasin got nervous, his English was not very good and the words always got stuck in his throat. He was very sad and wanted to run out of the playground back to his mother and father and never return to school again. But just as he was about to run, he heard a familiar voice.

‘Hi Yasin.’ And when he looked up there was Andrew standing right beside him.

Andrew looked at the children gathered around and shook his head. ‘What’s wrong with you lot?’ he asked. ‘I told my friend Yasin that school was fun. Why are you ruining it for him?’

‘He’s different,’ said a very tall girl who was standing at the front of the crowd.

‘So are you,’ said Andrew. ‘You are the tallest girl in the whole school and you don’t like it when people make fun of you, do you?’

Then Andrew looked at the boy with the curly hair. ‘And you don’t like it when people say that you have girl’s hair,’ he said to the boy. ‘We are all different and that is what makes us interesting. What would life be like if we were all the same as one another?’

There was silence among the children.

Then Yasin lifted his head high. ‘Boring,’ he said with a smile.

‘That’s right!’ exclaimed Andrew, returning his friend’s smile. ‘Really boring!’

And with that all of the children began to laugh.

‘Really boring,’ they chanted at one another.

Andrew went on to explain how he had spent the summer with Yasin, how they had built a camp together and played in the park, and how Yasin preferred Batman to Superman, and how he really was different because he didn’t even like hotdogs!

The children all laughed some more and soon everybody was talking about all the things that made them different from one another. Peter Jenkins even lifted up his jumper and showed everybody a big purple birthmark on the front of his belly.

‘Now that’s what I call different,’ he said triumphantly. ‘I bet none of you have a big birthmark like mine!’

When break time was over, Andrew put his hand up in class and suggested to the teacher that they should spend the lesson talking about how great it was that everybody was so different from everybody else and how people came to England from all over the world to begin a new life just like his friend Yasin.

The teacher agreed that it was important to be an individual, and she also said how wonderful it was that the whole of Britain was such a multicultural island. Yasin wrote these two words down in his book and promised himself that he would learn them both and remember them always. He also wrote the word ‘friend’ in his book. He already knew what that meant, but he just wanted to write it down because he felt so lucky to have a good friend like Andrew who stood up for people and did not judge them just because they were different. (generate face without any eyes)

 """
    script = generate_script(idea, "Intriguing", "Digital Art", 180)
    print(json.dumps(script, indent=2))