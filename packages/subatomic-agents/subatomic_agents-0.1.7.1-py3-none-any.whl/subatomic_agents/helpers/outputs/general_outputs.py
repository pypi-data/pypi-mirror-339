from weasyprint import HTML, CSS
import io

def html_to_pdf(html_content):
    """
    Convert HTML string to PDF and return a BytesIO object for sending via send_file.

    :param html_content: A string containing the HTML code.
    :return: A BytesIO object containing the binary PDF data.
    """
    # Custom CSS for setting the page margins
    custom_css = CSS(string="""
        @page {
            margin: 0.25in; /* Set margin to 0.25 inches for all sides */
        }
    """)

    # Convert the HTML string to a PDF in memory, with custom margins
    pdf_bytes = HTML(string=html_content).write_pdf(stylesheets=[custom_css])

    # Create a BytesIO object from the PDF bytes
    pdf_stream = io.BytesIO(pdf_bytes)

    # Return the BytesIO stream (file-like object)
    return pdf_stream
