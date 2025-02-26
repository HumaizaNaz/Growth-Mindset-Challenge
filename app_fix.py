# # First, let's check what's causing the error and how to fix it
# import sys
# print(f"Python version: {sys.version}")

# # Check if matplotlib is installed
# try:
#     import matplotlib
#     print(f"Matplotlib is installed (version: {matplotlib.__version__})")
# except ImportError:
#     print("Matplotlib is NOT installed")

# # Check if other required packages are installed
# required_packages = ["streamlit", "pandas", "numpy", "pillow"]
# for package in required_packages:
#     try:
#         module = __import__(package)
#         if hasattr(module, "__version__"):
#             print(f"{package} is installed (version: {module.__version__})")
#         else:
#             print(f"{package} is installed (version unknown)")
#     except ImportError:
#         print(f"{package} is NOT installed")

# # Solution
# print("\n--- SOLUTION ---")
# print("To fix the ModuleNotFoundError for matplotlib, you need to install it:")
# print("Run this command in your terminal:")
# print("pip install matplotlib")
# print("\nIf you're using a virtual environment or conda, make sure to activate it first.")
# print("\nIf you're deploying on Streamlit Cloud, add matplotlib to your requirements.txt file:")
# print("matplotlib>=3.5.0")