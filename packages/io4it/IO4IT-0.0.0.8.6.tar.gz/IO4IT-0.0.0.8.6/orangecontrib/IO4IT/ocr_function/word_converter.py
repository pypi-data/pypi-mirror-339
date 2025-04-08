import os
import win32com.client
from pathlib import Path

#docx_path = pdf_path.replace(".pdf", ".docx")
def convert_pdf_structure(input_dir: str, output_dir: str, progress_callback=None):
    """
    return a string with log in  case of error
    Recursively lists all .pdf and .PDF files in the input directory,
    replicates the folder structure in the output directory, and
    creates empty .docx files with the same names.

    Parameters:
    input_dir (str): Path to the input directory containing PDF files.
    output_dir (str): Path to the output directory where DOCX files will be created.
    """
    error_log=""
    if os.name != 'nt':
        error_log="version developped for windows computer "
        return error_log

    nbre_file = 0
    for i, data in enumerate(input_dir):
        input_path = Path(str(input_dir[i]))
        for pdf_file in input_path.rglob("*.pdf"):
            nbre_file += 1

    k = 1
    for i, data in enumerate(input_dir):
        input_path = Path(str(input_dir[i]))
        output_path = Path(str(output_dir[i]))

        if not input_path.exists() or not input_path.is_dir():
            print(f"Error: The input directory '{input_dir}' does not exist or is not a directory.")
            return f"Error: The input directory '{input_dir}' does not exist or is not a directory. "

        for pdf_file in input_path.rglob("*.pdf"):  # Recursively search for .pdf and .PDF files
            relative_path = pdf_file.relative_to(input_path)  # Get relative path from input root
            new_file_path = output_path / relative_path.with_suffix(".docx")  # Change extension to .docx

            # Create necessary directories in the output folder
            new_file_path.parent.mkdir(parents=True, exist_ok=True)
            if 0!= convert_pdf_to_docx(str(pdf_file),str(new_file_path)):
                if error_log!="":
                    error_log+="\n"
                error_log+="error -> "+pdf_file
            if progress_callback is not None:
                progress_value = float(100 * (k) / nbre_file)
                k += 1
                progress_callback(progress_value)
    return error_log

def convert_pdf_to_docx(pdf_path,docx_path):
    # return 0 ok return 1 ok
    to_return = 1
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} doesn t exist.")
        return to_return
    try:
        # Lancer Word
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True  # Mettre à True pour voir Word en action
        word.DisplayAlerts = 0  # Désactiver les alertes et fenêtres
        print(f"Conversion  {pdf_path} to {docx_path}...")

        # Ouvrir le PDF avec les bons paramètres
        doc = word.Documents.Open(pdf_path, ReadOnly=True, ConfirmConversions=False)

        # Sauvegarder en DOCX
        doc.SaveAs(docx_path, FileFormat=16)  # 16 = wdFormatDocumentDefault
        doc.Close(False)

        print(f"Conversion ok : {docx_path}")
        to_return=0
    except Exception as e:
        print(f"Error : {e}")


    finally:
        word.Quit()
        return to_return