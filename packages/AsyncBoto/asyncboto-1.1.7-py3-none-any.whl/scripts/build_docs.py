import os

def create_markdown_files(package_path, docs_path):
    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.relpath(os.path.join(root, file), package_path)
                module_name = f"async_boto.{module_path.replace(os.sep, '.').replace('.py', '')}"
                docs_file_path = os.path.join(docs_path, module_path.replace(".py", ".md"))

                os.makedirs(os.path.dirname(docs_file_path), exist_ok=True)

                with open(docs_file_path, "w") as f:
                    f.write(f"::: {module_name}\n")

if __name__ == "__main__":
    package_path = "async_boto"
    docs_path = "docs/async_boto"
    create_markdown_files(package_path, docs_path)