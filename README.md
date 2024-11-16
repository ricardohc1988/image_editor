# Image Editor

**Image Editor** is a Python-based project for image processing tasks, including background removal and advanced image manipulation.

## Features
- **User Interface:** Simple and modern GUI built with `customtkinter`.
- **Background Removal:** Removes image backgrounds using `rembg` and `backgroundremover`.
- **Image Format Support:** Handles various image formats like JPG and PNG with the help of `pillow`.
- **Advanced Image Manipulation:** Utilizes OpenCV for additional image processing features.

## Requirements
- Python 3.10
- Virtual environment (recommended)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/image_editor.git
   cd image_editor

2. Create and activate a virtual environment:
    ```bash
    pip install pipenv
    pipenv shell

3. Install dependencies
    ```bash
    pipenv install

## Usage
1. Prepare your input images in a compatible format (JPG, PNG, etc.).
2. Run the main script:
    ```bash
    python image_editor.py

3. Follow the instructions in the GUI to load and process images.

## Libraries 
- **customtkinter: For the graphical user interface.**
- **pillow: For basic image handling.**
- **opencv-python: For advanced image manipulation.**
- **rembg: For background removal.**
- **backgroundremover: Additional tool for background removal.**