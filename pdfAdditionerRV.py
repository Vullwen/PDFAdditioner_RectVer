import os
import PyPDF2
import re
import math
import time

inputDirectory = 'C://Users//cpinquier//Documents//taf//Programmes//pdfAdditionerRV//CNI-R-V'



def main():
    fileAct = 1
    err = []

    # Set the directory containing the PDF files
    inputDirectory = 'C://Users//cpinquier//Documents//taf//Programmes//pdfAdditionerRV//input'
    # Set the directory where the output PDF files will be saved
    outputDirectory = 'C://Users//cpinquier//Documents//taf//Programmes//pdfAdditionerRV//output'

    # Get a list of all of the PDF filenames in the input directory
    pdfFilenames = [f for f in os.listdir(inputDirectory) if f.endswith('.pdf')]
    # Sort the filenames	
    pdfFilenames.sort()

    print("Recherche des fichiers R et V")
    pdfDict = {}
    for file in pdfFilenames:
        progressBar(len(pdfFilenames), pdfFilenames.index(file)+1, err)
        time.sleep(0.01)
        if file.endswith('R.pdf'):
            pdfDict[file] = file.replace('R.pdf', 'V.pdf')
        elif file.endswith('V.pdf'):
            pdfDict[file.replace('V.pdf', 'R.pdf')] = file
        else:
            err.append(file)
            continue
    
    fileAct = 1
    print("Addition des fichiers")
    for fileR, fileV in pdfDict.items():
        time.sleep(0.01)
        # Ouvrez les fichiers PDF
        progressBar(len(pdfDict), fileAct, err)
        fileAct += 1
        with open(f'{inputDirectory}//{fileR}', 'rb') as fileHandle1, open(f'{inputDirectory}//{fileV}', 'rb') as fileHandle2:
            # Créez des objets PDF à partir des fichiers
            try:
                pdf1 = PyPDF2.PdfFileReader(fileHandle1, strict=False)               
                pdf2 = PyPDF2.PdfFileReader(fileHandle2, strict=False)                
                # Créez un nouvel objet PDF
                pdfWriter = PyPDF2.PdfFileWriter(False)
                # Ajoutez chaque page des fichiers PDF originaux au nouveau fichier
                for pageNum in range(pdf1.getNumPages()):
                    pdfWriter.addPage(pdf1.getPage(pageNum))
                for pageNum in range(pdf2.getNumPages()):
                    pdfWriter.addPage(pdf2.getPage(pageNum))
                # Créez le fichier PDF combiné en utilisant le nom des fichiers originaux
                with open(f'{outputDirectory}/{fileR[:-6]}_combined.pdf', 'wb') as fh:
                    pdfWriter.write(fh)

            except:
                valFin, val2 = re.split(r'[_-]', fileR, 1)
                err.append(valFin)
                continue
            print("\r", end='')
    print('\rFin d\'execution\n', end='')
        
            

def progressBar(nbVal, actVal, err = []):
    """
    Args:
        nbVal (int): length of the list that is being iterated.
        actVal (int): actual value of the iteration.
        err (list, optional): potentials errors, only print if not []. Defaults to [].
    """
    percent = actVal/nbVal
    nEquals = math.floor(percent*20)
    bar = '=' * nEquals + ' ' * ( 20 - nEquals )

    print("\r", end='')
    print(f"[{bar}] {percent*100:.2f}%", end='')

    if percent == 1:
        print("\nTerminé\n")
    if err != []:
        print("Erreurs: (",len(err),")")
        print(err)
        print("\n")

def verifyFile(path):
    if os.path.exists(path) == False:
        return path


if __name__ == '__main__':
    main()
