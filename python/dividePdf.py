import fitz  # PyMuPDF
import os

def split_pdf_by_custom_ranges(input_pdf_path, output_prefix, page_ranges):
    try:
        pdf_document = fitz.open(input_pdf_path)
    except Exception as e:
        print(f"Error al abrir el PDF: {e}")
        return

    total_pages = pdf_document.page_count

    output_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docPDF'))
    os.makedirs(output_dir, exist_ok=True)

    for i, (start, end) in enumerate(page_ranges):
        if start < 1 or end > total_pages or start > end:
            print(f"Rango inválido: ({start}, {end})")
            continue
        output_pdf = fitz.open()
        for page_num in range(start - 1, end):  # Índices base 0
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        output_filename = os.path.join(output_dir, f"{output_prefix}_part_{i+1}.pdf")
        output_pdf.save(output_filename)
        output_pdf.close()
        print(f"Guardado: {output_filename}")

    pdf_document.close()


# Ejemplo de uso
input_pdf = "/home/carlosv/Descargas/00-NCh-433-Of-1996-Mod-2009-DS-61-2011-refundido.pdf"
output_prefix = "Nch433_of96_Mod2012_"
page_ranges = [(11,16),(16,37),(38,46),(47,48),(49,52),(53,57),(58,58),(59,74)]

#Verificar si existe archivo o directorio
if not os.path.exists(input_pdf):
    print("No existe:", input_pdf)



split_pdf_by_custom_ranges(input_pdf, output_prefix, page_ranges)