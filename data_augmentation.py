from pydub import AudioSegment
import os
import shutil

input_dir = 'speaker_01'    # Write the path to your input directory where your all audio_files are present \
                            # in our case it is speaker_01 file of audio_data/hi_test directory


output_dir = 'speaker_01'   # Write the path to your output directory where you want to store other files which will be made by this code
# if os.path.exists(output_dir):
#     shutil.rmtree(output_dir)

noise_path = 'noise.wav'    # Write the path to your noise audio file that we will use to add noise to some files and if you don't have one then
                            # you can just comment out this and remove pair ("add_noise", 0.1) from augmentation_techniques variable which is a list
# Different data augmentation techniques that we will use here with their parameters
augmentation_techniques = [
    ("speed_up", 1.2),      # Speed up by 20%
    ("speed_down", 0.8),    # Speed down by 20%
    ("pitch_up", 100),      # Increase pitch by 100 cents 
    ("pitch_down", -100),   # Decrease pitch by 100 cents 
    ("add_noise", 0.1),     # Add white noise with a volume of 0.1 (here I have taken a gaussian noise)
    ("time_shift", 5000),   # Time shift by 5000 milliseconds (5 seconds)
]

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through each .wav file in the input directory
for iterator,filename in enumerate(os.listdir(input_dir)):
    if filename.endswith(".wav"):
        file_path = os.path.join(input_dir, filename)
        
        # Check the size of the file (in bytes)
        file_size = os.path.getsize(file_path)
        
        # Skip files with size less than 100 bytes
        if file_size < 100:
            print(f"Skipping {filename} due to small size ({file_size} bytes).")
            continue
        
        # Load the original audio file
        audio = AudioSegment.from_file(file_path, format="wav")
        
        # Apply each augmentation technique and save the augmented audio
        technique, parameter = augmentation_techniques[iterator%len(augmentation_techniques)]
        augmented_audio = audio
        if technique == "speed_up":
            augmented_audio = audio.speedup(playback_speed=parameter)
        elif technique == "speed_down":
            augmented_audio = audio.speedup(playback_speed=parameter)
        elif technique == "pitch_up":
            augmented_audio = audio.set_frame_rate(int(audio.frame_rate * (2 ** (parameter / 1200.0))))
        elif technique == "pitch_down":
            augmented_audio = audio.set_frame_rate(int(audio.frame_rate * (2 ** (parameter / 1200.0))))
        elif technique == "add_noise":
            noise = AudioSegment.silent(duration=len(audio))
            noise = noise.overlay(AudioSegment.from_file(noise_path), position=0)
            augmented_audio = audio + noise
        elif technique == "time_shift":
            augmented_audio = audio[:parameter] + AudioSegment.silent(duration=parameter) + audio[parameter:]
        
        # Check if the resulting audio duration is still long enough
        if len(augmented_audio) > 150:
            # Save the augmented audio to the output directory
            output_filename = f"{(os.path.splitext(filename)[0])[:11]+'7'+(os.path.splitext(filename)[0])[12:]}.wav"
            output_path = os.path.join(output_dir, output_filename)
            augmented_audio.export(output_path, format="wav")

print("Data augmentation complete.")
