# app/utils/pdf.py
import os
from xhtml2pdf import pisa
from jinja2 import Template
from tempfile import NamedTemporaryFile
from app.models.parametri import ParametriAnalize


# === HTML TEMPLATE (osnovni stil, prilagodi po potrebi) ===
PDF_TEMPLATE = """
<html>
  <head>
    <style>
      body { font-family: DejaVu Sans, sans-serif; font-size: 12pt; }
      h1 { color: #003366; }
      .section { margin-bottom: 20px; }
      .label { font-weight: bold; }
    </style>
  </head>
  <body>
    <h1>Izveštaj o analizi korisnika</h1>
    <div class="section">
      <p><span class="label">Pol:</span> {{ analiza.pol }}</p>
      <p><span class="label">Godine:</span> {{ analiza.godine }}</p>
      <p><span class="label">Trudnoća:</span> {{ analiza.trudnoca }}</p>
      <p><span class="label">Dijagnoza:</span> {{ analiza.dijagnoza }}</p>
      <p><span class="label">Komorbiditeti:</span> {{ analiza.komorbiditeti }}</p>
      <p><span class="label">Alergije:</span> {{ analiza.alergije }}</p>
    </div>
    <div class="section">
      <p><span class="label">Fiziološki status:</span><br>{{ analiza.fizioloski_status.replace('\n', '<br>') }}</p>
      <p><span class="label">Nutritivni status:</span><br>{{ analiza.nutritivni_status.replace('\n', '<br>') }}</p>
      <p><span class="label">Psihološki faktori:</span><br>{{ analiza.psiholoski_faktori.replace('\n', '<br>') }}</p>
      <p><span class="label">Životni stil:</span><br>{{ analiza.zivotni_stil.replace('\n', '<br>') }}</p>
      <p><span class="label">Genetski faktori:</span><br>{{ analiza.genetski_faktori.replace('\n', '<br>') }}</p>
      <p><span class="label">Okruženje:</span><br>{{ analiza.okruzenje.replace('\n', '<br>') }}</p>
    </div>
  </body>
</html>
"""


def generate_pdf_from_analiza(analiza: ParametriAnalize) -> str:
    """
    Generiše PDF iz instance ParametriAnalize i vraća putanju do PDF fajla.
    """
    html_content = Template(PDF_TEMPLATE).render(analiza=analiza)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pisa_status = pisa.CreatePDF(src=html_content, dest=temp_file)
        if pisa_status.err:
            raise Exception("Greška pri generisanju PDF fajla")
        return temp_file.name
