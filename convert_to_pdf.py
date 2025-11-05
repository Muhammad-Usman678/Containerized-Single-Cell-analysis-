"""
Convert HTML report to PDF using weasyprint or alternative methods.
"""

import os
from pathlib import Path

def html_to_pdf_weasyprint():
    """Convert using WeasyPrint (best quality)."""
    try:
        from weasyprint import HTML
        
        html_path = "results/single_cell_analysis/interactive_report.html"
        pdf_path = "results/single_cell_analysis/analysis_report.pdf"
        
        print("Converting HTML to PDF using WeasyPrint...")
        HTML(html_path).write_pdf(pdf_path)
        print(f"✓ PDF saved to: {pdf_path}")
        return True
    except ImportError:
        print("WeasyPrint not installed. Trying alternative method...")
        return False

def html_to_pdf_pdfkit():
    """Convert using pdfkit (wkhtmltopdf)."""
    try:
        import pdfkit
        
        html_path = "results/single_cell_analysis/interactive_report.html"
        pdf_path = "results/single_cell_analysis/analysis_report.pdf"
        
        print("Converting HTML to PDF using pdfkit...")
        pdfkit.from_file(html_path, pdf_path)
        print(f"✓ PDF saved to: {pdf_path}")
        return True
    except Exception as e:
        print(f"pdfkit failed: {e}")
        return False

def html_to_pdf_playwright():
    """Convert using Playwright (headless browser)."""
    try:
        from playwright.sync_api import sync_playwright
        
        html_path = Path("results/single_cell_analysis/interactive_report.html").absolute()
        pdf_path = "results/single_cell_analysis/analysis_report.pdf"
        
        print("Converting HTML to PDF using Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file:///{html_path}")
            page.pdf(path=pdf_path, format="A4", print_background=True)
            browser.close()
        
        print(f"✓ PDF saved to: {pdf_path}")
        return True
    except Exception as e:
        print(f"Playwright failed: {e}")
        return False

if __name__ == "__main__":
    # Try methods in order of quality
    methods = [
        ("WeasyPrint", html_to_pdf_weasyprint),
        ("Playwright", html_to_pdf_playwright),
        ("pdfkit", html_to_pdf_pdfkit),
    ]
    
    success = False
    for name, method in methods:
        if method():
            success = True
            break
    
    if not success:
        print("\n❌ All methods failed. Please install one of:")
        print("  pip install weasyprint")
        print("  pip install playwright && playwright install chromium")
        print("  pip install pdfkit")
