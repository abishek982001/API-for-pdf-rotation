from flask import Flask, send_from_directory
import PyPDF2
import os

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to Pdf Rotater"


@app.route("/rotate/<path:file_path>/<int:angle>/<int:page_number>")
def rotate_single_page(file_path, angle, page_number):
    pdf_in = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        if pagenum == page_number-1 and angle % 90 == 0:
            page.rotateClockwise(angle)
        pdf_writer.addPage(page)
    pdf_out = open('rotated.pdf', 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
    working_dir = os.path.abspath(os.getcwd())

    return send_from_directory(working_dir, "rotated.pdf")


@app.route("/rotate/<path:file_path>/<int:angle>/<int:start>/<int:end>")
def rotate_multiple_page(file_path, angle, start, end):
    angle = int(angle)
    limit = set(range(int(start)-1, int(end)))

    pdf_in = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        if pagenum in limit and angle % 90 == 0:
            page.rotateClockwise(angle)
        pdf_writer.addPage(page)
    pdf_out = open('rotated.pdf', 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
    working_dir = os.path.abspath(os.getcwd())

    return send_from_directory(working_dir, "rotated.pdf")


if __name__ == '__main__':
    app.run(debug=True)
