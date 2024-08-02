from github import Github

def get_repo_files(repo_name, directory_path):
    g = Github()  # No token needed for public repos
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(directory_path)

    files = []
    for content_file in contents:
        if content_file.type == "file":
            files.append(content_file.download_url)  # Or content_file.path for just the path
    
    return files

# Usage
repo_name = "Drakosfire/CardGenerator"
directory_path = "seed_images/item_seeds"

files = get_repo_files(repo_name, directory_path)
print(files)
