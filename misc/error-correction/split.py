import os
from PIL import Image

def split_image_5x5(image_path, output_directory):
    """
    Splits an image into 25 parts (5x5 grid) and saves them to an output directory.
    """
    try:
        # Open the target image
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: Could not find the image at '{image_path}'")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    img_width, img_height = img.size
    
    # Calculate the base width and height of each tile
    tile_width = img_width // 5
    tile_height = img_height // 5

    print(f"Original image size: {img_width}x{img_height}")
    print(f"Base tile size: {tile_width}x{tile_height}")

    tile_number = 1

    # Loop through the 5x5 grid
    for row in range(5):
        for col in range(5):
            # Calculate the bounding box for the crop
            left = col * tile_width
            upper = row * tile_height
            
            # For the last column/row, grab any remaining pixels just in case 
            # the image dimensions aren't perfectly divisible by 5
            right = img_width if col == 4 else left + tile_width
            lower = img_height if row == 4 else upper + tile_height

            # Crop the image
            tile = img.crop((left, upper, right, lower))
            
            # Generate the filename and save
            # Zfill(2) ensures files are named part_01.png, part_02.png, etc.
            filename = os.path.join(output_directory, f"part_{str(tile_number).zfill(2)}.png")
            tile.save(filename)
            
            tile_number += 1

    print(f"Success! 25 tiles saved to the '{output_directory}' folder.")

# === Example Usage ===
if __name__ == "__main__":
    # Replace 'input_image.jpg' with the path to your actual image
    IMAGE_FILE = "chall.png" 
    OUTPUT_FOLDER = "split_pieces"
    
    split_image_5x5(IMAGE_FILE, OUTPUT_FOLDER)