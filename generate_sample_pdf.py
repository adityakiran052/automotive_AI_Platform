from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

os.makedirs("data/raw", exist_ok=True)
pdf_path = "data/raw/AUTOSAR_HLD_BrakeSystem.pdf"

c = canvas.Canvas(pdf_path, pagesize=letter)

# Page 1
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 750, "AUTOSAR High-Level Design: Electronic Braking System")
c.setFont("Helvetica", 10)
c.drawString(50, 735, "Document Ref: HLD-EBS-2026-V1.0 | Classification: Internal")

c.setFont("Helvetica-Bold", 12)
c.drawString(50, 690, "1. Architecture Overview")
c.setFont("Helvetica", 10)
text_p1 = [
    "The Electronic Braking System contains three core software components:",
    "  - SWC_BrakeControl: Executes driver deceleration requests and ABS regulation.",
    "  - SWC_SensorFusion: Consolidates raw wheel speeds and yaw rate sensor inputs.",
    "  - SWC_ActuatorInterface: Interfaces with electromechanical hydraulic valves."
]
y = 670
for line in text_p1:
    c.drawString(50, y, line)
    y -= 20

c.showPage()

# Page 2
c.setFont("Helvetica-Bold", 12)
c.drawString(50, 750, "2. Ports and Interface Mapping")
c.setFont("Helvetica", 10)
text_p2 = [
    "SWC_BrakeControl specifies the following communication endpoints:",
    "  - Required Port: Rp_WheelPulse with Interface IVehicleSpeed (from SWC_SensorFusion).",
    "  - Provided Port: Pp_DecelerationCmd with Interface IBrakeActuation (to SWC_ActuatorInterface).",
    "  - Client-Server Port: Cp_Diagnostics with Interface IDiagnosticControl.",
    "",
    "Architectural Rule: If IVehicleSpeed signals fail, SWC_BrakeControl shifts to fail-safe within 15 ms."
]
y = 720
for line in text_p2:
    c.drawString(50, y, line)
    y -= 20

c.save()
print(f"Sample PDF generated at: {pdf_path}")