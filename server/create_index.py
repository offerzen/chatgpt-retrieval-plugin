import os
from datastore.factory import get_datastore
from services.file import get_document_from_file
from models.models import *
import asyncio
from services.file import *
from fastapi import UploadFile
from typing import List

datastore = None

async def startup():
    global datastore
    datastore = await get_datastore()


async def process_directory(directory_path: str) -> List[Document]:
    """Process all files in a directory and its subdirectories and return a list of Document objects."""
    documents = []
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "rb") as file:
                    file_content = file.read()
                    metadata = DocumentMetadata(source=Source.file)
                    document = await get_document_from_file(filename, file_content, metadata)
                    documents.append(document)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return documents


import argparse

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("directory_path", help="The path to the directory to process")
    args = parser.parse_args()

    # Call startup function
    await startup()

    # Process all files in the directory
    documents = await process_directory(args.directory_path)

    # Upsert the documents to the datastore
    try:
        ids = await datastore.upsert(documents)
        print(f"Upserted documents with IDs: {ids}")
    except Exception as e:
        print(f"Error upserting documents: {e}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

