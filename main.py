import os
import shutil
from src.helpers import generate_pages_recursive

def copy_directory(source_dir, dest_dir):   
    dir_list = os.listdir(source_dir)
    for object in dir_list:
        if os.path.isfile(f"{source_dir}/{object}"):
            print(f"Copying from: '{source_dir}/{object}' to '{dest_dir}/{object}'")
            shutil.copy(f"{source_dir}/{object}", f"{dest_dir}/{object}") 
        else: 
            if not os.path.exists(f"{dest_dir}/{object}"):
                os.mkdir(f"{dest_dir}/{object}")
            copy_directory(f"{source_dir}/{object}", f"{dest_dir}/{object}")

def copy_assets_to_public_dir():
    print("Processing static assets...")
    
    # working directory paths
    source_dir = "static" # staitc folder in root
    dest_dir = "public" # public folder in root
           
    #   delete all content in the destination dir    
    print("Deleting 'public' folder...")
    if os.path.exists(dest_dir):
       shutil.rmtree(dest_dir)

    # make the public directory    
    os.mkdir(dest_dir)
        
    print("Copying assets to 'public' directory...")
    copy_directory(source_dir, dest_dir)
    print("Finished copying assets.")  

def main():   
    # copy assets from 'static' folder to 'public
    copy_assets_to_public_dir()
    
    # create html page from markdown
    generate_pages_recursive("content", "template.html", "public")

main()
