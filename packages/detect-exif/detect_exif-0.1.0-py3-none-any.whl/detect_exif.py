"""EXIF Cleaning Tools."""

import io
import sys
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

SUPPORTED_EXTENSIONS = {".png", ".jpeg", ".jpg", ".webp"}

# Special tags to explicitly check for (for reporting purposes)
SPECIAL_CHECK_TAGS = {
    # Device information
    0x010F: "Camera Make",
    0x0110: "Camera Model",
    0x0131: "Software/Firmware",
    0xA433: "Lens Make",
    0xA434: "Lens Model",
    # GPS-related tags
    0x8825: "GPS Info Block",  # Main GPS info block
    0x0001: "GPS Latitude Ref",
    0x0002: "GPS Latitude",
    0x0003: "GPS Longitude Ref",
    0x0004: "GPS Longitude",
    0x0005: "GPS Altitude Ref",
    0x0006: "GPS Altitude",
    0x001D: "GPS Date Stamp",
    0x001B: "GPS Processing Method",
    # Time/Date (can reveal location via timezone)
    0x9003: "Date/Time Original",
    0x9004: "Date/Time Digitized",
    0x0132: "Modify Date/Time",
}

# Human-readable names for EXIF tags (for reporting)
EXIF_TAG_NAMES = {
    0x0100: "Image Width",
    0x0101: "Image Height",
    0x0102: "Bits Per Sample",
    0x0103: "Compression",
    0x0106: "Photometric Interpretation",
    0x0112: "Orientation",
    0x011C: "Planar Configuration",
    0x0128: "Resolution Unit",
    0x011A: "X Resolution",
    0x011B: "Y Resolution",
    0x0115: "Samples Per Pixel",
    0xA001: "Color Space",
    0xA002: "Exif Image Width",
    0xA003: "Exif Image Height",
    0x829A: "Exposure Time",
    0x829D: "F Number",
    0x8827: "ISO Speed",
    0x9202: "Aperture Value",
    0x9203: "Brightness Value",
    0x9204: "Exposure Bias",
    0x9205: "Max Aperture Value",
    0x9207: "Metering Mode",
    0x920B: "Flash Energy",
    0x920A: "Focal Length",
    0xA402: "Exposure Mode",
    0xA403: "White Balance",
    0xA404: "Digital Zoom Ratio",
    0xA405: "Focal Length (35mm)",
    0xA406: "Scene Capture Type",
    0xA407: "Gain Control",
    0xA408: "Contrast",
    0xA409: "Saturation",
    0xA40A: "Sharpness",
    0xA40C: "Subject Distance Range",
    # Special check tags (merge with the dictionary)
    **SPECIAL_CHECK_TAGS,
    # Other common sensitive tags
    0x013B: "Artist/Author",
    0x8298: "Copyright",
    0x9286: "User Comments",
    0xA430: "Camera Owner",
    0xA431: "Camera Serial Number",
    0x9211: "Image Unique ID",
    0x927C: "Maker Notes",
    0x02BC: "XMP Metadata",
}


def get_gps_info(exif_data):
    """
    Extract human-readable GPS information from EXIF data if present.

    Parameters
    ----------
    exif_data : PIL.Image._getexif
        The full EXIF data

    Returns
    -------
    str or None
        Human-readable GPS information or None if not found
    """
    if not exif_data:
        return None

    # Check for GPSInfo tag
    gps_info = None
    if 0x8825 in exif_data:
        gps_data = exif_data[0x8825]
        if not isinstance(gps_data, dict):
            return "GPS data present but unreadable"

        # Extract latitude
        if 2 in gps_data and 1 in gps_data:
            lat = gps_data[2]
            lat_ref = gps_data[1]
            if isinstance(lat, tuple) and len(lat) == 3:
                try:
                    lat_value = lat[0] + lat[1] / 60 + lat[2] / 3600
                    if lat_ref == "S":
                        lat_value = -lat_value
                    gps_info = f"Lat: {lat_value:.6f}"
                except (TypeError, ZeroDivisionError):
                    gps_info = "Latitude present but unreadable"

        # Extract longitude
        if 4 in gps_data and 3 in gps_data:
            lon = gps_data[4]
            lon_ref = gps_data[3]
            if isinstance(lon, tuple) and len(lon) == 3:
                try:
                    lon_value = lon[0] + lon[1] / 60 + lon[2] / 3600
                    if lon_ref == "W":
                        lon_value = -lon_value
                    gps_info = f"{gps_info or ''} Lon: {lon_value:.6f}".strip()
                except (TypeError, ZeroDivisionError):
                    gps_info = (
                        f"{gps_info or ''} Longitude present but unreadable".strip()
                    )

        # If we couldn't parse specific values but GPS data exists
        if not gps_info and gps_data:
            return "GPS data present"

    return gps_info


