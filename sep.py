import os
import random
import shutil

# Set up paths
original_folder = 'Dataset'
train_folder = "train"
test_folder = "test"

# Create train and test folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Define split ratio
train_ratio = 0.8

# Iterate over the original folders
for folder_name in os.listdir(original_folder):
    folder_path = os.path.join(original_folder, folder_name)

    # Create train and test subfolders
    train_subfolder = os.path.join(train_folder, folder_name)
    test_subfolder = os.path.join(test_folder, folder_name)
    os.makedirs(train_subfolder, exist_ok=True)
    os.makedirs(test_subfolder, exist_ok=True)

    # List all images in the folder
    images = os.listdir(folder_path)
    num_images = len(images)

    # Calculate the number of images for train and test
    num_train = int(train_ratio * num_images)
    num_test = num_images - num_train

    # Randomly select images for train and test
    random.shuffle(images)
    train_images = images[:num_train]
    test_images = images[num_train:]

    # Move images to train folder
    for image in train_images:
        src = os.path.join(folder_path, image)
        dst = os.path.join(train_subfolder, image)
        shutil.copy(src, dst)

    # Move images to test folder
    for image in test_images:
        src = os.path.join(folder_path, image)
        dst = os.path.join(test_folder, folder_name, image)
        shutil.copy(src, dst)
