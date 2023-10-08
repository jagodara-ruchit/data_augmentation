import os
import shutil 
generated_audiofile_path = 'try'    		# Give the path to your audio files generated
input_path = 'text'                             # Give your input path to text file
wav_output_file_path = 'wav_final.scp'          # Give your final output path here for wav.scp file
text_output_file_path = 'text_final'            # Give your final output path here for text file
spk2utt_output_file_path = 'spk2utt_final'      # Give your final output path here for spk2utt file
utt2spk_output_file_path = 'utt2spk_final'      # Give your final output path here for utt2spk file


# we can create a temparory text_new.scp file using text file to take reference because we have not changed the words which are present in the audio files 
# we have just changed their parameters so the text file will remain same but we have to add same thing to their because we have 
# changed the name of audio_files so here this code will give you new wav.scp,text,spk2utt,utt2spk files which then you have to manually add to
# original files. 

# Creating a temparory text_new file
output_path = 'text_new'         # This is a temparory file so do not change anything related to this
with open(input_path,'r') as f:
    data = f.read().split('\n')
f.close()
file = open(output_path,'w')
for i in range(len(data)):
    file.write(data[i][:8]+'7'+data[i][9:]+'\n')  #Use any other id instead of 7 if you want to change the id of audio files
file.close()
ref_file_path = output_path

with open(ref_file_path,'r') as file:
    data = file.read().split('\n')
file.close()

os.remove(ref_file_path)

audiofile_names = os.listdir(generated_audiofile_path)

wav_output_file = open(wav_output_file_path,'w')
text_output_file = open(text_output_file_path,'w')
utt2spk_output_file = open(utt2spk_output_file_path,'w')
spk2utt_output_file = open(spk2utt_output_file_path,'w')
y=8  #This is the id of audio files which you have given in text_new file. If you have changed the id then change this also.
for audio_file in audiofile_names:
    for iterator in range(len(data)):
        audio_name = 'indian_s01_'+data[iterator][8:32]+'.wav'
        if audio_name == audio_file:
            id = audio_name[11:35]
            wav_output_file.write(f'{y}S00011-{id} sox db/audio_data/speaker_01/indian_s01_{id}.wav -r 8000 -c 1 -t wav -|\n')
            text_output_file.write(data[iterator][:8]+id+data[iterator][32:]+'\n')
            spk2utt_output_file.write(f'{y}S00011-{id} {y}S00011-{id}'+'\n')
            utt2spk_output_file.write(f'{y}S00011-{id} {y}S00011-{id}'+'\n')
wav_output_file.close()
text_output_file.close()
utt2spk_output_file.close()
spk2utt_output_file.close()
print("Excecution competed successfully.")
