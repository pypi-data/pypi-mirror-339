from gpt4all import GPT4All
model = GPT4All(r"C:\Users\lucas\aait_store\Models\NLP\Qwen2.5-Dyanka-7B-Preview.Q6_K.gguf",
                model_path=r"C:\Users\lucas\aait_store\Models\NLP\Qwen2.5-Dyanka-7B-Preview.Q6_K.gguf",
                n_ctx=32000, device="cuda", allow_download=False) # downloads / loads a 4.66GB LLM
# Start a chat session
with model.chat_session():
    print("🤖 Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        response = model.generate(user_input, max_tokens=512)  # Adjust max_tokens as needed
        print("AI:", response)







# import psutil
#
# for proc in psutil.process_iter(["pid", "name", "cmdline", "create_time", "memory_info", "ppid"]):
#     if proc.info["name"] == "python.exe" or proc.info["name"] == "python":
#         print(f"PID: {proc.info['pid']}")
#         print(f"Status: {proc.info}")
#         print(f"Name: {proc.info['name']}")
#         print(f"Command: {proc.info['cmdline']}")
#         print(f"Parent PID: {proc.info['ppid']}")  # Useful if a known process started it
#         print(f"Start Time: {psutil.Process(proc.info['pid']).create_time()}")  # When it started
#         print(f"Memory Usage: {proc.info['memory_info'].rss / 1024**2:.2f} MB")  # RAM used
#         print("-" * 50)
# #
# #
# import psutil
# import os
# import signal
#
# # Find all Orange.canvas processes
# orange_processes = []
#
# for proc in psutil.process_iter(["pid", "name", "cmdline", "create_time"]):
#     if "python" in proc.info["name"] and "-m" in proc.info["cmdline"] and "Orange.canvas" in proc.info["cmdline"]:
#         orange_processes.append(proc)
#
# # Only kill the oldest one if there's more than one
# if len(orange_processes) > 1:
#     oldest_process = min(orange_processes, key=lambda p: p.info["create_time"])
#     print(f"Killing oldest Orange.canvas process: PID {oldest_process.info['pid']}, started at {oldest_process.info['create_time']}")
#     os.kill(oldest_process.info["pid"], signal.SIGTERM)  # Try a safe kill
# else:
#     print("Only one Orange.canvas process found, nothing to kill.")






# import glob
# import os
# import ntpath
# import fitz  # PyMuPDF
# from paddleocr import PaddleOCR
# from PIL import Image
# import numpy as np
#
#
#
# def highlight_material_bbox(pdf_path, output_pdf_path, output_png_path):
#     # Open the PDF
#     doc = fitz.open(pdf_path)
#
#     # Iterate through each page
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#
#         # Search for the word "MATIERE/MATERIAL" in the page
#         text_instances = page.search_for("MATERIAL")
#
#         # Iterate through found instances
#         for bbox in text_instances:
#             width = bbox[2] - bbox[0]
#             height = bbox[3] - bbox[1]
#
#             # Modify bbox coordinates as per the original request
#             bbox[0] = bbox[0] - 1.2 * width
#             bbox[1] = bbox[1] - 10 * height
#             bbox[2] = bbox[2] + 10 * width
#             bbox[3] = bbox[3] + 23 * height
#
#             print("height:", height)
#             print("width:", width)
#             print("Modified bbox:", bbox)
#
#             # Extract the selected bbox area and save it as a PNG without drawing the red rectangle
#             matrix = fitz.Matrix(2, 2)  # Adjust this for higher resolution (2x scaling)
#             pix = page.get_pixmap(matrix=matrix, clip=bbox)  # Extract the region inside the bbox
#             pix.save(output_png_path)  # Save the cropped region as PNG in the highest quality possible
#
#             # Draw a rectangle around the bbox in the PDF
#             page.draw_rect(bbox, color=(1, 0, 0), width=2)  # Red rectangle with width=2
#
#         break  # Remove this if you want to process all pages, not just the first one
#
#     # Save the modified PDF to a new file
#     doc.save(output_pdf_path)
#
#
# folder_path = r"C:\Users\lucas\Desktop\folder"  # Change this to your folder path
# pdf_files = [os.path.abspath(f) for f in glob.glob(os.path.join(folder_path, "*.pdf"))]
#
# for pdf_file in pdf_files:
#     pdf_name = ntpath.basename(pdf_file)
#     output_pdf_path = os.path.join(r"C:\Users\lucas\Desktop\folder2", pdf_name)
#     output_png_path = output_pdf_path.replace(".pdf", ".png")
#     highlight_material_bbox(pdf_file, output_pdf_path, output_png_path)
#
#     # Initialize PaddleOCR
#     ocr = PaddleOCR(
#         use_angle_cls=True,
#         lang="fr",
#         det_model_dir=r"C:\Users\lucas\.paddleocr\whl\det",  # Detection model
#         rec_model_dir=r"C:\Users\lucas\.paddleocr\whl\rec",  # Recognition model
#         cls_model_dir=r"C:\Users\lucas\.paddleocr\whl\cls"  # Classification model (optional)
#     )
#
#     # Get the image
#     img = Image.open(output_png_path)
#
#     # Convert PIL Image to NumPy array (RGB format)
#     img_np = np.array(img)
#
#     # Run OCR on an image
#     result = ocr.ocr(img_np, cls=True)
#
#     for res in result:
#         print(res)
#         for line in res:
#             print(line[-1])



# from paddleocr import PaddleOCR
# import fitz  # PyMuPDF
# from paddleocr import PaddleOCR
# from PIL import Image
# import numpy as np
# import io
#
# # Initialize PaddleOCR
# ocr = PaddleOCR(use_angle_cls=True, lang="fr")
#
# # Open the PDF
# # doc = fitz.open(pdf_path)
#
# # Process the first page
# # page = doc[0]
#
# # Convert page to image
# # pix = page.get_pixmap(dpi=300)  # Higher DPI for better OCR
# img = Image.open(output_png_path)
#
# # Convert PIL Image to NumPy array (RGB format)
# img_np = np.array(img)
#
#
# # Run OCR on an image
# result = ocr.ocr(img_path, cls=True)
#
#
# for res in result:
#     print(res)
#     for line in res:
#         print(line[-1])
# bla
# # # Extract text safely
# # for line in result[0]:
# #     for word in line:
# #         if isinstance(word[1], (list, tuple)) and len(word[1]) > 0:
# #             print(word[1][0])  # Extracted text
