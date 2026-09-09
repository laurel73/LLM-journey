from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_auto_page_break(False)

        self.set_font("helvetica", "B", 50)
        self.cell(0, 60, "CS50 Shirtificate", align="C")
        self.ln()

        self.image("shirtificate.png", 10, 70, 190)

        name = input("Name: ")
        self.set_font("helvetica", "B", 25)
        self.set_text_color(255, 255, 255)
        self.cell(0, 150, f"{name} took CS50", align="C")


def main():
    pdf = PDF()
    pdf.add_page()
    pdf.output("shirtificate.pdf")


if __name__ == "__main__":
    main()
