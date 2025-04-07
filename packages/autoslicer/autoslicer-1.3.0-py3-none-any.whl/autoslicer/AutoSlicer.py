import os
import SimpleITK as sitk
import nibabel as nib
import numpy as np
import torch
from totalsegmentator.python_api import totalsegmentator
from totalsegmentator.nifti_ext_header import load_multilabel_nifti
import matplotlib.pyplot as plt
import vtk
import vtk.util.numpy_support as numpy_support
from scipy.ndimage import label
import pydicom
import glob

# Density map for each label (modifiable according to requirements)
DENSITY_MAP = {
    1: 1.05, 2: 1.06, 3: 1.06, 4: 1.02, 5: 1.05, 6: 1.04, 7: 1.04, 8: 1.04, 9: 1.04,
    10: 0.3, 11: 0.3, 12: 0.3, 13: 0.3, 14: 0.3, 15: 1.04, 16: 0.8, 17: 1.04, 18: 1.04,
    19: 1.04, 20: 1.04, 21: 1.05, 22: 1.04, 23: 1.01, 24: 1.01, 25: 1.9, 26: 1.9,
    27: 1.9, 28: 1.9, 29: 1.9, 30: 1.9, 31: 1.9, 32: 1.9, 33: 1.9, 34: 1.9, 35: 1.9,
    36: 1.9, 37: 1.9, 38: 1.9, 39: 1.9, 40: 1.9, 41: 1.9, 42: 1.9, 43: 1.9, 44: 1.9,
    45: 1.9, 46: 1.9, 47: 1.9, 48: 1.9, 49: 1.9, 50: 1.9, 51: 1.06, 52: 1.05, 53: 1.05,
    54: 1.05, 55: 1.05, 56: 1.05, 57: 1.05, 58: 1.05, 59: 1.05, 60: 1.05, 61: 1.06,
    62: 1.05, 63: 1.05, 64: 1.05, 65: 1.05, 66: 1.05, 67: 1.05, 68: 1.05, 69: 1.85,
    70: 1.85, 71: 1.85, 72: 1.85, 73: 1.85, 74: 1.85, 75: 1.85, 76: 1.85, 77: 1.85,
    78: 1.85, 79: 1.04, 80: 1.06, 81: 1.06, 82: 1.06, 83: 1.06, 84: 1.06, 85: 1.06,
    86: 1.06, 87: 1.06, 88: 1.06, 89: 1.06, 90: 1.04, 91: 1.9, 92: 1.85, 93: 1.85,
    94: 1.85, 95: 1.85, 96: 1.85, 97: 1.85, 98: 1.85, 99: 1.1, 100: 1.1, 101: 1.85,
    102: 1.85, 103: 1.85, 104: 1.85, 105: 1.85, 106: 1.85, 107: 1.85, 108: 1.85,
    109: 1.85, 110: 1.85, 111: 1.85, 112: 1.85, 113: 1.85, 114: 1.85, 115: 1.85,
    116: 1.85, 117: 1.8, 118: 1.0
}

