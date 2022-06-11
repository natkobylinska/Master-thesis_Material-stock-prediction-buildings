from fpdf import FPDF
pdf = FPDF()

# imagelist is the list with all image filenames
imagelist = ("page_1.jpg", "page_2.jpg", "page_3.jpg")
for image in imagelist:
    pdf.add_page()
    pdf.image(image, w = 180)
pdf.output("yourfile.pdf", "F")