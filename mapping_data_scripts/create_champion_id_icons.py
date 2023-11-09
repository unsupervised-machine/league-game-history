import pickle
import shutil
import os

expected_directory = 'league-game-history'
current_directory = os.getcwd()
current_directory_name = os.path.basename(current_directory)

if current_directory != expected_directory:
    raise SystemExit(f"Current directory '{current_directory}' is not the expected directory '{expected_directory}'.")
else:
    print(f"Current directory is the expected directory: '{current_directory}'")

expected_directory = '/path/to/expected/directory'

source_directory = 'static/champion/champion_icons_name'
target_directory = 'static/champion/champion_icons_id'

with open('static/champion/name_to_id_mapping.pkl', 'rb') as pickle_file:
    mapping = pickle.load(pickle_file)

image_name_mapping = {}
for key, value in mapping.items():
    image_name_mapping[f'{value["name"]}.png'] = f'{value["id"]}.png'


for filename in os.listdir(source_directory):
    print(filename)
    if filename in image_name_mapping:
        old_path = os.path.normpath(os.path.join(source_directory, filename))
        print(old_path)
        new_filename = image_name_mapping[filename]
        new_path = os.path.normpath(os.path.join(target_directory, new_filename))
        print(new_path)

        # Rename the file and copy it to the target directory
        shutil.copy(old_path, new_path)
