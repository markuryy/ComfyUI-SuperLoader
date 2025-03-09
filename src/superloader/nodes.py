import os.path
from nodes import LoraLoader
import folder_paths


def extract_base_filename(lora_name):
    """Extract the base filename without extension and path."""
    # Get just the filename without the path
    filename = os.path.basename(lora_name)
    # Remove the extension if it's .safetensors
    if filename.endswith('.safetensors'):
        filename = filename[:-12]
    return filename


class LoRAMetadata(LoraLoader):
    """
    Loads a LoRA and provides the filename as a string output.
    Model and clip inputs are optional - you can skip either or both to not apply the LoRA to those components.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        parent_inputs = super().INPUT_TYPES()
        
        # Create a new input structure
        inputs = {"required": {}, "optional": {}}
        
        # Move model and clip to optional
        if "model" in parent_inputs["required"]:
            inputs["optional"]["model"] = parent_inputs["required"]["model"]
        if "clip" in parent_inputs["required"]:
            inputs["optional"]["clip"] = parent_inputs["required"]["clip"]
        
        # Keep other required inputs
        for k, v in parent_inputs["required"].items():
            if k not in ["model", "clip"]:
                inputs["required"][k] = v
        
        # Add any existing optional inputs
        if "optional" in parent_inputs:
            for k, v in parent_inputs["optional"].items():
                inputs["optional"][k] = v
                
        return inputs
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("model", "clip", "filename")
    FUNCTION = "load_lora_with_metadata"
    CATEGORY = "loaders"
    DESCRIPTION = "Loads a LoRA and provides the filename as a string output. Model and clip inputs are optional."
    
    def load_lora_with_metadata(self, lora_name, strength_model, strength_clip, model=None, clip=None):
        # Extract the base filename
        filename = extract_base_filename(lora_name)
        
        # If both model and clip are None, just return the filename
        if model is None and clip is None:
            return (None, None, filename)
        
        # If only one is provided, call parent method with the provided input
        if model is not None and clip is None:
            model_lora, _ = self.load_lora(model, None, lora_name, strength_model, 0)
            return (model_lora, None, filename)
        
        if model is None and clip is not None:
            _, clip_lora = self.load_lora(None, clip, lora_name, 0, strength_clip)
            return (None, clip_lora, filename)
        
        # If both are provided, normal operation
        model_lora, clip_lora = self.load_lora(model, clip, lora_name, strength_model, strength_clip)
        return (model_lora, clip_lora, filename)


class StringDisplay:
    """
    A simple node that displays a string input.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "unique_id")
    FUNCTION = "display_string"
    CATEGORY = "utils"
    DESCRIPTION = "Displays a string input within the node."
    OUTPUT_NODE = True
    
    def display_string(self, text, prompt=None, extra_pnginfo=None, unique_id=None):
        return {
            "ui": {
                "text": (text,)
            },
            "result": (text, unique_id)
        }


class StringDisplayMultiline:
    """
    A simple node that displays a multiline string input.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO", "unique_id": "UNIQUE_ID"},
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "unique_id")
    FUNCTION = "display_string"
    CATEGORY = "utils"
    DESCRIPTION = "Displays a multiline string input within the node."
    OUTPUT_NODE = True
    
    def display_string(self, text, prompt=None, extra_pnginfo=None, unique_id=None):
        return {
            "ui": {
                "text": (text,)
            },
            "result": (text, unique_id)
        }


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoRA Metadata": LoRAMetadata,
    "Display String": StringDisplay,
    "Display String Multiline": StringDisplayMultiline
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoRA Metadata": "🐈‍⬛ LoRA Metadata",
    "Display String": "🐈‍⬛ Display String",
    "Display String Multiline": "🐈‍⬛ Display String Multiline"
}
