import os
from io import BytesIO
import PyPDF2
from PIL import Image, ImageFont, ImageDraw
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat import backends
from endesive.pdf.cms import sign
from django.utils import timezone

from conf.settings import BASE_DIR, CERTIFICATE_PATH, CERTIFICATE_PASSWORD

REASON = "On behalf of the Secretary of State"
LOCATION = "Department for International Trade"
CONTACT = "spire@berr.gsi.gov.uk"

FONT = os.path.join(BASE_DIR, "assets", "fonts", "Helvetica.ttf")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "assets", "images", "dit_emblem.png")
TITLE_FONT_SIZE = 80
FONT_SIZE = 50
SIGNATURE_POSITIONING = (50, 675, 450, 775)
TITLE_POSITIONING = (500, 30)
TEXT_POSITIONING = (500, 180)


def _load_certificate():
    path = os.path.join(BASE_DIR, CERTIFICATE_PATH)
    with open(path, "rb") as fp:
        return pkcs12.load_key_and_certificates(fp.read(), str.encode(CERTIFICATE_PASSWORD), backends.default_backend())


def _get_signature_text(date):
    return "\n\n".join(
        [f"Date: {date.strftime('%Y.%m.%d %H:%M:%S GMT')}", f"Reason: {REASON}", f"Location: {LOCATION}"]
    )


def _add_blank_page(pdf_bytes):
    # Write a blank page
    pdf = PyPDF2.PdfFileReader(pdf_bytes)
    out_pdf = PyPDF2.PdfFileWriter()
    out_pdf.appendPagesFromReader(pdf)
    out_pdf.addBlankPage()
    num_pages = out_pdf.getNumPages()

    # Convert back into bytes
    output_buffer = BytesIO()
    out_pdf.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read(), num_pages


def _get_signature_image(text):
    # Load image and fonts
    image = Image.open(BACKGROUND_IMAGE)
    title_font = ImageFont.truetype(FONT, TITLE_FONT_SIZE)
    text_font = ImageFont.truetype(FONT, FONT_SIZE)
    drawing = ImageDraw.Draw(image)

    # Add text
    drawing.text(TITLE_POSITIONING, "Digital Signature", font=title_font, fill=(0, 0, 0))
    drawing.text(TEXT_POSITIONING, text, font=text_font, fill=(0, 0, 0))

    return image


def sign_pdf():
    date = timezone.now()
    signing_metadata = {
        "sigflags": 3,
        "sigandcertify": True,
        "signaturebox": SIGNATURE_POSITIONING,
        "signature_img": _get_signature_image(_get_signature_text(date)),
        "contact": CONTACT,
        "location": LOCATION,
        "signingdate": date.strftime("D:%Y%m%d%H%M%S+00'00'"),
        "reason": REASON,
    }
    key, cert, othercerts = _load_certificate()

    with open(os.path.join(BASE_DIR, "test.pdf"), "rb") as original_pdf:
        # Add a blank page to the end
        pdf, num_pages = _add_blank_page(original_pdf)

        # Add the signature to the last page
        signing_metadata["sigpage"] = num_pages - 1
        signature = sign(pdf, signing_metadata, key, cert, othercerts, "sha256")

        output_name = os.path.join(BASE_DIR, "test.pdf").replace(".pdf", "-signed-cms.pdf")
        data = pdf + signature
        with open(output_name, "wb") as fp:
            fp.write(data)

        return data