class AutoSlicer:
    """
    AutoSlicer performs:
      1. DICOM to NIfTI conversion
      2. TotalSegmentator-based segmentation
      3. Adding a skin label in a given intensity range
      4. Computing mass, volume, inertia, center of mass
      5. Generating a VTK model file
      6. Visualizing the VTK (optional)
    """

    def __init__(self, workspace: str):
        """
        Initializes AutoSlicer with file paths and threshold defaults.

        Args:
            workspace (str): Name of the workspace directory.
        """
        # self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # self.workspace = os.path.join(self.current_dir, workspace)
        self.workspace = workspace
        self._ensure_directory(self.workspace)

        # Default intensity thresholds
        self.lower_ = -96.25
        self.upper_ = 153.46

        # File path configuration
        self.source_volume_path = os.path.join(self.workspace, "CT_Source_Volume.nii.gz")
        self.total_seg_result = os.path.join(self.workspace, "CT_TotalSegmentation.nii.gz")
        self.other_soft_tissue = os.path.join(self.workspace, "CT_SoftTissueLabel0.nii.gz")
        self.final_seg_result = os.path.join(self.workspace, "CT_SoftTissueLabel1.nii.gz")
        self.cropping = os.path.join(self.workspace, "CT_Cropping_seg.nii.gz")
        self.vtk_path = os.path.join(self.workspace, "CT_visualization.vtk")

        # The screenshot will be saved here
        self.output_image = os.path.join(self.workspace, "vtk_visualization.png")
        self.Inertia_parameters_file = os.path.join(self.workspace, "inertia_parameters.txt")
        self.voxel_size_value = [0,0,0]
        self.input_folder_path = None

    @staticmethod
    def _ensure_directory(path: str) -> None:
        os.makedirs(path, exist_ok=True)

    def set_density(self, label: int, value: float) -> None:
        if label in DENSITY_MAP:
            DENSITY_MAP[label] = value
        else:
            print(f"Label {label} not found in the density map. Skipping.")

    def set_threshold(self, lower_val: float, upper_val: float) -> None:
        self.lower_ = lower_val
        self.upper_ = upper_val

    # ----------------- NIfTI Creation ----------------- #
    # @staticmethod
    def _get_voxel_size(self,input_folder: str):
        try:
            reader = sitk.ImageSeriesReader()
            dicom_series = reader.GetGDCMSeriesIDs(input_folder)
            if not dicom_series:
                raise ValueError("No DICOM series found.")

            series_file_names = reader.GetGDCMSeriesFileNames(input_folder, dicom_series[0])
            reader.SetFileNames(series_file_names)
            image = reader.Execute()

            voxel_size = image.GetSpacing()
            self.voxel_size_value = voxel_size
            print(f"Voxel size (x, y, z): {voxel_size}")
            unit = "mm"
            print(f"Assumed unit: {unit}")
            return voxel_size, unit

        except Exception as e:
            print(f"Error reading voxel size: {e}")
            return None, None

    def _dicom_to_nifti(self, input_folder: str, output_path: str) -> None:
        try:
            reader = sitk.ImageSeriesReader()
            self._get_voxel_size(input_folder)

            dicom_series = reader.GetGDCMSeriesIDs(input_folder)
            if not dicom_series:
                raise ValueError("No DICOM series found.")

            print(f"Found {len(dicom_series)} DICOM series.")
            for series_id in dicom_series:
                series_file_names = reader.GetGDCMSeriesFileNames(input_folder, series_id)
                reader.SetFileNames(series_file_names)
                image = reader.Execute()
                sitk.WriteImage(image, output_path)
                print(f"Converted series {series_id} to {output_path}")

            print("All DICOM series converted successfully.")

        except Exception as e:
            print(f"Error during DICOM->NIfTI: {e}")

    def create_nifti(self, input_folder: str) -> None:
        self._dicom_to_nifti(input_folder, self.source_volume_path)

    # ----------------- Segmentation ----------------- #
    def _segment_image(self, input_image_path: str, output_path: str) -> None:
        device = "gpu" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        try:
            input_img = nib.load(input_image_path)
            print("Running TotalSegmentator...")
            output_img = totalsegmentator(
                input=input_img,
                task="total",
                ml=True,
                device=device
            )
            nib.save(output_img, output_path)
            print(f"Segmentation done. Saved to: {output_path}")
        except Exception as e:
            print(f"Error in segmentation: {e}")
            raise

    def _label_segmentation(self, seg_result_path: str, labeled_output_path: str) -> None:
        try:
            print("Loading segmentation with labels...")
            seg_nifti_img, label_map_dict = load_multilabel_nifti(seg_result_path)

            label_img = seg_nifti_img.get_fdata().astype(int)
            label_nifti = nib.Nifti1Image(label_img, seg_nifti_img.affine, seg_nifti_img.header)
            label_nifti.header["descrip"] = "Label Map for 3D Slicer"

            for label, description in label_map_dict.items():
                label_nifti.header.extensions.append(
                    nib.nifti1.Nifti1Extension(4, f"{label}: {description}".encode("utf-8"))
                )

            nib.save(label_nifti, labeled_output_path)
            print(f"Labeled segmentation saved to: {labeled_output_path}")
        except Exception as e:
            print(f"Error labeling segmentation: {e}")
            raise

    def create_segmentation(self) -> None:
        self._segment_image(self.source_volume_path, self.total_seg_result)
        self._label_segmentation(self.total_seg_result, self.other_soft_tissue)

    # ----------------- Skin Labeling ----------------- #
    @staticmethod
    def _load_nifti_file(file_path: str):
        nifti_img = nib.load(file_path)
        return nifti_img.get_fdata(), nifti_img.affine

    @staticmethod
    def _save_nifti_file(data: np.ndarray, affine: np.ndarray, file_path: str) -> None:
        new_nifti_img = nib.Nifti1Image(data, affine)
        nib.save(new_nifti_img, file_path)

    def _add_skin_label(self, src_volume: np.ndarray, seg_result: np.ndarray) -> np.ndarray:
        """
        Use self.lower_ and self.upper_ to define the intensity range for 'skin',
        then label it as 118 in the final segmentation array.
        """
        skin_candidate = (src_volume >= self.lower_) & (src_volume <= self.upper_)
        unlabeled_area = (seg_result == 0)
        skin_label_area = skin_candidate & unlabeled_area

        updated_seg = seg_result.copy()
        updated_seg[skin_label_area] = 118
        return updated_seg

    def create_soft_tissue_segmentation(self) -> None:
        seg_result, seg_affine = self._load_nifti_file(self.other_soft_tissue)
        source_volume, _ = self._load_nifti_file(self.source_volume_path)

        updated_seg = self._add_skin_label(source_volume, seg_result)
        self._save_nifti_file(updated_seg, seg_affine, self.final_seg_result)
        print(f"Updated segmentation saved: {self.final_seg_result}")

    # ----------------- Inertia + Center of Mass ----------------- #
    @staticmethod
    def _get_segmentation_labels(seg_file: str) -> list:
        nifti_img = nib.load(seg_file)
        seg_data = nifti_img.get_fdata()
        unique_labels = np.unique(seg_data)
        return [int(x) for x in unique_labels.tolist()]

    def _extract_patient_metadata(self, input_folder):

        try:
            dicom_files = glob.glob(os.path.join(input_folder, "*.dcm"))
            if not dicom_files:
                print("No DICOM files found in folder.")
                return {}

            ds = pydicom.dcmread(dicom_files[0], stop_before_pixels=True)

            return {
                "PatientID": getattr(ds, "PatientID", ""),
                "PatientSex": getattr(ds, "PatientSex", ""),
                "PatientAge": getattr(ds, "PatientAge", ""),
                "StudyInstanceUID": getattr(ds, "StudyInstanceUID", ""),
                "SeriesInstanceUID": getattr(ds, "SeriesInstanceUID", ""),
                "SOPInstanceUID": getattr(ds, "SOPInstanceUID", ""),
            }
        except Exception as e:
            print(f"Error extracting patient metadata: {e}")
            return {}
    def _calculate_inertia_parameters(self, seg_file: str) -> dict:
        """
        Calculates volume, mass, inertia, and center of mass across all labeled structures.
        NOTE: For an actual medical scenario, replace (1,1,1) with real voxel spacing if known.
        """
        voxel_size = (1, 1, 1)  # Modify if you know the real spacing
        voxel_size = self.voxel_size_value
        labels = self._get_segmentation_labels(seg_file)
        nifti_img = nib.load(seg_file)
        seg_data = nifti_img.get_fdata()

        # Convert 1 mm^3 to 0.001 cm^3
        voxel_vol_cm3 = (voxel_size[0] * voxel_size[1] * voxel_size[2]) / 1000.0

        total_mass = 0.0
        total_volume = 0.0
        total_inertia_tensor = np.zeros((3, 3))

        acc_mass_times_centroid = np.zeros(3)
        acc_mass = 0.0

        for label in labels:
            if label == 0:
                continue
            if label not in DENSITY_MAP:
                print(f"Warning: Label {label} not in density map. Skipping.")
                continue

            mask = (seg_data == label)
            num_voxels = mask.sum()
            if num_voxels == 0:
                continue

            density = DENSITY_MAP[label]
            volume = num_voxels * voxel_vol_cm3
            mass = (volume * density) / 1000.0  # convert volume from cm^3 to L, then multiply by density

            coords = np.array(np.where(mask)).T
            coords_mm = coords * voxel_size
            centroid = coords_mm.mean(axis=0)

            acc_mass_times_centroid += mass * centroid
            acc_mass += mass

            # For inertia, each voxel is the same mass = mass / num_voxels
            inertia_tensor = np.zeros((3, 3))
            for c in coords_mm:
                rel_pos = c - centroid
                x, y, z = rel_pos
                # Basic inertia formula
                inertia_tensor += np.array([
                    [y**2 + z**2, -x*y,       -x*z],
                    [-x*y,        x**2 + z**2, -y*z],
                    [-x*z,        -y*z,       x**2 + y**2]
                ]) * mass / num_voxels

            total_volume += volume
            total_mass += mass
            total_inertia_tensor += inertia_tensor

        if acc_mass > 0:
            global_com = acc_mass_times_centroid / acc_mass
        else:
            global_com = np.zeros(3)

        result = {
            "T1": {"name": "Volume", "value": total_volume, "unit": "cm³"},
            "T2": {"name": "Mass",   "value": total_mass,   "unit": "kg"},
            "T3": {"name": "Total Inertia Tensor", "value": total_inertia_tensor, "unit": "kg·mm²"},
            "T4": {"name": "Total Inertia Tensor", "value": total_inertia_tensor / 100.0, "unit": "kg·cm²"},
            "T5": {"name": "Center of Mass",       "value": global_com.tolist(),  "unit": "mm"}
        }
        with open(self.Inertia_parameters_file, "w", encoding="utf-8") as file:
            # Patient metadata
            patient_info = self._extract_patient_metadata(self.input_folder_path)
            file.write("Patient Metadata:\n")
            for key in ["PatientID", "PatientSex", "PatientAge", "StudyInstanceUID", "SeriesInstanceUID",
                        "SOPInstanceUID"]:
                value = patient_info.get(key, "")
                file.write(f"  {key}: {value}\n")
            file.write("\n")

            # Inertia parameters
            for key, value in result.items():
                file.write(f"{str(key)}:\n")
                file.write(f"  Name: {str(value['name'])}\n")
                file.write(f"  Value: {str(value['value'])}\n")
                file.write(f"  Unit: {str(value['unit'])}\n")
                file.write("\n")
        return result

    def get_VTK_file(self):
        """
        Generates a VTK file from the final segmentation, with a 'Density' array
        stored per label as a point data array in the polygon mesh.
        """
        seg_file = self.final_seg_result
        output_file_name = self.vtk_path

        seg_reader = vtk.vtkNIFTIImageReader()
        seg_reader.SetFileName(seg_file)
        seg_reader.Update()
        seg_image = seg_reader.GetOutput()

        seg_array = numpy_support.vtk_to_numpy(seg_image.GetPointData().GetScalars())
        unique_labels = np.unique(seg_array)

        density_lut = {}
        for label in unique_labels:
            if label == 0:
                continue
            density_lut[label] = DENSITY_MAP.get(int(label), 1.0)

        append_filter = vtk.vtkAppendPolyData()

        for label in unique_labels:
            if label == 0:
                continue

            thresh = vtk.vtkImageThreshold()
            thresh.SetInputData(seg_image)
            thresh.ThresholdBetween(label, label)
            thresh.SetInValue(1)
            thresh.SetOutValue(0)
            thresh.Update()

            cast_filter = vtk.vtkImageCast()
            cast_filter.SetInputConnection(thresh.GetOutputPort())
            cast_filter.SetOutputScalarTypeToUnsignedChar()
            cast_filter.Update()

            contour = vtk.vtkMarchingCubes()
            contour.SetInputConnection(cast_filter.GetOutputPort())
            contour.SetValue(0, 0.5)
            contour.Update()

            smooth = vtk.vtkSmoothPolyDataFilter()
            smooth.SetInputConnection(contour.GetOutputPort())
            smooth.SetNumberOfIterations(30)
            smooth.SetRelaxationFactor(0.1)
            smooth.FeatureEdgeSmoothingOff()
            smooth.BoundarySmoothingOn()
            smooth.Update()

            fill_holes = vtk.vtkFillHolesFilter()
            fill_holes.SetInputConnection(smooth.GetOutputPort())
            fill_holes.SetHoleSize(1000.0)
            fill_holes.Update()

            polydata = fill_holes.GetOutput()
            density = density_lut[label]

            density_array = vtk.vtkFloatArray()
            density_array.SetName("Density")
            density_array.SetNumberOfComponents(1)
            density_array.SetNumberOfTuples(polydata.GetNumberOfPoints())
            density_array.FillComponent(0, density)
            polydata.GetPointData().AddArray(density_array)

            append_filter.AddInputData(polydata)

        append_filter.Update()

        cleaner = vtk.vtkCleanPolyData()
        cleaner.SetInputConnection(append_filter.GetOutputPort())
        cleaner.Update()

        writer = vtk.vtkPolyDataWriter()
        writer.SetFileName(output_file_name)
        writer.SetInputConnection(cleaner.GetOutputPort())
        writer.Write()

    def calculate_inertia(self) -> dict:
        return self._calculate_inertia_parameters(self.final_seg_result)

    def run_automation(self, input_folder: str) -> dict:
        """
        One-click process:
          1. Convert DICOM -> NIfTI
          2. Perform segmentation
          3. Add skin label
          4. Compute inertia/center of mass
          5. Generate VTK file

        Returns a dict of computed volume, mass, inertia, and center of mass.
        """
        self.input_folder_path = input_folder

        self.create_nifti(input_folder)
        self.create_segmentation()
        self.create_soft_tissue_segmentation()

        # Further process of the data
        # remove medical devices
        self.keep_largest_component_only_target(118.0)
        # to make sure the C1 is cleaned
        self.keep_largest_component_only_target(50.0)
        self.keep_largest_component_only_target(90.0)
        self.keep_largest_component_only_target(91.0)
        # Cut head
        self.cut_below_plane_defined_by_points(offset=10)
        # remove the rest part of tissue
        self.crop_x_axis_by_target(self.final_seg_result,
                                   self.final_seg_result,
                                   target_label=91.0,
                                   offset=15)
        self.keep_largest_component_only_target(118.0)
        # remove other labels
        self.filter_segmentation_labels(self.final_seg_result,
                                        self.final_seg_result,
                                        [118.0,91.0,90.0])

        self.get_VTK_file()
        result = self.calculate_inertia()
        # self.save_segmentation_slices_as_images(output_prefix="CT_seg")

        # Cleanup temporary files if desired
        try:
            if os.path.exists(self.other_soft_tissue):
                os.remove(self.other_soft_tissue)
                print(f"Deleted temp file: {self.other_soft_tissue}")
            if os.path.exists(self.total_seg_result):
                os.remove(self.total_seg_result)
                print(f"Deleted temp file: {self.total_seg_result}")
        except Exception as e:
            print(f"Error deleting temp files: {e}")

        return result

    @staticmethod
    def center_crop_or_pad(image, center, output_size=(256, 256)):
        """
        Crop or pad a 2D image around a given center to a fixed output size.

        Args:
            image (np.ndarray): 2D input image (e.g., segmentation slice).
            center (tuple): (y, x) coordinates of the desired center.
            output_size (tuple): Desired output image size (height, width).

        Returns:
            np.ndarray: Centered, cropped/padded image.
        """
        H, W = image.shape
        out_h, out_w = output_size
        cy, cx = center

        # Define the bounding box
        y1 = int(cy - out_h // 2)
        y2 = y1 + out_h
        x1 = int(cx - out_w // 2)
        x2 = x1 + out_w

        # Create a blank output canvas
        output = np.zeros((out_h, out_w), dtype=image.dtype)

        # Determine valid source and destination regions
        src_y1 = max(y1, 0)
        src_y2 = min(y2, H)
        src_x1 = max(x1, 0)
        src_x2 = min(x2, W)

        dst_y1 = src_y1 - y1
        dst_y2 = dst_y1 + (src_y2 - src_y1)
        dst_x1 = src_x1 - x1
        dst_x2 = dst_x1 + (src_x2 - src_x1)

        output[dst_y1:dst_y2, dst_x1:dst_x2] = image[src_y1:src_y2, src_x1:src_x2]

        return output

    def save_segmentation_slices_as_images(self, output_prefix="slice", output_size=(256, 256)):
        """
        Save centered slices of the final segmentation in 3 orthogonal planes:
        axial (top-down), sagittal (left-right), and coronal (front-back).

        The saved PNG images will be centered on the region of interest and padded to output_size.
        """
        import matplotlib.pyplot as plt
        import numpy as np
        import os
        import nibabel as nib

        # Load segmentation
        seg = nib.load(self.final_seg_result)
        data = seg.get_fdata()

        # Get coordinates of foreground voxels
        coords = np.argwhere(data > 0)
        if coords.shape[0] == 0:
            print("No foreground labels found in segmentation.")
            return

        # Compute center of mass
        center_x = int(np.mean(coords[:, 0]))
        center_y = int(np.mean(coords[:, 1]))
        center_z = int(np.mean(coords[:, 2]))

        # Define output file paths
        paths = {
            "sagittal_left_right": os.path.join(self.workspace, f"{output_prefix}_sagittal_LR.png"),
            "coronal_front_back": os.path.join(self.workspace, f"{output_prefix}_coronal_FB.png"),
            "axial_top_bottom": os.path.join(self.workspace, f"{output_prefix}_axial_TB.png"),
        }

        # Extract slices
        sag = np.rot90(data[center_x, :, :])
        cor = np.rot90(data[:, center_y, :])
        axi = np.rot90(data[:, :, center_z])

        # Calculate center for each slice (2D)
        def get_slice_center(slice_2d):
            nonzero = np.argwhere(slice_2d > 0)
            if len(nonzero) == 0:
                return (slice_2d.shape[0] // 2, slice_2d.shape[1] // 2)
            return tuple(np.mean(nonzero, axis=0).astype(int)[::-1])  # (y, x)

        sag_center = get_slice_center(sag)
        cor_center = get_slice_center(cor)
        axi_center = get_slice_center(axi)

        # Center-crop or pad
        sag_cropped = self.center_crop_or_pad(sag, sag_center, output_size)
        cor_cropped = self.center_crop_or_pad(cor, cor_center, output_size)
        axi_cropped = self.center_crop_or_pad(axi, axi_center, output_size)

        # Save images using colorful colormap
        plt.imsave(paths["sagittal_left_right"], sag_cropped, cmap='nipy_spectral')
        plt.imsave(paths["coronal_front_back"], cor_cropped, cmap='nipy_spectral')
        plt.imsave(paths["axial_top_bottom"], axi_cropped, cmap='nipy_spectral')

        print("Centered segmentation preview images saved:")
        for name, path in paths.items():
            print(f"  {name}: {path}")

    def filter_segmentation_labels(self,input_path, output_path, target_labels):
        """
        Keep only the specified label values in a segmentation file.

        :param input_path: Path to the input .nii.gz segmentation file
        :param output_path: Path to save the filtered .nii.gz file
        :param target_labels: A list of label values to keep, e.g., [1, 3, 5]
        """
        # Load the segmentation image
        img = nib.load(input_path)
        data = img.get_fdata()

        # Create an empty array with the same shape
        filtered_data = np.zeros_like(data)

        # Copy over only the target labels
        for label in target_labels:
            filtered_data[data == label] = label

        # Save the filtered image
        filtered_img = nib.Nifti1Image(filtered_data, affine=img.affine, header=img.header)
        nib.save(filtered_img, output_path)

        print(f"Filtered segmentation saved to: {output_path}")

    def keep_largest_component_only_target(self, target_label):
        # Load the original segmentation file

        seg = nib.load(self.final_seg_result)
        data = seg.get_fdata()
        affine = seg.affine
        header = seg.header

        # Make a copy of the original data to preserve all other labels
        new_data = data.copy()

        # Create a binary mask for the target label
        mask = (data == target_label).astype(np.uint8)

        # Perform 3D connected component labeling
        labeled_array, num_features = label(mask)
        if num_features == 0:
            print(f"No connected components found for label {target_label}")
            return

        # Find the label of the largest connected component
        counts = np.bincount(labeled_array.flatten())
        counts[0] = 0  # Ignore background
        max_label = np.argmax(counts)

        # Create a mask that only includes the largest connected component
        cleaned_mask = (labeled_array == max_label)

        # Set all other voxels with the target label to background (0)
        new_data[(data == target_label) & (~cleaned_mask)] = 0

        # Save the cleaned segmentation to a new file
        new_seg = nib.Nifti1Image(new_data.astype(data.dtype), affine, header)
        nib.save(new_seg, self.final_seg_result)

        print(f"Kept only the largest connected component for label {target_label}, other labels preserved.")
        print(f"Cleaned segmentation saved to: {self.final_seg_result}")

    def crop_x_axis_by_target(self,input_path, output_path, target_label, offset=10):
        """
        Crop a NIfTI image along the X-axis based on a target label's left-right boundaries,
        and update the affine to preserve the original world-space position.

        Args:
            input_path (str): Path to the input .nii.gz file.
            output_path (str): Path to save the cropped .nii.gz file.
            target_label (int): Label value to locate along X-axis.
            offset (int): Number of voxels to expand the crop on both sides.
        """
        # Load image
        img = nib.load(input_path)
        data = img.get_fdata()
        affine = img.affine

        # Create a mask for the target label
        target_mask = (data == target_label)
        coords = np.argwhere(target_mask)

        if coords.shape[0] == 0:
            print(f"Target label {target_label} not found in image.")
            return

        # Get X-axis min and max
        x_min = np.min(coords[:, 0])
        x_max = np.max(coords[:, 0])

        # Apply offset
        x_min = max(x_min - offset, 0)
        x_max = min(x_max + offset, data.shape[0] - 1)

        # Crop data along X-axis
        cropped_data = data[x_min:x_max + 1, :, :]

        # Update affine to preserve spatial location
        new_affine = affine.copy()
        new_affine[:3, 3] += affine[:3, 0] * x_min

        # Save the cropped image
        cropped_img = nib.Nifti1Image(cropped_data, affine=new_affine, header=img.header)
        nib.save(cropped_img, output_path)

        print(f"Cropped image saved to: {output_path}")
        print(f"X range: {x_min} to {x_max} (with offset = {offset})")
    # estimate the Skin HU range
    def get_hu_from_dicom(self,input_folder):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(input_folder)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()

        image_np = sitk.GetArrayFromImage(image).astype(np.int16)
        hu_data = image_np

        return hu_data

    def estimate_skin_HU(self, input_folder, lower_q=5, upper_q=95):
        hu_volume = self.get_hu_from_dicom(input_folder=input_folder)

        valid = hu_volume[(hu_volume > -300) & (hu_volume < 400)]

        lower = np.percentile(valid, lower_q)
        upper = np.percentile(valid, upper_q)

        print(f"Estimated optimal skin HU range: {lower:.2f} to {upper:.2f}")
        return lower, upper

    @staticmethod
    def get_lowest_point(mask):
        """Get the lowest point (minimum z) in the largest connected component"""
        labeled_array, num_features = label(mask)
        if num_features == 0:
            return None
        counts = np.bincount(labeled_array.flatten())
        counts[0] = 0
        max_lbl = np.argmax(counts)
        coords = np.argwhere(labeled_array == max_lbl)
        min_z = np.min(coords[:, 2])
        lowest_points = coords[coords[:, 2] == min_z]
        return lowest_points[0]

    @staticmethod
    def get_highest_point(mask):
        """Get the highest point (maximum z) in the largest connected component"""
        labeled_array, num_features = label(mask)
        if num_features == 0:
            return None
        counts = np.bincount(labeled_array.flatten())
        counts[0] = 0
        max_lbl = np.argmax(counts)
        coords = np.argwhere(labeled_array == max_lbl)
        max_z = np.max(coords[:, 2])
        highest_points = coords[coords[:, 2] == max_z]
        return highest_points[0]

    def cut_below_plane_defined_by_points(self,
            target_label_base=50,
            target_label_slope1=50,
            target_label_slope2=91,
            axis='x',
            mode='keep_above',
            offset=5
    ):
        """
        Cut a volume below a slanted plane defined by two points and a base horizontal plane.

        The slanted plane is defined by the highest point of slope1 label and the lowest point of slope2 label.
        The base horizontal plane is defined by the lowest point of the base label.
        The cutting plane is defined by the intersection of the slanted and horizontal planes.

        :param file_path: Path to the NIfTI image
        :param target_label_base: Label used to define the base horizontal plane (lowest point)
        :param target_label_slope1: Label used to define the start point (highest) of the slanted plane
        :param target_label_slope2: Label used to define the end point (lowest) of the slanted plane
        :param output_path: Output path to save the result
        :param axis: 'x' or 'y', defining the direction of the slant
        :param mode: 'keep_above' or 'keep_below', whether to keep voxels above or below the cutting surface
        :param offset: z-axis offset added to make the slope steeper
        """
        # 1. Load image
        img = nib.load(self.final_seg_result)
        data = img.get_fdata()
        affine = img.affine
        axcodes = nib.aff2axcodes(affine)
        print(f"Axis directions (axcodes): {axcodes}")

        # 2. Extract key points
        base_point = self.get_lowest_point((data == target_label_base).astype(np.uint8))
        pt1 = self.get_highest_point((data == target_label_slope1).astype(np.uint8))  # Highest point
        pt2 = self.get_lowest_point((data == target_label_slope2).astype(np.uint8))  # Lowest point

        if base_point is None or pt1 is None or pt2 is None:
            print("Valid region not found for one or more labels.")
            return

        print(f"Lowest point of horizontal plane (from label {target_label_base}): {base_point}")
        print(f"Start point of slope (highest, from label {target_label_slope1}): {pt1}")
        print(f"End point of slope (lowest, from label {target_label_slope2}): {pt2}")

        base_z = base_point[2]
        pt2[2] = pt2[2] - offset  # Adjust for steeper slope

        # 3. Define slanted cutting surface z_cut(x, y)
        if axis == 'x':
            y1, z1 = pt1[1], pt1[2]
            y2, z2 = pt2[1], pt2[2]
            slope = (z2 - z1) / (y2 - y1 + 1e-6)
            y0 = y1
            get_z_cut = lambda x, y: slope * (y - y0) + z1
            print(f"Slope direction: y-z plane (perpendicular to x-axis), slope = {slope:.4f}")
        elif axis == 'y':
            x1, z1 = pt1[0], pt1[2]
            x2, z2 = pt2[0], pt2[2]
            slope = (z2 - z1) / (x2 - x1 + 1e-6)
            x0 = x1
            get_z_cut = lambda x, y: slope * (x - x0) + z1
            print(f"Slope direction: x-z plane (perpendicular to y-axis), slope = {slope:.4f}")
        else:
            raise ValueError("Parameter 'axis' must be either 'x' or 'y'")

        # 4. Perform voxel removal below/above the plane
        count_cut = 0
        for x in range(data.shape[0]):
            for y in range(data.shape[1]):
                z_cut = get_z_cut(x, y)
                z_threshold = min(base_z, z_cut)
                for z in range(data.shape[2]):
                    if mode == 'keep_above' and z < z_threshold:
                        data[x, y, z] = 0
                        count_cut += 1
                    elif mode == 'keep_below' and z > z_threshold:
                        data[x, y, z] = 0
                        count_cut += 1

        # 5. Save result
        print(f"Total voxels removed: {count_cut}")
        nib.save(nib.Nifti1Image(data, affine), self.final_seg_result)
        print(f"Clipping result saved to: {self.final_seg_result}")


# Helper methods for visualization
def _decimate_polydata(polydata, reduction=0.3):
    decimator = vtk.vtkDecimatePro()
    decimator.SetInputData(polydata)
    decimator.SetTargetReduction(reduction)
    decimator.PreserveTopologyOn()
    decimator.Update()
    return decimator.GetOutput()


def _transform_to_origin(polydata):
    bounds = polydata.GetBounds()  # (xmin, xmax, ymin, ymax, zmin, zmax)
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin

    transform = vtk.vtkTransform()
    transform.Translate(-xmin, -ymin, -zmin)

    tf_filter = vtk.vtkTransformPolyDataFilter()
    tf_filter.SetInputData(polydata)
    tf_filter.SetTransform(transform)
    tf_filter.Update()

    return tf_filter.GetOutput(), dx, dy, dz, transform


def _create_line_actor(pt1, pt2, color=(0.7, 0.7, 0.7), width=2.0):
    line_source = vtk.vtkLineSource()
    line_source.SetPoint1(pt1)
    line_source.SetPoint2(pt2)
    line_source.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(line_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetLineWidth(width)
    return actor

def visualize_with_coordinate_axes(original_com=None, decimate_ratio=0.0, vtk_set=None,output_image=None):
    """
    Reads the self.vtk_path VTK model and visualizes it with:
      1) Model aligned so that the bounding box min corner is at (0,0,0)
      2) vtkCubeAxesActor for annotated axes
      3) If original_com is provided, displays a sphere at the center of mass
         (plus lines projecting to x=0, y=0, and z=0)
      4) decimate_ratio can reduce the polygon count to speed up rendering
      5) A screenshot is saved to self.output_image, capturing the entire model
    """

    # ----------------- Read the VTK mesh ----------------- #
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtk_set)
    reader.Update()
    polydata = reader.GetOutput()

    # ----------------- Optional decimation ----------------- #
    if decimate_ratio > 0:
        polydata = _decimate_polydata(polydata, decimate_ratio)

    # ----------------- Translate geometry to origin ----------------- #
    transformed_polydata, dx, dy, dz, transform = _transform_to_origin(polydata)

    # ----------------- Create actor from polydata ----------------- #
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(transformed_polydata)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(0.2)  # Make main actor partially transparent

    # ----------------- Create renderer, add actor ----------------- #
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)  # dark background

    # ----------------- Add Cube Axes ----------------- #
    cube_axes = vtk.vtkCubeAxesActor()
    cube_axes.SetBounds(0, dx, 0, dy, 0, dz)
    cube_axes.SetCamera(renderer.GetActiveCamera())
    cube_axes.SetXTitle("X Axis (mm)")
    cube_axes.SetYTitle("Y Axis (mm)")
    cube_axes.SetZTitle("Z Axis (mm)")
    # Some VTK versions might require .SetFlyModeToStatic() or .SetFlyModeToStaticEdges()
    cube_axes.SetFlyModeToStaticEdges()
    for i in range(3):
        cube_axes.GetTitleTextProperty(i).SetColor(1, 1, 1)
        cube_axes.GetLabelTextProperty(i).SetColor(1, 1, 1)
    renderer.AddActor(cube_axes)

    # ----------------- Optionally add COM sphere + lines ----------------- #
    if original_com is not None:
        tx, ty, tz = transform.GetPosition()
        cx_new = original_com[0] + tx
        cy_new = original_com[1] + ty
        cz_new = original_com[2] + tz

        # 1) Create a bigger, brighter sphere at COM
        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetCenter(cx_new, cy_new, cz_new)
        sphere_source.SetRadius(10.0)  # e.g., 10.0 mm radius
        sphere_source.Update()

        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # bright red
        renderer.AddActor(sphere_actor)

        # 2) Create lines from COM to the bounding planes
        line_com_x = _create_line_actor(
            (cx_new, cy_new, cz_new),
            (0, cy_new, cz_new),
            color=(0.0, 1.0, 0.0),  # bright green
            width=3.0
        )
        line_com_y = _create_line_actor(
            (cx_new, cy_new, cz_new),
            (cx_new, 0, cz_new),
            color=(0.0, 1.0, 0.0),
            width=3.0
        )
        line_com_z = _create_line_actor(
            (cx_new, cy_new, cz_new),
            (cx_new, cy_new, 0),
            color=(0.0, 1.0, 0.0),
            width=3.0
        )
        renderer.AddActor(line_com_x)
        renderer.AddActor(line_com_y)
        renderer.AddActor(line_com_z)

        # 3) Add text overlay for COM
        text_actor = vtk.vtkTextActor()
        text_info = (
            f"Original COM: ({original_com[0]:.2f}, {original_com[1]:.2f}, {original_com[2]:.2f})\n"
            f"New COM: ({cx_new:.2f}, {cy_new:.2f}, {cz_new:.2f})"
        )
        text_actor.SetInput(text_info)
        text_actor.GetTextProperty().SetFontSize(18)
        text_actor.GetTextProperty().SetColor(1, 1, 1)
        text_actor.SetDisplayPosition(10, 10)
        renderer.AddActor2D(text_actor)

    # ----------------- Create a window + in
    # teractor ----------------- #
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(1024, 768)  # Larger window for a bigger screenshot
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # ----------------- Ensure entire model is in view ----------------- #
    renderer.ResetCamera()

    # ----------------- Render the scene first ----------------- #
    render_window.Render()
    if output_image != None:
        # ----------------- Take a screenshot ----------------- #
        window_to_image_filter = vtk.vtkWindowToImageFilter()
        window_to_image_filter.SetInput(render_window)
        window_to_image_filter.Update()

        png_writer = vtk.vtkPNGWriter()
        png_writer.SetFileName(output_image)
        png_writer.SetInputConnection(window_to_image_filter.GetOutputPort())
        png_writer.Write()
        print(f"Screenshot saved to: {output_image}")

    # ----------------- Start interactive window ----------------- #
    print("VTK window started. Press 'q' or close the window to exit.")
    interactor.Start()




if __name__ == "__main__":
    # test("D:\Curtin Hive Internship\T9\CT_SoftTissueLabel1.nii.gz",118.0, axis='x')

    # Example workspace and DICOM folder
    slicer = AutoSlicer("T2workspace")
    dicom_folder = r"D:\Healthy-Total-Body-CTs-002\06-19-2002-NA-CTSoft512x512 3hr-23072\head"
    #
    results = slicer.run_automation(dicom_folder)
    print("Final results:", results)
    #
    # # 2) Visualize with COM (if it exists in results)
    # com = results["T4"]["value"]  # center of mass from pipeline
    # com = [253.64205539346176, 304.00651615735956, 107.49544928350699]
    # visualize_with_coordinate_axes(original_com=com, decimate_ratio=0.3, vtk_set="D:\Curtin Hive Internship\T4workspace\CT_visualization.vtk")