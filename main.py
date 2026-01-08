from audio_manager import AudioManager
import os
from file_utils import *
from llm.completor_vision import OpenAICompletorVision
from llm.completor_openai import OpenAICompletor
import subprocess
import numpy as np
import ast
import rospy
from std_msgs.msg import String


api_key = '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'
image_path = "/home/crslab/Grounded-Segment-Anything/images/top_down_img.png"
# image_path = "/home/crslab/Grounded-Segment-Anything/images/top_down_img - Copy"

def run_task():
    #### capture scene point cloud
    rospy.init_node("gengraspModule")
    publisher = rospy.Publisher("/graspflow/move_to", String, queue_size=10)
    msg = String("0 0 scan")
    publisher.publish(msg)

    rospy.sleep(5)
    #### call gsam to segment objects, saved as scene_pc and obj_pc
    subprocess.call

    #### afterwards, format scene_pc and obj_pc to become scene.json
    #### then call graspgen demo_scene_pc to create grasps
    #### save these grasps
    #### in the tower, allow the user to choose which grasp to use



def main():
    completor = OpenAICompletorVision(api_key, model="gpt-4o-2024-08-06")
    # completor = OpenAICompletor(api_key, model="gpt-4o")
    audio_manager = AudioManager()

    # ================== Task 0: take the photo / call GSAM ==================
    # 2. call GSAM / make sure the target dir is correct.
   
    # base_dir = "/home/crslab/Grounded-Segment-Anything/"
    # subprocess.Popen(['python', f'{base_dir}grounded_sam_demo.py', 
    #                   "--config", f"{base_dir}GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", 
    #                   "--grounded_checkpoint", f"{base_dir}groundingdino_swint_ogc.pth", 
    #                   "--sam_checkpoint", f"{base_dir}sam_vit_h_4b8939.pth", 
    #                   "--input_image", image_path, 
    #                   "--output_dir", f"{base_dir}outputs/test", 
    #                   "--box_threshold", "0.3", 
    #                   "--text_threshold", "0.25", 
    #                   "--text_prompt", "mug, box, bowl", 
    #                   "--device", "cuda"],
    #                   stdout=subprocess.DEVNULL,  # Suppress stdout
    #                   stderr=subprocess.DEVNULL   # Suppress stderr
    #                   )

    # ================== Task 1: analyze the image ==================
    question_prompt = read_txt_file('prompts/demo/question_prompt.txt')
    answered = False

    print("="*40)
    # print("Please tell me your question.")
    input("Press Enter to start recording...")


    question_list = [
        "How can I help you?",
        "What can I assist you with?",
        "Is there anything you need help with?",
        "How may I assist you?",
        "What do you need assistance with today?",
        "How can I be of service to you?",
        "Anything I can help you with?",
        "How can I assist?"
    ]
    chosen_question = np.random.choice(question_list)

    
    audio_manager.speak(chosen_question) #some varations
    text = audio_manager.listen()

    # text = "I want to drink." # fix
    # text = "What are on the table?" 
    # text = "Pick the plate on the table." # fix
    # text = "Pick the orange on the table."
    # text = "Give me this table."
    # text = "Give me this mug."
    # text = "give me this apple."
    # text = "Put the apple and place it in the red mug."
    # text = "Pick this box."
    # text = "Pick this mug."
    # text = "Pick this apple."

    state = "robot hand is empty."

    while True:

        if text:
            question = f"""{question_prompt} 
                        \n The question is: [{text}].
                        \n The current state is: [{state}].
                        """
            # print(f"Question: {text}")

            print("Thinking...")
            # answer = completor.answer(text)
            answer = completor.answer_with_image(question, image_path)


            print(f"Answer1: {answer}")
            audio_manager.speak(answer)

        else: # If the audio is not recognized
            print("Please try again.")
            audio_manager.speak("Sorry, I could not understand you. Could you please repeat your request?") #some variations
            text = audio_manager.listen()
            continue
    
        # ================== Task 2: analyze what to do ==================
        manipulation_prompt = read_txt_file('prompts/demo/manipulation_prompt.txt')
        action_answer = completor.answer(manipulation_prompt)
        print(f"Answer2: {action_answer}")

        action = ast.literal_eval(action_answer)
        with open('item_prompt.txt', 'w') as f:
            f.write(action_answer)


        if action['object'] == None  or action['grasp'] == False:
            pass

        else:
            state = f"robot hand is holding {action['object']}"


        # get next speak
        communication_prompt = read_txt_file('prompts/demo/communication_prompt.txt')
        comm_ans = completor.answer(communication_prompt)
        print('comm_ans:', comm_ans)
        # p1 = completor.pop()
        # p2 = completor.pop()
        # print(p1, p2)


        input("Press Enter to start recording...")
        audio_manager.speak(comm_ans)
        text = audio_manager.listen()

        # can manual reset
        inpt = input("Press Enter to skip... R to reset the state...")
        if inpt == "R" or inpt=="r":
            state = "robot hand is empty."
            print("State reset.")
        else:
            print("State remains.")
   
        completor.clear()

if __name__ == "__main__":
    main()