import base64
import binascii
import io
from typing import Any, Dict, List

import requests
from PIL import Image, UnidentifiedImageError


def convert_to_unsloth(
    messages_input: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Converts a list of messages from an OpenAI-like chat format to the Nebulous conversation format.
    Images specified by URLs or base64 strings are loaded into PIL.Image objects.

    Input format example:
    [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Describe the image."},
                {"type": "input_image", "image_url": "http://... or base64 string"},
            ]
        },
        {
            "role": "assistant",
            "content": [{"type": "text", "text": "This is an image of..."}] # Or potentially just a string
        }
    ]

    Output format example:
    {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the image."},
                    {"type": "image", "image": <PIL.Image.Image object>},
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "This is an image of..."}]
            }
        ]
    }
    """
    nebu_conversation = []
    for message in messages_input:
        role = message.get("role")
        input_content = message.get("content")  # Can be list or string

        processed_content = []

        if isinstance(input_content, list):
            # Process list content (multi-modal)
            for item in input_content:
                item_type = item.get("type")
                if item_type in ("input_text", "text"):
                    processed_content.append(
                        {"type": "text", "text": item.get("text", "")}
                    )
                elif item_type in (
                    "input_image",
                    "image_url",
                    "image",
                ):  # Accept 'image' as source key too
                    # Use "image_url" first, then fallback to "image" if needed
                    image_source = item.get("image_url", item.get("image"))
                    if image_source:
                        pil_image = None
                        try:
                            if isinstance(
                                image_source, str
                            ) and image_source.startswith(("http://", "https://")):
                                # Handle URL
                                response = requests.get(image_source, stream=True)
                                response.raise_for_status()  # Raise an exception for bad status codes
                                pil_image = Image.open(response.raw)
                            elif isinstance(image_source, str):
                                # Handle base64 string
                                # Remove potential data URI prefix (e.g., "data:image/png;base64,")
                                if "," in image_source:
                                    image_source = image_source.split(",", 1)[1]
                                image_bytes = base64.b64decode(image_source)
                                pil_image = Image.open(io.BytesIO(image_bytes))

                            elif isinstance(image_source, Image.Image):
                                # Handle direct PIL.Image input
                                pil_image = image_source

                            if pil_image:
                                processed_content.append(
                                    {"type": "image", "image": pil_image}
                                )
                            else:
                                print(
                                    f"Warning: Could not load image from source: {type(image_source)}"
                                )

                        except requests.exceptions.RequestException as e:
                            print(
                                f"Warning: Failed to fetch image from URL {image_source}: {e}"
                            )
                        except (binascii.Error, ValueError) as e:
                            print(f"Warning: Failed to decode base64 image string: {e}")
                        except (IOError, UnidentifiedImageError) as e:
                            print(f"Warning: Failed to open image: {e}")
                        except Exception as e:
                            print(
                                f"Warning: An unexpected error occurred while processing image: {e}"
                            )

                    else:
                        print(
                            "Warning: Image item provided but 'image_url' or 'image' key is missing or empty."
                        )

                # Add handling for other potential input types if necessary
        elif isinstance(input_content, str):
            # Handle simple string content (common for assistant messages)
            processed_content.append({"type": "text", "text": input_content})
        # else: Handle unexpected content format (e.g., log warning, skip message)

        if role and processed_content:
            nebu_conversation.append({"role": role, "content": processed_content})
        # else: Handle missing role or empty content if needed

    return {"messages": nebu_conversation}
