import base64
from io import BytesIO
import pdf2image
from jinja2 import Template

def convert_pdf_to_base64_images(pdf_path):
    """Converts PDF pages to base64-encoded images."""
    images = pdf2image.convert_from_path(pdf_path)
    encoded_images = []

    for image in images:
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{encoded}"
        encoded_images.append(data_url)

    return encoded_images

def generate_html(image_paths, output_html):
    """Generates an interactive HTML flipbook from images."""
    template_str = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flipbook</title>
        <style>
            body {
                text-align: center;
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                overflow: hidden;
            }

            .zoom-container {
                width: 100%;
                height: 100vh;
                overflow: auto;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                padding-top: 20px;
            }

            .flipbook-container {
                position: relative;
                width: 800px;
                height: 900px;
                perspective: 2000px;
                transform-origin: center top;
                transition: transform 0.3s ease-in-out;
            }

            .page {
                position: absolute;
                width: 100%;
                height: 100%;
                background: white;
                border: 2px solid #ccc;
                transform-origin: left center;
                transition: transform 0.8s cubic-bezier(0.4, 0.2, 0.3, 1);
                backface-visibility: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }

            .page img {
                width: 100%;
                height: 100%;
                object-fit: contain;
            }

            .flipped {
                transform: rotateY(-180deg);
                box-shadow: -5px 5px 15px rgba(0, 0, 0, 0.3);
            }

            .controls {
                position: fixed;
                right: 20px;
                top: 50%;
                transform: translateY(-50%);
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .controls button {
                padding: 12px;
                font-size: 16px;
                cursor: pointer;
                border: none;
                background: #007bff;
                color: white;
                border-radius: 5px;
                transition: 0.2s;
            }

            .controls button:hover {
                background: #0056b3;
                transform: scale(1.1);
            }
        </style>
    </head>
    <body>
        <h2>Flipbook</h2>

        <div class="zoom-container" id="zoom-container">
            <div class="flipbook-container" id="flipbook">
                {% for image in images %}
                    <div class="page" data-index="{{ loop.index0 }}" data-zindex="{{ loop.revindex }}">
                        <img src="{{ image }}" alt="Page {{ loop.index }}">
                    </div>
                {% endfor %}
            </div>
        </div>

        <div class="controls">
            <button id="first">First Page</button>
            <button id="prev">Previous</button>
            <button id="next">Next</button>
            <button id="last">Last Page</button>
            <button id="zoom-in">Zoom In</button>
            <button id="zoom-out">Zoom Out</button>
        </div>

        <script>
            const pages = document.querySelectorAll(".page");
            pages.forEach(page => {
                const zIndex = page.getAttribute("data-zindex");
                page.style.zIndex = zIndex;
            });
            let currentPage = 0;
            let scale = 1;
            const flipbook = document.getElementById("flipbook");
            const zoomContainer = document.getElementById("zoom-container");

            function flipPage(forward) {
                if (forward && currentPage < pages.length - 1) {
                    pages[currentPage].style.zIndex = pages.length - currentPage;
                    pages[currentPage].classList.add("flipped");

                    setTimeout(() => {
                        currentPage++;
                    }, 800);
                } 
                else if (!forward && currentPage > 0) {
                    currentPage--;

                    setTimeout(() => {
                        pages[currentPage].classList.remove("flipped");
                        pages[currentPage].style.zIndex = pages.length - currentPage;
                    }, 10);
                }
            }

            document.getElementById("next").addEventListener("click", function() {
                flipPage(true);
            });

            document.getElementById("prev").addEventListener("click", function() {
                flipPage(false);
            });

            document.getElementById("first").addEventListener("click", function() {
                while (currentPage > 0) {
                    currentPage--;
                    pages[currentPage].classList.remove("flipped");
                    pages[currentPage].style.zIndex = pages.length - currentPage;
                }
            });

            document.getElementById("last").addEventListener("click", function() {
                while (currentPage < pages.length - 1) {
                    pages[currentPage].style.zIndex = pages.length - currentPage;
                    pages[currentPage].classList.add("flipped");
                    currentPage++;
                }
            });

            document.getElementById("zoom-in").addEventListener("click", function() {
                scale += 0.2;
                flipbook.style.transform = `scale(${scale})`;
                zoomContainer.style.overflowY = "auto";
                zoomContainer.scrollTop = 0;
            });

            document.getElementById("zoom-out").addEventListener("click", function() {
                if (scale > 1) {
                    scale -= 0.2;
                    flipbook.style.transform = `scale(${scale})`;
                }
                if (scale === 1) {
                    zoomContainer.style.overflowY = "hidden";
                }
            });
        </script>
    </body>
    </html>
    '''

    template = Template(template_str)
    html_content = template.render(images=image_paths)
    with open(output_html, "w") as f:
        f.write(html_content)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert a PDF to a self-contained HTML flipbook.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output", default="flipbook.html", help="Output HTML filename")
    args = parser.parse_args()

    images = convert_pdf_to_base64_images(args.pdf_path)
    generate_html(images, args.output)
    print(f"Flipbook generated! Open {args.output} in your browser.")



if __name__ == "__main__":
    main()

