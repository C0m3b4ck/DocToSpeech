import torch
import pyfiglet
import pathlib
from TTS.api import TTS
from datetime import datetime

def greet():
	ASCII_art_greet = pyfiglet.figlet_format("DocToSpeech",font='alphabet')
	print(ASCII_art_greet)
	ASCII_art_credit = pyfiglet.figlet_format("By C0m3b4ck under APL 2.0")
	print(ASCII_art_credit)

def get_user_input_docs():
	print("Currently supported formats: [PDF, EPUB, DOCX, DOC, HTML, DJVU, TXT]")
	doc_path = str(input("Input doc path: "))
	print("Document path: ", doc_path)
	file_extention = (pathlib.Path(doc_path).suffix).lower()
	print("Document file extention: ", file_extention)
	
	# Convert to .txt, then return .txt path
	if (file_extention == ".epub"):
		txt_path = epub_to_text(doc_path)
	elif (file_extention == ".pdf"):
		txt_path = pdf_to_text(doc_path)
	elif (file_extention == ".docx"):
		txt_path = docx_to_text(doc_path)
	elif (file_extention == ".doc"):
		txt_path = doc_to_text(doc_path)
	elif (file_extention == ".html" or file_extention == ".htm"):
		txt_path = html_to_text(doc_path)
	elif (file_extention == ".djvu"):
		txt_path = djvu_to_text(doc_path)
	# If file is already .txt, proceed to tts option selection
	elif (file_extention == ".txt"):
		print("File already in raw text format! Proceeding to tts option selection...")
		txt_path = doc_path
	else
		print("Unrecognized extention.")
	while (len(choice) != 1) and choice != "y" and choice != "n"):
		choice = input("Treat the inputted doc as text file? y/n: ")
		choice.lower()
		if (choice == "y"):
			print("File already in raw text format! Proceeding to tts option selection...")
			txt_path = doc_path
		else if (choice == "n"):
			print("Unknown file extention. Closing program.")
			exit()

def make_tts_voiceover(text_to_say, cloning_audio_relative_path, language, file_name):

	# Get device
	device = "cuda" if torch.cuda.is_available() else "cpu"

	# List available TTS models
	#print("Available models: ",TTS().list_models())

	# Initialize TTS
	tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

	# List speakers
	#print("Speakers: ",tts.speakers)

	# Run TTS
	# ❗ XTTS supports both, but many models allow only one of the `speaker` and
	# `speaker_wav` arguments
	
	# Get current datetime object
	current_datetime = datetime.now()

	# Convert datetime object to timestamp
	current_timestamp = current_datetime.timestamp()
	print("Current Timestamp:", current_timestamp)
	output_path = (file_name + "_" + current_timestamp + ".wav")
	print("Output file name: ", output_path)
	# TTS with list of amplitude values as output, clone the voice from `cloning_audio_relative_path`
	wav = tts.tts(
  		text=text_to_say,
  		speaker_wav=cloning_audio_relative_path,
  		language=language,
		file_path=output_path
	)
	# TTS to a file, use a preset speaker
	#tts.tts_to_file(
	#  text="Hello world!",
	#  speaker="Craig Gutsy",
	#  language="en",
	#  file_path="output.wav"
	#)

if __name__ == '__main__':
	greet()
	get_user_input_docs()
