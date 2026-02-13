#!/usr/bin/env python3
"""
PDF Folder Joiner
Joins all PDF files in a root folder and all subfolders into one PDF.
Files are merged in order of their path (folder order: 00_Introduction, 01_Regular_Data, ...).
"""

import glob
import os
from typing import List, Optional

import fitz  # PyMuPDF
from tqdm import tqdm

ROOT_DIR = "/home/niklas/Desktop/Uni_Niklas/MASTER/Semester1/ParallelProgrammierung/ParalleleNebenlaeufigeVerteilteProgrammierung_ws25"


def get_pdf_files_recursive(root_path: str) -> List[str]:
    """
    Get all PDF files from root_path and all subfolders, sorted by path
    so that folder order is preserved (e.g. 00_Introduction before 01_Regular_Data).

    Args:
        root_path: Path to the root folder to search

    Returns:
        List of PDF file paths sorted by full path
    """
    if not os.path.exists(root_path):
        raise FileNotFoundError(f"Folder not found: {root_path}")

    root_path = os.path.abspath(root_path)
    pdf_files = []

    for dirpath, _dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename == "slides.pdf":
                full_path = os.path.join(dirpath, filename)
                pdf_files.append(full_path)

    pdf_files.sort()
    return pdf_files


def join_pdfs_recursive(
    input_folder: str,
    output_file: str,
    exclude_patterns: Optional[List[str]] = None,
) -> None:
    """
    Join all PDF files in input_folder and all subfolders into one PDF.
    Order is determined by full path (subfolder order preserved).

    Args:
        input_folder: Root path to search for PDF files
        output_file: Path for the output merged PDF file
        exclude_patterns: List of filename patterns to exclude (e.g., ['*temp*', '*draft*'])
    """
    try:
        pdf_files = get_pdf_files_recursive(input_folder)

        if exclude_patterns:
            filtered_files = []
            for pdf_file in pdf_files:
                filename = os.path.basename(pdf_file)
                should_exclude = False
                for pattern in exclude_patterns:
                    if glob.fnmatch.fnmatch(filename.lower(), pattern.lower()):
                        should_exclude = True
                        break
                if not should_exclude:
                    filtered_files.append(pdf_file)
            pdf_files = filtered_files

        if not pdf_files:
            raise ValueError(f"No PDF files found under {input_folder}")

        print(f"Found {len(pdf_files)} PDF files to join:")
        for i, pdf_file in enumerate(pdf_files, 1):
            rel = os.path.relpath(pdf_file, input_folder)
            print(f"  {i}. {rel}")

        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        merged_pdf = fitz.open()

        print("\nJoining PDFs...")
        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            try:
                pdf_doc = fitz.open(pdf_file)
                merged_pdf.insert_pdf(pdf_doc)
                pdf_doc.close()
            except Exception as e:
                print(f"Warning: Could not process {pdf_file}: {e}")
                continue

        total_pages = len(merged_pdf)
        merged_pdf.save(output_file)
        merged_pdf.close()

        print(f"\nSuccessfully created merged PDF: {output_file}")
        print(f"Total pages: {total_pages}")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    join_pdfs_recursive(
        input_folder=ROOT_DIR,
        output_file=os.path.join(ROOT_DIR, "merged_slides.pdf"),
    )