def is_unsafe_exif(img):
    """
    Check if the image has any non-technical EXIF data that could be private.

    Instead of using a whitelist approach, we'll assume all EXIF is unsafe
    except for purely technical image parameters.

    Parameters
    ----------
    img : PIL.Image.Image
        The image object to check for sensitive EXIF data.

    Returns
    -------
    tuple
        (bool, dict) where:
        - bool is True if sensitive EXIF data was found
        - dict contains special info (camera, GPS, etc.) for reporting
    """
    if not hasattr(img, "getexif"):
        return False, {}

    exif_data = img.getexif()
    if not exif_data:
        return False, {}

    # Check if the image has any EXIF data at all (except orientation)
    has_exif = False
    for tag_id in exif_data:
        # Skip orientation tag as that's purely technical
        if tag_id != 0x0112 and exif_data[tag_id]:
            has_exif = True
            break

    if not has_exif:
        return False, {}

    # Get the full EXIF data for deeper checks
    full_exif = None
    if hasattr(img, "_getexif"):
        full_exif = img._getexif() or {}
    else:
        full_exif = exif_data

    # Collect information for reporting
    special_info = {}

    # Check for special tags we want to highlight
    for tag_id, tag_name in SPECIAL_CHECK_TAGS.items():
        if tag_id in full_exif and full_exif[tag_id]:
            special_info[tag_name] = full_exif[tag_id]

    # Special check for GPS information
    gps_info = get_gps_info(full_exif)
    if gps_info:
        special_info["GPS Coordinates"] = gps_info

    # Special check for device information as a group
    if 0x010F in full_exif or 0x0110 in full_exif:
        make = full_exif.get(0x010F, "")
        model = full_exif.get(0x0110, "")
        if make or model:
            special_info["Camera"] = f"{make} {model}".strip()

    # Special check for software/firmware
    if 0x0131 in full_exif:
        special_info["Software"] = full_exif[0x0131]

    # Check for embedded thumbnail
    if 0x0201 in full_exif:  # JPEGInterchangeFormat tag
        special_info["Embedded Thumbnail"] = "Present"

    # Check for XMP metadata
    if hasattr(img, "info") and "XML:com.adobe.xmp" in img.info:
        special_info["XMP Metadata"] = "Present"

    return True, special_info


def sanitize_image(img):
    """
    Sanitize image by removing all EXIF data while preserving orientation.

    Parameters
    ----------
    img : PIL.Image.Image
        The image to sanitize

    Returns
    -------
    PIL.Image.Image
        New image with all EXIF data removed
    """
    # First, apply any orientation from EXIF
    img = ImageOps.exif_transpose(img)

    # Create a new image without any EXIF data
    img_format = img.format or "JPEG"
    with io.BytesIO() as buffer:
        img.save(buffer, format=img_format)
        buffer.seek(0)
        cleaned_img = Image.open(buffer)
        cleaned_img.load()  # Important to load the image data

    return cleaned_img


def process_files(files, remove=False, quiet=False):
    """
    Process image files to check for and optionally remove EXIF data.

    Parameters
    ----------
    files : list of str
        List of file paths to process.
    remove : bool, optional
        Whether to remove EXIF data from images, by default False.
    quiet : bool, optional
        Whether to minimize output, by default False.

    Returns
    -------
    int
        Exit code. Returns 1 if any unsafe EXIF data was found (to block commits),
        0 if no unsafe EXIF data was found or all EXIF data was successfully removed.
    """
    unsupported_files = []
    unsafe_exif_found = False
    sensitive_files = []

    for file_str in files:
        file_path = Path(file_str)

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            unsupported_files.append(file_path)
            continue

        try:
            original = Image.open(file_path)
            has_unsafe, special_info = is_unsafe_exif(original)

            if has_unsafe:
                unsafe_exif_found = True
                sensitive_files.append(file_path)

                if not quiet:
                    print(f"Sensitive EXIF data found in: {file_path}")

                    # Print the special highlighted information if available
                    if special_info:
                        print("  ⚠️ SENSITIVE INFORMATION DETECTED:")
                        for info_name, info_value in special_info.items():
                            # Format the value for display
                            if isinstance(info_value, str) and len(info_value) > 50:
                                info_value = info_value[:47] + "..."
                            elif isinstance(info_value, bytes):
                                info_value = f"Binary data ({len(info_value)} bytes)"
                            print(f"  • {info_name}: {info_value}")

                if remove:
                    # Remove all EXIF data while preserving orientation
                    cleaned_img = sanitize_image(original)

                    # Save without any EXIF data
                    img_format = original.format or "JPEG"
                    cleaned_img.save(file_path, format=img_format)

                    if not quiet:
                        print(f"  ✓ Removed all EXIF data from: {file_path}")

        except UnidentifiedImageError:
            unsupported_files.append(file_path)
        except OSError as e:
            if not quiet:
                print(f"ERROR: Problem reading image file {file_path}: {e}")
            unsupported_files.append(file_path)

    # Summarize the results
    if not quiet:
        if unsupported_files:
            print("\nWARNING: The following files could not be checked for EXIF data:")
            for file in unsupported_files:
                print(f"  - {file}")

    # Even in quiet mode, we want to show a summary of findings
    if unsafe_exif_found:
        if quiet:
            print(f"Found sensitive EXIF data in {len(sensitive_files)} file(s).")
            if not remove:
                print("Run with --remove to clean files or use --verbose for details.")
            else:
                print("EXIF data was cleaned.")
        return 1  # Return error code to block the commit if unsafe EXIF data found
    return 0


def main():
    """
    Parse command line arguments and processes specified image files.

    Returns
    -------
    int
        Exit code from process_files. Returns 1 if any unsafe EXIF data was found,
        0 if all EXIF data was successfully sanitized.
    """
    # Parse arguments
    remove = "--remove" in sys.argv
    quiet = "--quiet" in sys.argv
    verbose = "--verbose" in sys.argv

    # Quiet mode is disabled if verbose is specified
    if verbose:
        quiet = False

    # Get the list of files, excluding flags
    files = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not files:
        print(
            "ERROR: No input files specified. Please provide one or more image files."
        )
        print(
            "Usage: detect-exif [--remove] [--quiet] [--verbose] file1.jpg file2.png ..."
        )
        return 1

    return process_files(files, remove, quiet)


if __name__ == "__main__":
    sys.exit(main())
