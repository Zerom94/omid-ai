import qrcode
from qrcode.constants import ERROR_CORRECT_M
from typing import Optional
from PIL import Image

def generate_qr(data: str, *, box_size: int = 10, border: int = 4, error_correction=ERROR_CORRECT_M) -> Image.Image:
    """
    Generate a QR code image.

    Parameters
    ----------
    data : str
        The data to encode.
    box_size : int, optional
        Size of each box in pixels. Default 10.
    border : int, optional
        Border size in boxes. Default 4.
    error_correction : qrcode.constants, optional
        Error correction level. Default ERROR_CORRECT_M.

    Returns
    -------
    PIL.Image.Image
        The generated QR code image.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    return img
