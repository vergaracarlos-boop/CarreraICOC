import fitz  # PyMuPDF

def split_pdf_by_custom_ranges(input_pdf_path, output_prefix, page_ranges):
    try:
        pdf_document = fitz.open(input_pdf_path)
    except Exception as e:
        print(f"Error al abrir el PDF: {e}")
        return

    total_pages = pdf_document.page_count

    for i, (start, end) in enumerate(page_ranges):
        if start < 1 or end > total_pages or start > end:
            print(f"Rango inválido: ({start}, {end})")
            continue
        output_pdf = fitz.open()
        for page_num in range(start - 1, end):  # Índices base 0
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        output_filename = f"{output_prefix}_part_{i+1}.pdf"
        output_pdf.save(output_filename)
        output_pdf.close()
        print(f"Guardado: {output_filename}")

    pdf_document.close()

# Ejemplo de uso
input_pdf = "C:/Users/chopp/OneDrive/Biblioteca Digital Vergara Ingenieria7Libros Investigación/Metodologia_de_la_Investigacion_-_Hernan.pdf"
output_prefix = "Metodología_Investigacion_HS_"
page_ranges = [(35,54),(55,65),(67,90),(91,120),(121,134),(135,158),(159,202),(203,228),(229,302),(303,368),(369,387),(389,414),(416,426),(427,500),(501,540),(541,563),(565,621)]




split_pdf_by_custom_ranges(input_pdf, output_prefix, page_ranges)