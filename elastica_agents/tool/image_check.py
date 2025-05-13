import os
import requests
import io
from mcp.server.fastmcp import Context, Image, FastMCP
from PIL import Image as PILImage


def load_image(image_path: str) -> Image:
    """
    Load an image from the filesystem and return in mcp image format.

    Args:
        image_path: The path to the image to load.
    """
    img = PILImage.open(image_path)
    return Image(data=img.tobytes(), format="jpeg")


# class ReverseImageSearchTool(Tool):
#     """
#     A tool that takes an image and queries an online reverse image search API
#     to find visually similar results.
#     """
#
#     name = "reverse_image_search"
#     description = (
#         "Upload an image to a reverse image search service (e.g., Bing Image Search API) "
#         "and return URLs of visually similar images and brief descriptions."
#     )
#
#     def _prepare_image_bytes(self, image: Image.Image) -> bytes:
#         buffer = io.BytesIO()
#         image.save(buffer, format="JPEG")
#         return buffer.getvalue()
#
#     def run(self, ctx: Context, image: ImageInput) -> str:
#         # Extract PIL Image from the ImageInput
#         img: Image.Image = image.open()
#         img_bytes = self._prepare_image_bytes(img)
#
#         # Configure the API endpoint and key
#         subscription_key = os.getenv("BING_IMAGE_SEARCH_KEY")
#         if not subscription_key:
#             return "Error: BING_IMAGE_SEARCH_KEY not set in environment variables."
#
#         search_url = "https://api.bing.microsoft.com/v7.0/images/visualsearch"
#         headers = {"Ocp-Apim-Subscription-Key": subscription_key}
#         files = {"image": ("image.jpg", img_bytes, "image/jpeg")}
#
#         # Perform the POST request
#         response = requests.post(search_url, headers=headers, files=files)
#         response.raise_for_status()
#         data = response.json()
#
#         # Parse the results
#         results = []
#         tags = data.get("tags", [])
#         for tag in tags:
#             for v in tag.get("actions", []):
#                 if v.get("actionType") == "VisualSearch":
#                     for img_info in v.get("data", {}).get("value", []):
#                         name = img_info.get("name")
#                         content_url = img_info.get("contentUrl")
#                         host_page = img_info.get("hostPageDisplayUrl")
#                         results.append(f"{name}: {content_url} (from {host_page})")
#
#         if not results:
#             return "No visually similar images found."
#         return "\n".join(results)
#
#
# # Instantiate agent with the tool
# tools = [ReverseImageSearchTool()]
# agent = Agent(tools=tools)
#
# if __name__ == "__main__":
#     # Example usage:
#     # Ensure you have set BING_IMAGE_SEARCH_KEY in your environment
#     from PIL import Image
#
#     img = Image.open("./query.jpg")  # Replace with your image path
#     result = agent.run("Find visually similar images online.", image=img)
#     print(result)
#
