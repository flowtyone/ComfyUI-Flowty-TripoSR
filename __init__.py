import sys
from os import path

sys.path.insert(0, path.dirname(__file__))
from folder_paths import get_filename_list, get_full_path, get_save_image_path, get_output_directory
from comfy.model_management import get_torch_device
from tsr.system import TSR
from PIL import Image
import numpy as np
import torch


def fill_background(image):
    image = np.array(image).astype(np.float32) / 255.0
    image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
    image = Image.fromarray((image * 255.0).astype(np.uint8))
    return image


class TripoSRModelLoader:
    def __init__(self):
        self.initialized_model = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (get_filename_list("checkpoints"),),
                "chunk_size": ("INT", {"default": 8192, "min": 1, "max": 10000})
            }
        }

    RETURN_TYPES = ("TRIPOSR_MODEL",)
    FUNCTION = "load"
    CATEGORY = "Flowty TripoSR"

    def load(self, model, chunk_size):
        device = get_torch_device()

        if not torch.cuda.is_available():
            device = "cpu"

        if not self.initialized_model:
            print("Loading TripoSR model")
            self.initialized_model = TSR.from_pretrained_custom(
                weight_path=get_full_path("checkpoints", model),
                config_path=path.join(path.dirname(__file__), "config.yaml")
            )
            self.initialized_model.renderer.set_chunk_size(chunk_size)
            self.initialized_model.to(device)

        return (self.initialized_model,)


class TripoSRSampler:

    def __init__(self):
        self.initialized_model = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("TRIPOSR_MODEL",),
                "reference_image": ("IMAGE",),
                "geometry_resolution": ("INT", {"default": 256, "min": 128, "max": 12288}),
                "threshold": ("FLOAT", {"default": 25.0, "min": 0.0, "step": 0.01}),
            },
            "optional": {
                "reference_mask": ("MASK",)
            }
        }

    RETURN_TYPES = ("MESH",)
    FUNCTION = "sample"
    CATEGORY = "Flowty TripoSR"

    def sample(self, model, reference_image, geometry_resolution, threshold, reference_mask=None):
        device = get_torch_device()

        if not torch.cuda.is_available():
            device = "cpu"

        image = reference_image[0]

        if reference_mask is not None:
            mask = reference_mask[0].unsqueeze(2)
            image = torch.cat((image, mask), dim=2).detach().cpu().numpy()
        else:
            image = image.detach().cpu().numpy()

        image = Image.fromarray(np.clip(255. * image, 0, 255).astype(np.uint8))
        if reference_mask is not None:
            image = fill_background(image)
        image = image.convert('RGB')
        scene_codes = model([image], device)
        meshes = model.extract_mesh(scene_codes, resolution=geometry_resolution, threshold=threshold)
        return ([meshes[0]],)


class TripoSRViewer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESH",)
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "display"
    CATEGORY = "Flowty TripoSR"

    def display(self, mesh):
        saved = list()
        full_output_folder, filename, counter, subfolder, filename_prefix = get_save_image_path("meshsave",
                                                                                                get_output_directory())

        for (batch_number, single_mesh) in enumerate(mesh):
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.obj"
            single_mesh.apply_transform(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]]))
            single_mesh.export(path.join(full_output_folder, file))
            saved.append({
                "filename": file,
                "type": "output",
                "subfolder": subfolder
            })

        return {"ui": {"mesh": saved}}


NODE_CLASS_MAPPINGS = {
    "TripoSRModelLoader": TripoSRModelLoader,
    "TripoSRSampler": TripoSRSampler,
    "TripoSRViewer": TripoSRViewer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TripoSRModelLoader": "TripoSR Model Loader",
    "TripoSRSampler": "TripoSR Sampler",
    "TripoSRViewer": "TripoSR Viewer"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
